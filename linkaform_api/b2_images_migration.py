# PYTHON
import json, psycopg2, mongo_util
from datetime import datetime
import time
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
absolute_path = 'https://app.linkaform.com/media/'

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
import  os
host = 'db3.linkaform.com'
port = 27017
collection_name = 'form_answer'
# cr = MongoClient('127.0.0.1', port)
cr = MongoClient(host, port)
# mongo_dbname = 'infosync_answers_client_%s'%user_id
#databases = open('/tmp/dbs.txt','r')
#databases = cr.database_names()
databases = ['infosync_answers_client_126']
print 'database', databases
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
#conn = psycopg2.connect('dbname=%s host=%s port=%s'%(postgres_dbname, postgres_host, postgres_port))
#cur = conn.cursor()

records_with_errors = {}
databases_with_errors = []

dbpath='/backup/infosync/2017/backup/infosync/2017/Mongoinfosync-ALLClientDB-2017-20'


for year in [2016,2015,2014]:
    for month in range(11):
        month += +1
        date_from = datetime.strptime('2015-%s-01 00:00:00'%month, "%Y-%m-%d %H:%M:%S")
        date_to = datetime.strptime('2015-%s-01 00:00:00'%(month+1), "%Y-%m-%d %H:%M:%S")
        for dbname in databases:
            #dbname.strip('\n')
            if dbname in ['infosync', 'local']:
                continue
            cur_db = mongo_util.connect_mongodb(dbname, host, port)
            # cur_db = mongo_util.connect_mongodb(dbname, '127.0.0.1', port)
            cur_col = mongo_util.get_mongo_collection(cur_db, collection_name)
            # cur_col_orig = mongo_util.get_mongo_collection(cur_db_orig, collection_name)

            query = {'deleted_at':{'$exists':0}, 'created_at':{'$gte':date_from,'$lt':date_to}}
            # query = {'deleted_at':{'$exists':0}, 'created_at':{'$gte':date}}
            # query = {'form_id':561,'deleted_at':{'$exists':0}}
            # result = mongo_util.get_collection_objects(cur_col_orig, query)
            print 'query=',query
            result = mongo_util.get_collection_objects(cur_col, query)
            print result.count()
            records = [record for record in result]
            i = 0
            print 'dbname', dbname
            for record in records:
                i += 1
                if i % 300 == 0:
                    print i
                if not record.get('answers', None):
                    continue
                ##### en los registos mas viejos del 2016 no hay porque copiar la info
                # cur_col.update(
                #      {'_id':ObjectId(record['_id'])},
                #         {
                #           "$set": {
                #                    'answers': record['answers']
                #                 }
                #           } )
                for _key in record['answers']:
                    if isinstance(record['answers'][_key], dict):
                        if 'file_url' in record['answers'][_key].keys():
                            new_url = None
                            already_in_b2 = False
                            file_url = record['answers'][_key]['file_url']
                            if file_url == False:
                                #print 'record_id', record['_id']
                                continue
                            if file_url and 'backblazeb2' in file_url:
                                if absolute_path in file_url:
                                    already_in_b2 = True
                                    file_url = file_url.replace(absolute_path, '')
                                else:
                                    continue
                            elif file_url and absolute_path in file_url:
                                last = file_url.rfind(absolute_path)
                                if last == 0:
                                    continue
                                else:
                                    file_url = file_url.replace(absolute_path, '')

                            if not already_in_b2:
                                record['answers'][_key]['file_url'] = absolute_path + file_url
                            else:
                                record['answers'][_key]['file_url'] = file_url
                            #print record['answers'][_key]['file_url']
                            cur_col.update(
                                {'_id':ObjectId(record['_id'])},
                                {
                                    "$set": {
                                        'answers.' + _key: record['answers'][_key]
                                             } })

                    elif isinstance(record['answers'][_key], list):
                        new_group = []
                        for group in record['answers'][_key]:
                            if isinstance(group, dict):
                                for group_key in group.keys():
                                    if isinstance(group[group_key], dict) and 'file_url' in group[group_key]:
                                        new_url = None
                                        file_url = group[group_key]['file_url']
                                        # print file_url
                                        # Change to absolute path
                                        if file_url and 'backblazeb2' in file_url:
                                            if absolute_path in file_url:
                                                already_in_b2 = True
                                                file_url = file_url.replace(absolute_path, '')
                                            else:
                                                continue
                                        elif file_url and absolute_path in file_url:
                                            last = file_url.rfind(absolute_path)
                                            if last == 0:
                                                continue
                                            else:
                                                file_url = file_url.replace(absolute_path, '')
                                        if not already_in_b2:
                                            group[group_key]['file_url'] = absolute_path + file_url
                                        else:
                                            group[group_key]['file_url'] = file_url
                                        print group[group_key]['file_url']
                                new_group.append(group)
                        cur_col.update(
                                    {'_id':ObjectId(record['_id'])},
                                    {
                                        "$set": {
                                            "answers." + _key: new_group
                                        }
                                    } )
            # cr.drop_database(dbname)
print 'records_with_errors=', records_with_errors
print 'dbs_with_errors=', databases_with_errors
