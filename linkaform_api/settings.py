
from utils import Cache

class ImportData:
    MONGO = 1
    REST = 2

cache =Cache()

mongo_hosts = 'db2.linkaform.com:27017,db3.linkaform.com:27017,db4.linkaform.com:27017'
mongo_replicaSet = 'linkaform_replica'
MONGO_READPREFERENCE='primary'
#MONGO_READPREFERENCE='secondaryPreferred'

MAX_POOL_SIZE = 1000
WAIT_QUEUE_TIMEOUT = 1000
MONGODB_URI = 'mongodb://%s/?replicaSet=%s&readPreference=%s'%(mongo_hosts, mongo_replicaSet, MONGO_READPREFERENCE)


config = {
    'USERNAME' : 'infosync@sanfandila.com',
    'PASS' : '123456',
    'COLLECTION' : 'form_answer',
    'MONGODB_URI':MONGODB_URI,
    'HOST' : 'localhost',
    'PORT' : 27019,
    'USER_ID' : '414',
    'KEYS_POSITION' : {},
    'FILE_PATH_DIR' : '/tmp/Import/',
    'IS_USING_APIKEY' : True,
    'AUTHORIZATION_EMAIL_VALUE' : 'infosync@sanfandila.com',
    'AUTHORIZATION_TOKEN_VALUE' : '530bd4396d7ffd9f6ee76aea4f621e7d00cd9e21',
    #'LOAD_DATA_USING' : ImportData.MONGO,
    'LOAD_DATA_USING' : ImportData.REST,
    'CREATE' : False
}

GLOBAL_ERRORS = []
GLOBAL_VAR ={'count':0}
