from linkaform_api import mongo_util
import mongo_util
from pymongo import MongoClient
from bson.objectid import ObjectId



def search_workflows(dbname, port, collection_name):
    print 'looking on dbname ...' , dbname
    cur_db = mongo_util.connect_mongodb(dbname, host, port)
    cur_col = mongo_util.get_mongo_collection(cur_db, collection_name )
    records = mongo_util.get_collection_objects(cur_col, query=None)
    count = 0
    for r in records:
        count +=1
        try:
            new_workflow = r.copy()
            new_workflow['workflows'] = []
            for trigger in r['workflows']:
                print 'trigger updatede', dbname
                new_trigger = trigger
                new_trigger['id'] = ObjectId()
                new_workflow['workflows'].append(new_trigger)
            cur_col.update({'_id':r['_id']}, new_workflow)
        except:
            print 'other type of db'
    print 'next db ...'


host='localhost'
port=27019
collection_name = 'workflow_data'

cr = MongoClient()
cr = MongoClient(host, port)

databases = cr.database_names()
databases = ['infosync_answers_client_47','infosync_answers_client_101']

for dbname in databases:
    if dbname in ['test', 'infosync']:
        continue
    search_workflows(dbname, port, collection_name)

dbname='infosync'
colection_name ='answer_version'
search_key(dbname, key, collection_name)
