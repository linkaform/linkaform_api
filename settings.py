
#from utils import Cache

class ImportData:
    MONGO = 1
    REST = 2

#cache =Cache()

mongo_hosts = 'db2.linkaform.com:27017,db3.linkaform.com:27017,db4.linkaform.com:27017'
mongo_replicaSet = 'linkaform_replica'
MONGO_READPREFERENCE='primary'
#MONGO_READPREFERENCE='secondaryPreferred'

MAX_POOL_SIZE = 1000
WAIT_QUEUE_TIMEOUT = 1000
MONGODB_URI = 'mongodb://%s/?replicaSet=%s&readPreference=%s'%(mongo_hosts, mongo_replicaSet, MONGO_READPREFERENCE)


config = {
    'USERNAME' : '',
    'PASS' : '',
    'COLLECTION' : 'form_answer',
    'MONGODB_URI':MONGODB_URI,
    'MONGODB_PORT':27017,
    'MONGODB_HOST': 'localhost',
    'PROTOCOL' : 'https', #http or https
    'HOST' : 'dev2.linkaform.com',
    'USER_ID' : '414',
    'KEYS_POSITION' : {},
    'FILE_PATH_DIR' : '/tmp/Import/',
    'IS_USING_APIKEY' : True,
    'AUTHORIZATION_EMAIL_VALUE' : '',
    'AUTHORIZATION_TOKEN_VALUE' : '',
    #'LOAD_DATA_USING' : ImportData.MONGO,
    'LOAD_DATA_USING' : ImportData.REST,
    'CREATE' : False
}

GLOBAL_ERRORS = []
GLOBAL_VAR ={'count':0}
