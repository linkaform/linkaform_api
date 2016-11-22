import json, psycopg2
import mongo_util
from os import remove

from bson.objectid import ObjectId

from b2_storage import B2Connection
from pymongo import MongoClient


user_id = 9
# local
media_path = '/var/www/infosync-api/backend/media/'
# dev
media_path = '/srv/slimey.info-sync.com/infosync-api/backend/media/'
# app
media_path = '/srv/backend.linkaform.com/infosync-api/backend/media/'
file_path = 'uploads/'

# MONGO
# local
host = 'localhost'
port = 27017
# dev
# host = '10.1.66.19'
# port = 27019
# app
# host = 'db3.linkaform.com'
# port = 27017
collection_name = 'form_answer'
cr = MongoClient(host, port)
mongo_dbname = 'infosync_answers_client_%s'%user_id
print 'db_name=', mongo_dbname

# POSTGRES
# local
postgres_dbname = 'infosync_1018'
conn = psycopg2.connect('dbname=%s'%postgres_dbname)
# dev
# postgres_dbname = 'infosync_prod'
# postgres_host = '10.1.66.19'
# postgres_port = '5432'
# app
# postgres_dbname = 'infosync'
# postgres_host = 'db3.linkaform.com'
# postgres_port = '5432'
# conn = psycopg2.connect('dbname=%s host=%s port=%s'%(postgres_dbname, postgres_host, postgres_port))
cur = conn.cursor()
query = "select properties from users_integration where id ={user_id};\n".format(user_id=user_id)
cur.execute(query)
properties = json.loads(cur.fetchone()[0])

storage = B2Connection()

def upload_file(form_id, field_id ,file_path, properties):
    file_name = '%s/%s/%s/%s'% (properties['folder_name'],
        form_id, field_id, file_path.split('/')[-1])
    local_path = media_path + file_path
    try:
        up_file = open(local_path)
        remove(local_path)
        print 'UPLOADING....'
        return storage.b2_save(file_name, up_file, properties['bucket_id'])
    except Exception, e:
        print 'Exception=',e
        return None


cur_db = mongo_util.connect_mongodb(mongo_dbname, host, port)
cur_col = mongo_util.get_mongo_collection(cur_db, collection_name)
query = {'deleted_at':{'$exists':0}}
records = mongo_util.get_collection_objects(cur_col, query)
for record in records:
    for _key in record['answers']:
        if isinstance(record['answers'][_key], dict):
            if 'file_url' in record['answers'][_key].keys():
                file_url = record['answers'][_key]['file_url']
                new_url = upload_file(record['form_id'], _key, file_url, properties)
                if new_url:
                    record['answers'][_key]['file_url'] = new_url
                    cur_col.update(
                        {'_id':ObjectId(record['_id'])},
                        {
                            "$set": {
                                'answers':{
                                    _key: record['answers'][_key]
                                }
                            }
                        } )
        elif isinstance(record['answers'][_key], list):
            for group in record['answers'][_key]:
                if isinstance(group, dict):
                    for group_key in group.keys():
                        if isinstance(group[group_key], dict) and 'file_url' in group[group_key]:
                            file_url = group[group_key]['file_url']
                            new_url = upload_file(record['form_id'], _key, file_url, properties)
                            if new_url:
                                group[group_key]['file_url'] = new_url
                                cur_col.update(
                                    {'_id':ObjectId(record['_id'])},
                                    {
                                        "$set": {
                                            "answers":{
                                                _key: group
                                            }
                                        }
                                    } )
