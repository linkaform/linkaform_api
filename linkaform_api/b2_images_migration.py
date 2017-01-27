# PYTHON
import json, psycopg2, mongo_util
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
    query = 'select properties from users_integration where user_id ={user_id};\n'.format(user_id=user_id)
    cur.execute(query)
    return json.loads(cur.fetchone()[0])

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

def upload_file(form_id, field_id ,file_path, properties):
    file_url = None
    file_name = '%s/%s/%s/%s'% (properties['folder_name'],
        form_id, field_id, file_path.split('/')[-1])
    local_path = media_path + file_path
    thumb_name = file_name.rsplit('.', 1)[0] + '.thumbnail'
    thumb_path = local_path.rsplit('.', 1)[0] + '.thumbnail'
    try:
        if path.exists(local_path):   
            print 'UPLOADING....'
            print 'file_name=', file_name
            up_file = open(local_path)
            file_url = storage.b2_save(file_name, up_file, properties['bucket_id'])
            if path.exists(thumb_path):
                thumb_file = open(thumb_path)
            else:
                thumb_file = create_thumbnail(local_path, up_file)
            # remove(local_path)
            # remove(thumb_path)
            thumb_url = storage.b2_save(thumb_name, thumb_file, properties['bucket_id'])
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
# conn = psycopg2.connect('dbname=%s host=%s port=%s'%(postgres_dbname, postgres_host, postgres_port))
cur = conn.cursor()
# query = "select properties from users_integration where user_id ={user_id};\n".format(user_id=user_id)
# cur.execute(query)
# properties = json.loads(cur.fetchone()[0])
user_email = get_user_email(user_id)
properties = get_properties(user_id)
storage = B2Connection()

for dbname in databases:
    if dbname in ['infosync']:
        continue
    cur_db = mongo_util.connect_mongodb(dbname, host, port)
    cur_col = mongo_util.get_mongo_collection(cur_db, collection_name)
    query = {'deleted_at':{'$exists':0}}
    records = mongo_util.get_collection_objects(cur_col, query)
    new_url = None
    for record in records:
        for _key in record['answers']:
            if isinstance(record['answers'][_key], dict):
                if 'file_url' in record['answers'][_key].keys():
                    file_url = record['answers'][_key]['file_url']
                    if user_email in file_url:
                        new_url = upload_file(record['form_id'], _key, file_url, properties)
                    elif file_url:
                        connection_id = file_url.split('/')[1].split('_')[0]
                        if connection_id:
                            connection_properties = get_properties(connection_id)
                            new_url = upload_file(record['form_id'], _key, file_url, connection_properties)
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
                                file_url = group[group_key]['file_url']
                                new_url = upload_file(record['form_id'], _key, file_url, properties)
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
