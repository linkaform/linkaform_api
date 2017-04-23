import mongo_util
from pymongo import MongoClient
from bson.objectid import ObjectId
import psycopg2
import sys

def connect_to_db(dbname, host, port, collection_name):
    cur_db = mongo_util.connect_mongodb(dbname, host, port)
    cur_col = mongo_util.get_mongo_collection(cur_db, collection_name)
    return cur_db, cur_col

def get_parent(user_id):
    try:
        conn = psycopg2.connect("dbname='infosync' user='postgres' port=5434",)
    except Exception, e:
        print "I am unable to connect to the database"
        print e
        sys.exit()

    cur = conn.cursor()
    query = "select parent_id from users_customuser where id=%d" % user_id
    cur.execute(query)
    parent_id = cur.fetchone()
    return parent_id[0]

def search_records(collection, connection_id=None):
    query = {'deleted_at': {'$exists':0}}
    if connection_id:
        query['connection_id'] = connection_id
    records = mongo_util.get_collection_objects(collection, query)
    return records

def update_records_connections(db_data, records, user_col, user):
    visited_connections = []
    changed_folios = []
    for record in records:
        if not 'record' in record:
            print record['_id']
        else:
            changed_folios.append(record['folio'])
        connection = record['user_id']
        if connection in visited_connections: continue
        con_parent_id = get_parent(connection)
        user_col.update_many(
            {'form_id':record['form_id'], 'user_id': connection, 'connection_id': user} ,
            {
                "$set": {
                    'connection_id': connection
                }
            } )
        #con_parent_id = get_parent(connection)
        if not con_parent_id:
            con_parent_id = connection
        col_db_name = 'infosync_answers_client_%s' % con_parent_id
        con_db, con_col = connect_to_db(col_db_name, db_data['host'], db_data['port'], db_data['collection'])
        con_col.update_many(
            {'form_id':record['form_id'], 'user_id': connection, 'connection_id': None} ,
            {
                "$set": {
                    'connection_id': user
                }
            } )
        visited_connections.append(connection)
    return changed_folios

db_data = {
    'host': 'db2.linkaform.com',
    'port': 27017,
    'collection': 'form_answer'
}

databases = ['infosync_answers_client_96']

for dbname in databases:
    if dbname in ['infosync']:
        continue
    db_data['dbname'] = dbname
    user = 501
    user_db, user_col = connect_to_db(db_data['dbname'], db_data['host'], db_data['port'], db_data['collection'])
    records = search_records(user_col, user)
    changed_folios = update_records_connections(db_data, records, user_col, user)
    print changed_folios
