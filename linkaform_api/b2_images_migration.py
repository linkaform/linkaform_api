# PYTHON
import json, psycopg2, mongo_util
from datetime import datetime
from PIL import Image
from os import path, remove

# MONGO
from bson.objectid import ObjectId
from pymongo import MongoClient

# LINKAFORM
from b2_storage import B2Connection

def get_user_email(user_id):
    query = 'select email from users_customuser where id ={id};\n'.format(id=user_id)
    cur.execute(query)
    return cur.fetchone()[0]

def get_properties(user_id):
    try:
        query = 'select properties from users_integration where user_id ={user_id};\n'.format(user_id=user_id)
        cur.execute(query)
        return json.loads(cur.fetchone()[0])
    except:
        return None

def create_or_get_thumbnail(image, file_name):
    """
    Creates a temp thumbnail image and returns its path.
    """
    thumb_path = path.splitext(file_name)[0] + '.thumbnail'
    x, extension = path.splitext(image.name)
    try:
        image.seek(0) # move the file position
        im = Image.open(image)
        if '.png' in extension.lower():
            im.convert('RGBA')
        else:
            im.convert('RGB')
        (width, height) = im.size

        if width >= height:
            im.thumbnail(THUMB_SIZE_H, Image.ANTIALIAS)
        else:
            im.thumbnail(THUMB_SIZE_V, Image.ANTIALIAS)

        im.save(thumb_path, 'JPEG')
        return thumb_path
    except Exception as e:
        print "Cannot create thumbnail for '%s'. %s."%(image.name, e)
    return None

def create_thumbnail(file_name, thumbnail):
    """
    Creates and save thumbnail from the given image.
    """
    thumb_name = path.splitext(file_name)[0] + '.thumbnail'
    thumb_path = create_or_get_thumbnail(thumbnail, file_name)
    thumb_up = open(thumb_path, 'r')
    return thumb_up

def get_bucket_files(bucket_id, bucket_name, folder_name):
    return storage.b2_list_file_names(bucket_id=bucket_id, max_file_count=10000, start_file_name=folder_name)

def upload_file(form_id, field_id ,file_path, properties, bucket_files):
    bucket_id = properties['bucket_id']
    bucket_name = properties['bucket_name']
    folder_name = properties['folder_name']
    file_url = None
    file_name = '%s/%s/%s/%s'% (folder_name,
        form_id, field_id, file_path.split('/')[-1])

    if file_name in bucket_files:
        print 'file already en B2'
        return file_name

    local_path = media_path + file_path
    thumb_name = file_name.rsplit('.', 1)[0] + '.thumbnail'
    thumb_path = local_path.rsplit('.', 1)[0] + '.thumbnail'
    try:
        if path.exists(local_path):   
            print 'UPLOADING....'
            print 'file_name=', file_name
            up_file = open(local_path)
            file_url = storage.b2_save(file_name, up_file, bucket_id)
            if path.exists(thumb_path):
                thumb_file = open(thumb_path)
            else:
                thumb_file = create_thumbnail(local_path, up_file)
            # remove(local_path)
            # remove(thumb_path)
            thumb_url = storage.b2_save(thumb_name, thumb_file, bucket_id)
        return file_url
    except Exception, e:
        print 'Exception=',e
        return None

# user_id = 9
# local
# media_path = '/var/www/infosync-api/backend/media/'
# dev
# media_path = '/srv/slimey.info-sync.com/infosync-api/backend/media/'
# bigbird
# media_path = '/srv/bigbird.info-sync.com/infosync-api/backend/media/'
# app
media_path = '/srv/backend.linkaform.com/infosync-api/backend/media/'
file_path = 'uploads/'

THUMB_SIZE_H = (90, 141)
THUMB_SIZE_V = (141, 90)

# MONGO
# local
# host = 'localhost'
# port = 27017
# dev
# host = '10.1.66.19'
# port = 27019
# host = '10.1.66.14'
# port = 27014
# app
host = 'db3.linkaform.com'
port = 27017
collection_name = 'form_answer'
cr = MongoClient(host, port)
# mongo_dbname = 'infosync_answers_client_%s'%user_id
# print 'db_name=', mongo_dbname
databases = cr.database_names()

# POSTGRES
# local y bigbird
# postgres_dbname = 'infosync_prod'
# conn = psycopg2.connect('dbname=%s'%postgres_dbname)
# dev
# postgres_dbname = 'infosync_prod'
# postgres_host = '10.1.66.19'
# postgres_port = '5432'
# app
postgres_dbname = 'infosync'
postgres_host = 'db3.linkaform.com'
postgres_port = '5432'
conn = psycopg2.connect('dbname=%s host=%s port=%s'%(postgres_dbname, postgres_host, postgres_port))
cur = conn.cursor()

records_with_errors = {}
databases_with_errors = []
date = datetime.strptime('2017-02-02 12:00:00', "%Y-%m-%d %H:%M:%S")

for dbname in databases:
    if dbname in ['infosync', 'local']:
        continue
    cur_db = mongo_util.connect_mongodb(dbname, host, port)
    cur_col = mongo_util.get_mongo_collection(cur_db, collection_name)
    user_id = dbname.split('_')[-1]
    if not user_id:
        print dbname
        databases_with_errors.append(dbname)
        continue
    user_email = get_user_email(user_id)
    properties = get_properties(user_id)
    if not properties:
        print 'user_id=', user_id
        continue
    storage = B2Connection()
    bucket_files = get_bucket_files(properties['bucket_id'], 
        properties['bucket_name'], properties['folder_name'])
    bucket_files = [ _file['fileName'] for _file in bucket_files]
    query = {'deleted_at':{'$exists':0}, 'created_at': {"$lte": date}}
    result = mongo_util.get_collection_objects(cur_col, query)
    records = [record for record in result]
    for record in records:
        for _key in record['answers']:
            if isinstance(record['answers'][_key], dict):
                if 'file_url' in record['answers'][_key].keys():
                    new_url = None
                    file_url = record['answers'][_key]['file_url']
                    if user_email in file_url:
                        new_url = upload_file(record['form_id'], _key, file_url, 
                            properties, bucket_files)
                    elif file_url:
                        connection_id = file_url.split('/')[1].split('_')[0]
                        if connection_id:
                            connection_properties = get_properties(connection_id)
                            connection_bucket_files = get_bucket_files(connection_properties['bucket_id'], 
                                connection_properties['bucket_name'], connection_properties['folder_name'])
                            connection_bucket_files = [ _file['fileName'] for _file in connection_bucket_files]
                            new_url = upload_file(record['form_id'], _key, file_url, 
                                connection_properties, connection_bucket_files)
                    if not new_url:
                        records_with_errors.setdefault(dbname,[]).append(record['_id'])
                    # if new_url:
                    #     record['answers'][_key]['file_url'] = new_url
                    #     cur_col.update(
                    #         {'_id':ObjectId(record['_id'])},
                    #         {
                    #             "$set": {
                    #                 'answers':{
                    #                     _key: record['answers'][_key]
                    #                 }
                    #             }
                    #         } )
            elif isinstance(record['answers'][_key], list):
                for group in record['answers'][_key]:
                    if isinstance(group, dict):
                        for group_key in group.keys():
                            if isinstance(group[group_key], dict) and 'file_url' in group[group_key]:
                                new_url = None
                                file_url = group[group_key]['file_url']
                                if user_email in file_url:
                                    new_url = upload_file(record['form_id'], _key, file_url, 
                                        properties, bucket_files)
                                elif file_url:
                                    connection_id = file_url.split('/')[1].split('_')[0]
                                    if connection_id:
                                        connection_properties = get_properties(connection_id)
                                        connection_bucket_files = get_bucket_files(connection_properties['bucket_id'], 
                                            connection_properties['bucket_name'], connection_properties['folder_name'])
                                        connection_bucket_files = [ _file['fileName'] for _file in connection_bucket_files]
                                        new_url = upload_file(record['form_id'], _key, file_url, 
                                            connection_properties, connection_bucket_files)
                                # new_url = upload_file(record['form_id'], _key, file_url, 
                                #     properties, bucket_files)
                                
                                if not new_url:
                                    records_with_errors.setdefault(dbname,[]).append(record['_id'])
                                # if new_url:
                                #     group[group_key]['file_url'] = new_url
                                #     cur_col.update(
                                #         {'_id':ObjectId(record['_id'])},
                                #         {
                                #             "$set": {
                                #                 "answers":{
                                #                     _key: group
                                #                 }
                                #             }
                                #         } )
print 'records_with_errors=', records_with_errors
print 'dbs_with_errors=', databases_with_errors
