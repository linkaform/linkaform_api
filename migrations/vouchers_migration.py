# coding: utf-8
#!/usr/bin/python

import sys, json, psycopg2, time, datetime, simplejson
sys.path.insert(0,"../")
from linkaform_api import mongo_util
from bson.objectid import ObjectId

# databases = cr.database_names()
databases = ['infosync_answers_client_126']
collection_name = 'form_answer'
config = {
    'HOST' : 'localhost',
    'PORT' : 27017,
}

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


def migrate_vouchers(dbname):
    print 'looking on dbname ...' , dbname
    cur_db = mongo_util.connect_mongodb(dbname, config['HOST'], config['PORT'])
    cur_col = mongo_util.get_mongo_collection(cur_db, collection_name)
    # query = {'voucher.fields': {'$exists':True}}
    query = {'form_id':561,'voucher.fields': {'$exists':True}}
    records = mongo_util.get_collection_objects(cur_col, query)
    # Voucher DB
    voucher_col = mongo_util.get_mongo_collection(cur_db, 'voucher')
    for record in records:
        voucher_id = create_voucher(voucher_col, record)
        if voucher_id:
            print 'voucher_id=',voucher_id,'\n'
            cur_col.update(
                {'_id':ObjectId(record['_id'])},
                {
                    '$unset': { 'voucher': '' }
                } )
            
            cur_col.update(
                {'_id':ObjectId(record['_id'])},
                {
                    '$set': {
                        'voucher_id':voucher_id
                    },
                } )
        else:
            print 'No voucher_id record_id=',record['_id']
    return True

def create_voucher(_col, record):
    if 'connection_id' in record:
        query = 'select parent_id from users_customuser where id ={user_id};\n'.format(
            user_id=record['connection_id'])
        cur.execute(query)
        result = cur.fetchone()
        if len(result) > 0:
            parent_id = result[0] 
        else:
            parent_id = record['connection_id']
        if not parent_id: parent_id = record['connection_id']
        connection_db = 'infosync_answers_client_%s' % parent_id
        cur_db = mongo_util.connect_mongodb(connection_db, config['HOST'], config['PORT'])
        _col = mongo_util.get_mongo_collection(cur_db, 'voucher')
    
    query = {'form_id': record['form_id'], 'updated_at':{ 
    "date": int(time.mktime(record['updated_at'].timetuple())) }}
    voucher = mongo_util.get_collection_objects(_col, query)
    if voucher.count() == 0:
        query = {'form_id': record['form_id'], 
        'updated_at':{ "date":  record['updated_at']}}
        voucher = mongo_util.get_collection_objects(_col, query)
    if voucher.count():
        voucher_id = voucher.next()['_id']
        return voucher_id
    else:
        voucher = record['voucher']
        voucher = parse_voucher(voucher)
        result = _col.insert_one(voucher)
        return result.inserted_id
    return True

def parse_voucher(voucher):
    for key, value in voucher.items():
        if key == 'id':
            voucher[key] = str(value['id'])
        if key == 'form_pages':
            for page in range(len(voucher[key])):
                for page_fields in range(len(voucher[key][page]['page_fields'])):
                    _id = str(voucher[key][page]['page_fields'][page_fields]['field_id']['id'])
                    voucher[key][page]['page_fields'][page_fields]['field_id'] = _id
                    if ('groups_fields' in voucher[key][page]['page_fields'][page_fields] and 
                        len(voucher[key][page]['page_fields'][page_fields]['groups_fields']) > 0):
                        group_fields = []
                        for group in range(len(voucher[key][page]['page_fields'][page_fields]['groups_fields'])):
                            try:
                                _id = str(voucher[key][page]['page_fields'][page_fields]['groups_fields'][group]['id'])
                                group_fields.append(_id)
                            except Exception, e:
                                print e
                                pass
                        voucher[key][page]['page_fields'][page_fields]['groups_fields'] = group_fields
                    if 'group' in voucher[key][page]['page_fields'][page_fields]:
                        _id = str(voucher[key][page]['page_fields'][page_fields]['group']['group_id']['id'])
                        voucher[key][page]['page_fields'][page_fields]['group']['group_id'] = _id
        if key == 'fields':
            for field in range(len(voucher[key])):
                _id = str(voucher[key][field]['field_id']['id'])
                voucher[key][field]['field_id'] = _id
                if ('groups_fields' in voucher[key][field] and 
                    len(voucher[key][field]['groups_fields']) > 0):
                    group_fields = []
                    for group in range(len(voucher[key][field]['groups_fields'])):
                        print 'group=', voucher[key][field]['groups_fields'][group]
                        try:
                            _id = str(voucher[key][field]['groups_fields'][group]['id'])
                            group_fields.append(_id)
                        except Exception, e:
                            print e
                            pass
                    voucher[key][field]['groups_fields'] = group_fields
                if 'group' in voucher[key][field] and len(voucher[key][field]['group']) > 0:
                    _id = str(voucher[key][field]['group']['group_id']['id'])
                    # if _id == '55ad0f9d23d3fd7c8949a411':
                    #     print voucher[key][field]
                    #     print asd
                    voucher[key][field]['group']['group_id'] = _id
    return voucher


if __name__ == '__main__':
    result = None
    for dbname in databases:
        result = migrate_vouchers(dbname)
    if result:
        print "> Updated correctly."
    else:
        print "> Updated incorrectly."