from linkaform_api import mongo_util

from pymongo import MongoClient



def search_key(dbname, key, collection_name):
    print 'looking on dbname ...' , dbname
    cur_db = connect_mongodb(dbname, host='localhost', port=27019)
    cur_col = get_mongo_collection(cur_db, collection_name )
    records = get_collection_objects(cur_col, query = None)
    count = 0
    for r in records:
        count +=1
        try:
            if key in r['answers']:
                print 'we found the one'
                print 'database is = ',dbname
                print 'record folio: ',r['folio']
                print 'form id:',r['form_id']
                print 'record folio: ',r['id']
        except:
            print 'other type of db'
    print 'records inspected ', count
    print '... not here'

            for field in r['voucher']['fields']:
                if key in field['field_id']['id']:
                        print 'we found the one ON THE VOUCHER'
                        print 'database is = ',dbname
                        print 'record folio: ',r['folio']
                        print 'voucher id',r['voucher']['id']
                        break
host='localhost'
port=27019
collection_name = 'form_answer'
key=u'56be6c5223d3fd535cb9eb36'

cr = MongoClient()
cr = MongoClient(host, port)

databases = cr.database_names()
databases = ['infosync_answers_client_893','infosync_answers_client_874','infosync_answers_client_892']
databases = []
db_id = [96,902,892,864,899,900,874,813,898,911,865,853,812,837,893,840,790,901,789,841,854,894,897,839,820,913]
for did in db_id:
    databases.append('infosync_answers_client_%s'%did)

for dbname in databases:
    if dbname in ['test', 'infosync']:
        continue
    search_key(dbname, key, collection_name)

dbname='infosync'
colection_name ='answer_version'
search_key(dbname, key, collection_name)
