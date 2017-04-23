# coding: utf-8
#!/usr/bin/python

import requests


def login(session, username, password):
    r = session.post(config['LOGIN_URL'], data = simplejson.dumps({"password": config['PASS'], "username": config['USERNAME']}))
    return r.status_code == 200


def login(session, username, password):
    r = session.post(config['LOGIN_URL'], data = simplejson.dumps({"password": config['PASS'], "username": config['USERNAME']}))
    return r.status_code == 200

def post_answers(session, answers, is_catalog,  test=False):
    POST_CORRECTLY=0
    errors_json = []
    if is_catalog :
        post_url = config['CATALOG_ANSWER_URL']
    else:
        post_url = config['FORM_ANSWER_URL']
    if test:
        answers = [answers[0],answers[1]]
    for index, answer in enumerate(answers):
        if config['IS_USING_APIKEY']:
            r = session.post(post_url, data = simplejson.dumps(answer, encoding='utf-8'), headers={'Content-type': 'application/json', 'Authorization':'ApiKey {0}:{1}'.format(config['AUTHORIZATION_EMAIL_VALUE'], config['AUTHORIZATION_TOKEN_VALUE'])}, verify=False)
        else:
            r = session.post(post_url, data = simplejson.dumps(answer, encoding='utf-8'), headers={'Content-type': 'application/json'}, verify=False)
        if r.status_code == 201:
            print "Answer %s saved."%(index + 1)
            POST_CORRECTLY += 1
        else:
            print "Answer %s was rejected."%(index + 1)
            print 'r.content', r.content
            response = simplejson.loads(r.content)
            errors_json.append(response)
    print 'Se importaron correctamente %s de %s registros'%(POST_CORRECTLY, index+1)
    if errors_json:
        print 'errors_json=', errors_json
        if test:
            GLOBAL_ERRORS.append(errors_json)

def rest_call(method, url):
    #TODO
    session = requests.Session()
    url = config[item_type]
    print 'url', url
    if config['IS_USING_APIKEY']:
        if method == 'get':
            r = session.get(url, headers={'Content-type': 'application/json', 'AUTHORIZATION':'ApiKey {0}:{1}'.format(config['AUTHORIZATION_EMAIL_VALUE'], config['AUTHORIZATION_TOKEN_VALUE'])}, verify=False)
    if login(session, config['USERNAME'], config['PASS']):
        print "User logged in.",url
        if method == 'get':
            r = session.get(url, headers={'Content-type': 'application/json'}, verify=False)
    if r.status_code == 200:
        return r
    else:
        return False


def upload_answers_to_database(answers):
    print "> Uploading Content ..."
    user_connection = get_db_connection(config['USER_ID'])
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

def upload_answers_using_rest(answers,is_catalog=False, test=False):
    session = requests.Session()
    if config['IS_USING_APIKEY']:
        post_answers(session, answers, is_catalog, test)
    else:
        # Log In
        if login(session, config['USERNAME'], config['PASS']):
            print "User logged in.",
            post_answers(session, answers, is_catalog, test)
        else:
            print "Invalid login."


####
### Database connections
####

def get_mongo_connection():
    print "> Getting connection ..."
    connection = {}
    connection['client'] = MongoClient(config['HOST'], config['PORT'])
    return connection

def get_db_connection(db_name=False):
    connection = get_mongo_connection()
    if db_name == 'infosync':
        db_name = "infosync"
    else:
        db_name = "infosync_answers_client_{0}".format(user_id)
    if not db_name:
        return None
    connection['db'] = connection['client'][db_name]
    return connection

def get_collection_connection(db_name, collection_name):
    connection = get_db_connection(db_name)
    return Collection(connection['db'],collection_name, create=config['CREATE'])

def create_collection(collection, user_connection):
    print "> Creating Collection ..."
    if config['CREATE'] and collection in user_connection['db'].collection_names():
        oldCollection = user_connection['db'][collection]
        oldCollection.drop()
    newCollection = Collection(user_connection['db'], collection, create=config['CREATE'])
    return newCollection
