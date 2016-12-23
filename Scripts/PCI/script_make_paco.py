#####
# Made by Jose Patricio VM
#####
# Script para generar pacos a partir de ordenes de Servicio de PCI Industrial
#
#
#####


from linkaform_api import settings
from linkaform_api import network, utils


#mongo_hosts = 'db2.linkaform.com:27017,db3.linkaform.com:27017,db4.linkaform.com:27017'
mongo_hosts = "127.0.0.1"
mongo_replicaSet = 'linkaform_replica'
MONGO_READPREFERENCE='primary'

MAX_POOL_SIZE = 50
WAIT_QUEUE_TIMEOUT = 1000
MONGODB_URI = 'mongodb://%s/?replicaSet=%s&readPreference=%s'%(mongo_hosts, mongo_replicaSet, MONGO_READPREFERENCE)


config = {
    #'USERNAME' : 'atencionalcliente@iesa.cc',
    #'PASS' : 'iesa2014',
    'COLLECTION' : 'form_answer',
    #'HOST' : 'db3.linkaform.com',
    'MONGODB_URI':MONGODB_URI,
    #'MONGODB_PASSWORD': mongodb_password_here
    'PORT' : 27017,
    'USER_ID' : '1259',
    'KEYS_POSITION' : {},
    'IS_USING_APIKEY' : True,
    'AUTHORIZATION_EMAIL_VALUE' : 'jgemayel@pcidustrial.com.mx',
    'AUTHORIZATION_TOKEN_VALUE' : '1a84bab48214997eced5b1baa7b0bb24a4058672',
}

settings.config = config
cr = network.get_collections()

def query_order4paco():
    query = [{'form_id': {'$in': [10540]}, 'deleted_at' : {'$exists':False}, 'answers.f1054000a030000000000002': 'liquidada'},
            {"$group": {
            "_id": {
                     'cope': "$answers.f1054000a010000000000002",
                     },
            "folioPisa": "$answers.f1054000a010000000000001",
            "folioPisaPlex": "$answers.f1054000a010000000000006",
            "telefono": "$answers.f1054000a010000000000005",
            "materiales": "$answers.f1054000a020000100000005",
            }}
            ]
    return query



def get_orders_ready4paco():
    query = query_order4paco()
    print 'queyr', query
    print fstop
    #query = {'form_id': {'$in': [10540]}, 'deleted_at' : {'$exists':False}, 'answers.f1054000a030000000000002': 'liquidada'}
    #select_columns = {'user_id':1, 'answers':1 , 'folio':1, 'conection_id':1, 'form_id':1}
    orders_records = cr.aggregate(query)
    print 'query', query
    print 'order find', orders_records.count()
    for order in orders_records:
        print 'order '
    return orders_records


def create_paco():
    orders = get_orders_ready4paco()

get_orders_ready4paco()
