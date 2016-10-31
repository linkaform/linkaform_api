# coding: utf-8
#!/usr/bin/python

import requests
import simplejson

from pymongo import MongoClient
from pymongo.collection import Collection

#linkaform api
import settings
from urls import api_url

def login(session, username, password):
    data = simplejson.dumps({"password": settings.config['PASS'], "username": settings.config['USERNAME']})
    response = dispatch(api_url['global']['login'], data=data, use_login=True)
    return response['status_code'] == 200

def get_url_method(url_method={}, url='', method=''):
    if not url and url_method.has_key('url'):
        url = url_method['url']
    elif not url:
        raise ("No URL found")
    if not method and url_method.has_key('method'):
        method = url_method['method']
    elif not method:
        raise ("No Method found")
    return url, method.upper()

def dispatch(url_method={}, url='', method='', data={}, use_login=False, use_api_key=False, encoding='utf-8'):
    #must use the url_method or a url and method directly
    #url_method is a {} with a key url and method just like expres on urls
    #url defines the url to make the call
    #method is the method to use
    #use_login -Optinal- forces the dispatch to be made by login method, if not will use  the config method
    #use_api_key -Optinal- forces the dispatch to be made by api_key method, if not will use  the config method
    url, method = get_url_method(url_method, url=url, method=method)
    response = False
    if type(data) == dict:
        data = simplejson.dumps(data, encoding)
    if method == 'GET':
        response = do_get(url, use_login, use_api_key)
    if method == 'POST':
        response = do_post(url, data, use_login, use_api_key)
    return response

def do_get(url, use_login=False, use_api_key=False):
    response = {'data':{}, 'status_code':''}
    session = requests.Session()
    if use_api_key or (settings.config['IS_USING_APIKEY'] and not use_login):
        r = requests.get(url, headers={'Content-type': 'application/json','Authorization':'ApiKey {0}:{1}'.format(settings.config['AUTHORIZATION_EMAIL_VALUE'],
        settings.config['AUTHORIZATION_TOKEN_VALUE'])})#,verify=False)
    #if use_login or not settings.config['IS_USING_APIKEY']:
    if r.status_code == 401:
        print '---------trying ---------------s'
        if login(session, settings.config['USERNAME'], settings.config['PASS']):
            print 'loing ok'
            print 'url/6226'
            url ='https://www.linkaform.com/api/infosync/get_form/?form_id=6226'
            r = session.get(url, headers={'Content-type': 'application/json'}, verify=False)
            print 'r',r
        else:
            raise('Cannot login, please check user and password, or network connection!!!')
    response['status_code'] = r.status_code
    if r.status_code == 200:
        r_data = simplejson.loads(r.content)
        response['data'] = r_data['objects']
    return response

def do_post(url, data, use_login=False, use_api_key=False, encoding='utf-8'):
    response = {'data':{}, 'status_code':''}
    send_data = {}
    if use_api_key or (settings.config['IS_USING_APIKEY'] and not use_login):
        r = requests.post(url, data, headers={'Content-type': 'application/json',
        'Authorization':'ApiKey {0}:{1}'.format(settings.config['AUTHORIZATION_EMAIL_VALUE'],
        settings.config['AUTHORIZATION_TOKEN_VALUE'])},verify=False)
    else:
        session = requests.Session()
        if use_login or (login(session, settings.config['USERNAME'], settings.config['PASS']) and not use_api_key):
            r = requests.post(url, data, headers={'Content-type': 'application/json'}, verify=False)
    response['status_code'] = r.status_code
    #if r.status_code == 200:
    response['data'] = simplejson.loads(r.content)
    return response
        # objects = response['objects']
        # print 'objects', objects
        # print stop_get_call
        # for obj in objects:
        #     print 'obj', obj['itype']
        #     if obj['itype'] == 'form' or obj['itype'] == 'catalog':
        #             items_ids.append(obj['id'])

def post_forms_answers(answers, test=False):
    POST_CORRECTLY=0
    errors_json = []
    if test:
        answers = [answers[0],answers[1]]
    for index, answer in enumerate(answers):
        print 'sending answer number', index
        r = dispatch(api_url['catalog']['set_catalog_answer'], data=answer)
        print 'r status code', r['status_code']
        if r['status_code'] in  (201,200,202,204):
            print "Answer %s saved."%(index + 1)
            POST_CORRECTLY += 1
        else:
            print "Answer %s was rejected."%(index + 1)
            errors_json.append(r)
    print 'Se importaron correctamente %s de %s registros'%(POST_CORRECTLY, index+1)
    if errors_json:
        print 'errors_json=', errors_json
        if test:
            settings.GLOBAL_ERRORS.append(errors_json)

def upload_answers_to_database(answers):
    print "> Uploading Content ..."
    user_connection = get_user_connection(config['USER_ID'])
    collection = create_collection(config['COLLECTION'], user_connection)
    counter = 0
    for answer in answers:
        try:
            document = collection.insert(answer)
        except:
            pass
            #print "The document {0} was not inserted".format(answer)
        finally:
            counter = counter +1


###
### Database Connection
###

def get_user_connection():
    connection = {}
    user_id = settings.config['USER_ID']
    if not settings.config.has_key('REPLICASET'):
        settings.config['REPLICASET'] = ''
    if settings.config.has_key('MONGODB_URI'):
        connection['client'] = MongoClient(settings.config['MONGODB_URI'])
    elif settings.config.has_key('PORT'):
        connection['client'] = MongoClient(settings.config['HOST'],settings.config['PORT'], replicaset=settings.config['REPLICASET'])
    else:
        connection['client'] = MongoClient(settings.config['HOST'], replicaset=settings.config['REPLICASET'] )
    user_db_name = "infosync_answers_client_{0}".format(user_id)
    if not user_db_name:
        return None
    connection['db'] = connection['client'][user_db_name]
    return connection

def create_collection(collection, user_connection):
    if config['CREATE'] and collection in user_connection['db'].collection_names():
        oldCollection = user_connection['db'][collection]
        oldCollection.drop()
    newCollection = Collection(user_connection['db'], collection, create=config['CREATE'])
    return newCollection

def get_collections(collection='form_answer', create=False):
    database = get_user_connection()
    return Collection(database['db'], collection, create)
