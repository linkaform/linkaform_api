
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
    'USERNAME' : 'josepato@linkaform.com',
    'PASS' : '654321',
    'COLLECTION' : 'form_answer',
    'MONGODB_URI':MONGODB_URI,
    'MONGODB_PORT':27017,
    'MONGODB_HOST': '',
    'PROTOCOL' : 'https', #http or https
    'HOST' : 'dev2.linkaform.com',
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
    'JWT_KEY': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Impvc2VwYXRvQGxpbmthZm9ybS5jb20iLCJ1c2VyX2lkIjoxMjYsImVtYWlsIjoiam9zZXBhdG9AbGlua2Fmb3JtLmNvbSIsImV4cCI6MTUyNzExMzI4OH0.JAfa7We1bDA7V8fITxXX21egVPie4ZhT8wF3niS3ftI'
}

GLOBAL_ERRORS = []
GLOBAL_VAR ={'count':0}
