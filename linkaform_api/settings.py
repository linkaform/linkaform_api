
#from utils import Cache

class ImportData:
    MONGO = 1
    REST = 2

#cache =Cache()

mongo_hosts = 'dev1.linkaform.com:27017,dev2.linkaform.com:27027,dev3.linkaform.com:27037'
mongo_replicaSet = 'info_repl'
MONGO_READPREFERENCE='primary'
#MONGO_READPREFERENCE='secondaryPreferred'

MAX_POOL_SIZE = 1000
WAIT_QUEUE_TIMEOUT = 1000
MONGODB_URI = 'mongodb://%s/?replicaSet=%s&readPreference=%s'%(mongo_hosts, mongo_replicaSet, MONGO_READPREFERENCE)


config = {
    'USERNAME' : 'your_likaform_username@here.com',
    'PASS' : 'YOUR_PASSOWRD_HERE',
    'COLLECTION' : 'form_answer',
    'MONGODB_PORT':27017,
    'MONGODB_HOST': '',
    'MONGODB_USER': '',
    # 'MONGODB_REPLICASET': 'linkaform_replica',
    # 'MONGO_READPREFERENCE': 'secondaryPreferred',
    'MONGODB_MAX_IDLE_TIME': 12000,
    'MONGODB_MAX_POOL_SIZE': 1000,
    'PROTOCOL' : 'https', #http or https
    'HOST' : 'qa.linkaform.com',
    'HOST_BOB' : 'bob.linkaform.com',
    'AIRFLOW_PROTOCOL' : 'https', #http or https
    # 'AIRFLOW_PORT' : 5000, #http or https
    #'AIRFLOW_HOST' : 'af.linkaform.com',
    'AIRFLOW_HOST' : 'airflow.linkaform.com',
    'USER_ID' : '',
    'ACCOUNT_ID': '',
    'KEYS_POSITION' : {},
    'FILE_PATH_DIR' : '/tmp/Import/',
    'IS_USING_APIKEY' : True,
    'AUTHORIZATION_EMAIL_VALUE' : '',
    'AUTHORIZATION_TOKEN_VALUE' : '',
    #'LOAD_DATA_USING' : ImportData.MONGO,
    'LOAD_DATA_USING' : ImportData.REST,
    'CREATE' : False,
    'JWT_KEY': False,
    'USE_JWT': True,
    'COUCH_ENV':'prod',
    'COUCH_PROTOCOL':'http',
    'COUCH_USER':'',
    'COUCH_PASSWORD':'',
    'COUCH_HOST':'',
    'COUCH_PORT':'',
    'COUCH_DEV_PROTOCOL':'http',
    'COUCH_DEV_USER':'',
    'COUCH_DEV_PASSWORD':'',
    'COUCH_DEV_HOST':'',
    'COUCH_DEV_PORT':'',
}

GLOBAL_ERRORS = []
GLOBAL_VAR ={'count':0}
