from datetime import datetime

from linkaform_api import settings
from linkaform_api import network, utils


mongo_hosts = 'db2.linkaform.com:27017,db3.linkaform.com:27017,db4.linkaform.com:27017'
mongo_replicaSet = 'linkaform_replica'
MONGO_READPREFERENCE='primary'
#MONGO_READPREFERENCE='secondaryPreferred'

MAX_POOL_SIZE = 1000
WAIT_QUEUE_TIMEOUT = 1000
MONGODB_URI = 'mongodb://%s/?replicaSet=%s&readPreference=%s'%(mongo_hosts, mongo_replicaSet, MONGO_READPREFERENCE)

config = {
    'USERNAME' : 'atencionalcliente@iesa.cc',
    'PASS' : 'iesa2014',
    'COLLECTION' : 'form_answer',
    #'HOST' : 'db3.linkaform.com',
    'MONGODB_URI':MONGODB_URI,
    'PORT' : 27017,
    'USER_ID' : '96',
    'KEYS_POSITION' : {},
    'IS_USING_APIKEY' : True,
    'AUTHORIZATION_EMAIL_VALUE' : 'atencionalcliente@iesa.cc',
    'AUTHORIZATION_TOKEN_VALUE' : '1a84bab48214997eced5b1baa7b0bb24a4058672',
}

settings.config = config
cr = network.get_collections()
cr_infosync = network.get_infsoync_collections(collection='answer_version')


conexion_form_id = 6180
service_form_id = 6143

def get_all_users():
    from IESA import users
    result = users.users
    return result

#lkf_api = utils.Cache()
USERS = get_all_users()

def get_connections_users():
    from IESA import connections
    connecitions = connections.connections
    result = {}
    for connection, user in connecitions['objects'].iteritems():
        for usr in user:
            if usr.has_key('user_id'):
                result[usr['user_id']] = {'user_name':usr['user_name']}
            else:
                result[usr['user']] = {'user_name':usr['user_name']}
    return result


CONNECTIONS = get_connections_users()


def get_user_info(user_id):
    result = {}
    result['user_id'] = user_id
    if user_id in CONNECTIONS:
        result['first_name'] = CONNECTIONS[user_id]['user_name']
        result['user_id'] = user_id
    else:
        for user in USERS:
            if user['id'] == user_id:
                result['first_name'] = user['first_name']
                result['user_id'] = user['id']
                result['email'] = user['email']
    return result


def  get_record_versions(record):
    query = {'folio':record['folio'], 'deleted_at' : {'$exists':False}}
    select_columns = {'user_id':1, 'duration':1, 'version':1, 'folio':1, 'conection_id':1, 'start_timestamp':1, 'end_timestamp':1}
    version_records = cr_infosync.find(query, select_columns)
    version_records = [a for a in version_records]
    return version_records


def get_folio_version_users(record, version_records, users_ids):
    #duration = record['duration']
    #result = record
    duration = 0
    count =0
    version_records.append(record)
    responsible ={'form_owner': {}}
    if record['user_id']  in users_ids:
        responsible ={'form_owner': get_user_info(record['user_id'])}
    #if rec['user_id'] not in users_ids:
    for rec in version_records:
        rec.pop('_id')
        if rec['user_id'] not in users_ids:
            #si el uesr id del registro no esta en la lista de usarios
            #Entonoces es una conexion
            continue
        count +=1
        if rec.has_key('duration'):
            rec_duration = rec['duration']
        else:
            rec_duration =  rec['end_timestamp'] - rec['start_timestamp']
        if rec_duration > duration:
            result = rec
            responsible = {'form_owner': get_user_info(rec['user_id'])}
            duration = rec_duration
    return responsible


def get_folio_version_connection(record, version_records, users_ids):
    duration = 0
    count =0
    version_records.append(record)
    responsible ={'connection': {}}
    if record['user_id'] not in users_ids:
        responsible = {'connection': get_user_info(record['user_id'])}
    #if rec['user_id'] not in users_ids:
    for rec in version_records:
        if rec['user_id'] in users_ids:
            #si el uesr id del registro  esta en la lista de usarios
            #Entonoces NO es una conexion
            continue
        count +=1
        if rec.has_key('duration'):
            rec_duration = rec['duration']
        else:
            rec_duration = rec['end_timestamp'] - rec['start_timestamp']
        if rec_duration > duration:
            result = rec
            responsible = {'connection': get_user_info(rec['user_id'])}
            duration = duration = rec_duration
    if not responsible['connection'] and rec.has_key('connection_id'):
        responsible['connection'] = get_user_info(rec['connection_id'])
    return responsible


def get_folios_user():
    query ={ 'form_id': {'$in': [6180, 6143]},'deleted_at' : {'$exists':False}}
    select_columns = {'user_id':1, 'duration':1, 'version':1, 'folio':1, 'connection_id':1, 'start_timestamp':1, 'end_timestamp':1, 'properties':1}
    records = cr.find(query, select_columns)
    count =0
    users_ids = [u['id'] for u in USERS]
    for rec in records:
        record_id = rec['_id']
        properties = {}
        responsible = {}
        if rec.has_key('properties'):
            properties = rec['properties']
        count +=1
        #if count > 5:
        #    break
        if rec['version'] >= 1:
            version_records = get_record_versions(rec)
            form_owner = get_folio_version_users(rec, version_records, users_ids)
            connection = get_folio_version_connection(rec, version_records, users_ids)
        else:
            #form_owner = {'form_owner': get_user_info(rec['user_id'])}
            user_record = rec
            if rec.has_key('connection_id'):
                connection = {'connection':get_user_info(rec['connection_id'])}
        responsible.update(form_owner)
        responsible.update(connection)
        properties.update({'responsible':responsible })
        update = {'id':record_id}, {"$set":{'properties':properties}}
        cr.update({'_id':record_id}, {'$unset':{'properites':1}})
        cr.update({'_id':record_id}, {"$set":{'properties':properties}})


get_folios_user()
