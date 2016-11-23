# from linkaform_api import mongo_util
import mongo_util
from pymongo import MongoClient
from bson.objectid import ObjectId



def search_ids(dbname, port, collection_name, folio_list):
    print 'looking on dbname ...' , dbname
    found_it = False
    cur_db = mongo_util.connect_mongodb(dbname, host, port)
    cur_col = mongo_util.get_mongo_collection(cur_db, collection_name )
    for folio in folio_list:
        query = {'_id':ObjectId(folio)}
        records = mongo_util.get_collection_objects(cur_col, query)
        if records.count() > 0:
            for res in records:
                print '-----------------------------------------'
                print ' folio:', res['folio']
                print 'id ', res['_id']
                print 'database', dbname
            found_it = True
    print 'next db ...'
    return found_it

def search_folios(dbname, port, collection_name, folio_list):
    print 'looking on dbname ...' , dbname
    found_it = False
    cur_db = mongo_util.connect_mongodb(dbname, host, port)
    cur_col = mongo_util.get_mongo_collection(cur_db, collection_name )
    for folio in folio_list:
        query = {'folio':folio}
        records = mongo_util.get_collection_objects(cur_col, query)
        if records.count() > 0:
            for res in records:
                print '-----------------------------------------'
                print ' folio:', res['folio']
                print 'id ', res['_id']
                print 'database', dbname
            found_it = True
    print 'next db ...',found_it
    return found_it


def search_workflows(dbname, port, collection_name, folio_list):
    print 'looking on dbname ...' , dbname
    found_it = False
    cur_db = mongo_util.connect_mongodb(dbname, host, port)
    cur_col = mongo_util.get_mongo_collection(cur_db, collection_name )
    for folio in folio_list:
        query = {'_id':ObjectId(folio)}
        records = mongo_util.get_collection_objects(cur_col, query)
        if records.count() > 0:
            for res in records:
                print '-----------------------------------------'
                print ' folio:', res['folio']
                print 'id ', res['_id']
                print 'database', dbname
            found_it = True
    print 'next db ...',found_it
    return found_it

def search_lost_folios(dbname, port, collection_name, form_list):
    print 'looking on dbname ...' , dbname
    found_it = {}
    infosync_db = mongo_util.connect_mongodb('infosync', host, port)
    infosync_cr = mongo_util.get_mongo_collection(infosync_db, 'answer_version' )
    cur_db = mongo_util.connect_mongodb(dbname, host, port)
    cur_col = mongo_util.get_mongo_collection(cur_db, collection_name )
    for form_id in form_list:
        query = {'form_id':form_id, 'deleted_at': {'$exists':0}}
        records = mongo_util.get_collection_objects(cur_col, query)

        for res in records:
            print '-----------------------------------------'
            print ' folio:', res['folio']
            old_folio = None
            other_versions = res['other_versions']
            if other_versions:
                old_folio = search_folio_in_versions(infosync_cr, other_versions, res['folio'])

            if old_folio:
                found_it.update({old_folio:res['folio']})
                res['folio'] = old_folio
                # search how to save
                cur_col.update_one(
                    {'_id':ObjectId(res['_id'])},
                    {
                        "$set": {
                            "folio":old_folio
                        }
                    } )
                print 'other_versions',other_versions

    print 'next db ...',found_it
    print 'found this folios', found_it
    return found_it

def search_folio_in_versions(infosync_cr, other_versions, folio):
    version_ids = []
    folio_ver1 = None
    for version in other_versions:
        uri = version['uri'].replace('/api/infosync/version/', '')
        query = {'_id':ObjectId(uri[:-1])}
        record = mongo_util.get_collection_objects(infosync_cr, query)
        for res in record:
            version_ids.append(res['_id'])
    print 'version_ids', version_ids

    #checar como hacer el in de object ids
    query = {'_id': { '$in': version_ids }, 'folio':{'$ne':folio}}
    #revisar si se puede hacer un query a la version 1
    records = mongo_util.get_collection_objects(infosync_cr, query)

    if records.count() > 0:
        query = {'_id': { '$in': version_ids }, 'version':1 }
        record_ver1 = mongo_util.get_collection_objects(infosync_cr, query)
        for vres in record_ver1:
            folio_ver1 = vres['folio']
            # return folio_ver1
        for res in version_ids:
            print '***********************'
            print 'folio_ver1', folio_ver1
            #print ' folio:', res['folio']
            #print ' id', res['_id']

            infosync_cr.update_one(
                {'_id':res},
                {
                    "$set": {
                        "folio":folio_ver1
                    }
                } )
            print '***********************'
        return folio_ver1
    return False

def update_voucher(dbname, port, collection_name, form_list, id_voucher):
    print 'looking on dbname ...' , dbname
    found_it = False
    found_it = []
    cur_db = mongo_util.connect_mongodb(dbname, host, port)
    cur_col = mongo_util.get_mongo_collection(cur_db, collection_name )
    query = {'_id': ObjectId(id_voucher)}
    record = mongo_util.get_collection_objects(cur_col, query)
    voucher_copy =  record.next()['voucher']
    for _id in form_list:
        query = {'form_id': _id, 'voucher.fields': {'$exists':0}, 'deleted_at' : {'$exists':0} }
        records = mongo_util.get_collection_objects(cur_col, query)
        print records.count()
        if records.count() > 0:
            for res in records:
                found_it.append(res['_id'])
                # res['voucher'] = voucher_copy
                cur_col.update_one(
                    {'_id':ObjectId(res['_id'])},
                    {
                        "$set": {
                            "voucher":voucher_copy
                        }
                    } )
    print 'Found', found_it
    print 'next db ...'
    return found_it

def created_at_wrong_type(dbname, host, port, collection_name):
    print 'looking on dbname ...' , dbname
    found_it = False
    found_it = []
    cur_db = mongo_util.connect_mongodb(dbname, host, port)
    cur_col = mongo_util.get_mongo_collection(cur_db, collection_name )
    query = {'created_at': {'$not': {'$type': 9}}}
    record = mongo_util.get_collection_objects(cur_col, query)
    count = record.count()
    if count > 0 :
        print 'dbname', dbname
        print 'count > 0'
        return dbname
    return False

host = 'db3.linkaform.com'
# host = 'localhost'

port = 27017
# port=27019
# collection_name = "workflow_data"
collection_name = 'form_answer'
cr = MongoClient()
cr = MongoClient(host, port)

databases = cr.database_names()
# databases = ['infosync_answers_client_96']#,'infosync_answers_client_9']


# folio_list = ['254010-96','239265-96',  '255619-96']
# folio_list = [ '57111ed923d3fd3044bca122']
# folio_list = ['53d6e61001a4de609b882a06']
# folio_list = ['571a9cb823d3fd5bf31860c1', '571a9cd923d3fd5bf31860c4']
# folio_list = [ '255619-96']
# form_list = [6180, 6143, 6248]
#form_list = [6143]
#pdf que no imprime la imagen
# form_list = ['571e6ea323d3fd2744ee502d', '571ea1cf23d3fd27400fbf0d']
found_all = 0

# worklfow = ["571f9ce723d3fd2ea8d0bd2b"]

# folio_list = ['57111ed923d3fd3044bca122']

#folio_list = ['573b899923d3fd40a0d9c072']
#error pdf mayo 20 2016
#folio_list = ['57311bcc23d3fd0fc31d0a86']
# folio_list =['574f23b423d3fd18f123da4a', '576dc078b43fdd1ea9b71b72' ]
#error mayo 20 2016
#folio_list = ['5749b24823d3fd6c2df1a3b8', '5748cac923d3fd219569826d' ]
#error octubre 28 2016
# folio_list = ['57718cc1b43fdd39c63780ec']




# 577c3a7eb43fdd15c725a9d7
# 577c3a7eb43fdd15c725a9d7

#error junio 1 2016
# folio_list = ['56fda2d223d3fd0b9f7c9c67', '574f4d5423d3fd18f123da62' ,'56e87ff223d3fd60fa6c4dc9']

# form_list = [6248]
# error no voucher 11 nov 2016
# form_list = ['10133']
# databases = ['infosync_answers_client_558']
# id_voucher = '5824da6ab43fdd5a2e19da3b'
# folio_list = ['5829e3e7b43fdd12f4913d26']
folio_list = ['5825f424b43fdd5a2f6adac7']
dbs_with_error  = []


for dbname in databases:
    if dbname in ['infosync']:#['test', 'infosync', 'admin']:
        continue
    found_it = search_ids(dbname, port, collection_name, folio_list)
    # found_it = update_voucher(dbname, port, collection_name, form_list, id_voucher)
    if found_it:
        found_all += 1
        if found_all == len(folio_list):
            break
#     dd = created_at_wrong_type(dbname, host, port, collection_name)
#     if dd:
#         dbs_with_error.append(dd)
# print dbs_with_error
    #search_workflows(dbname, port, collection_name, folio_list)

# for dbname in databases:
#     if dbname in ['test', 'infosync']:
#         continue
#     found_it = search_ids(dbname, port, collection_name, folio_list)
#     if found_it:
#         found_all += 1
#         if found_all == len(folio_list):
#             break
