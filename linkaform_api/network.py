# coding: utf-8
#!/usr/bin/python

import requests, simplejson, simplejson, time, threading, concurrent.futures
from bson import json_util, ObjectId
from urllib import quote_plus

from pymongo import MongoClient
from pymongo.collection import Collection
requests.packages.urllib3.disable_warnings() 


class Network:

    def __init__(self, settings={}):
        #linkaform api
        from urls import Api_url
        self.settings = settings
        self.api_url = Api_url(settings)
        self.thread_result = []

    def login(self, session, username, password, get_jwt=False):
        #data = simplejson.dumps({"password": self.settings.config['PASS'], "username": self.settings.config['USERNAME']})
        data = {"password": self.settings.config['PASS'], "username": self.settings.config['USERNAME']}
        response = self.dispatch(self.api_url.globals['login'], data=data, use_login=True)
        if get_jwt and response['status_code'] != 400:
            if response.get('content'):
                return response['content']['jwt']
            if response.get('json'):
                return response['json']['jwt']
        return response['status_code'] == 200

    def get_url_method(self, url_method={}, url='', method=''):
        if not url and url_method.has_key('url'):
            url = url_method['url']
        elif not url:
            raise Exception ("No URL found")
        if not method and url_method.has_key('method'):
            method = url_method['method']
        elif not method:
            raise Exception ("No Method found")
        return url, method.upper()

    def dispatch(self, url_method={}, url='', method='', data={}, params={},
                use_login=False, use_api_key=False, use_jwt=False, jwt_settings_key=False, 
                encoding='utf-8', up_file=False, count=0):
        #must use the url_method or a url and method directly
        #url_method is a {} with a key url and method just like expres on urls
        #url defines the url to make the call
        #method is the method to use
        #use_login -Optinal- forces the dispatch to be made by login method, if not will use  the config method
        #use_api_key -Optinal- forces the dispatch to be made by api_key method, if not will use  the config method
        #print 'in do dispatch'
        #print 'url_method', url_method
        url, method = self.get_url_method(url_method, url=url, method=method)
        response = False
        #print 'DISPATCH'
        #print 'data=', data
        if type(data) in (dict,str) and not up_file:
                data = simplejson.dumps(data, default=json_util.default, for_json=True)
        #print 'url=', url
        #print 'method', method
        #print 'jwt_settings_key',jwt_settings_key
        use_jwt = self.settings.config['USE_JWT']
        if method == 'GET':
            if params:
                response = self.do_get(url, params=params, use_login=use_login, 
                    use_api_key=use_api_key, use_jwt=use_jwt, jwt_settings_key=jwt_settings_key)
            else:
                response = self.do_get(url, use_login=use_login, 
                    use_api_key=use_api_key, use_jwt=use_jwt, jwt_settings_key=jwt_settings_key)
        if method == 'POST':
            if data == '{}' or not data:
                raise  ValueError('No data to post, check you post method')
            response = self.do_post(url, data, use_login, use_api_key, use_jwt=use_jwt, 
                jwt_settings_key=jwt_settings_key, up_file=up_file)
        if method == 'PATCH':
            if data == '{}' or not data:
                raise  ValueError('No data to post, check you post method')
            response = self.do_patch(url, data, use_login, use_api_key, use_jwt=use_jwt, 
                jwt_settings_key=jwt_settings_key, up_file=up_file)
        if response['status_code'] == 502:
            if count < 11 :
                count = count + 1
                time.sleep(5)
                self.dispatch(url_method=url_method, url=url, method=method, data=data, params=params,
                    use_login=use_login, use_api_key=use_api_key, use_jwt=use_jwt, jwt_settings_key=jwt_settings_key, 
                    encoding=encoding, up_file=up_file, count=count)
        return response

    def do_get(self, url, params= {}, use_login=False, use_api_key=False, 
        use_jwt=False, jwt_settings_key=False):
        response = {'data':{}, 'status_code':''}
        JWT = self.settings.config['JWT_KEY']
        if jwt_settings_key:
            JWT = self.settings.config[jwt_settings_key]
        if use_jwt and not use_api_key:
            headers = {'Content-type': 'application/json',
                       'Authorization':'jwt {0}'.format(JWT)}

        elif use_api_key or (self.settings.config['IS_USING_APIKEY'] and not use_login):
            headers = {'Content-type': 'application/json',
                       'Authorization':'ApiKey {0}:{1}'.format(self.settings.config['AUTHORIZATION_EMAIL_VALUE'],
                          self.settings.config['AUTHORIZATION_TOKEN_VALUE'])}
        if use_login:
            use_login = True
            session = requests.Session()
            if self.login(session, self.settings.config['USERNAME'], self.settings.config['PASS']):
                if params:
                    r = session.get(url, params=params, headers={'Content-type': 'application/json'}, verify=True)
                else:
                    r = session.get(url, headers={'Content-type': 'application/json'}, verify=True)
            else:
                raise Exception('Cannot login, please check user and password, or network connection!!!')

        if not use_login:
            if params:
                r = requests.get(url, params=params, headers=headers, verify=False)
            else:
                r = requests.get(url, headers=headers,verify=False)

        response['status_code'] = r.status_code

        if r.content and type(r.content) is dict:
            #print 'IMPRIMIENDO CONTENT: ', r.content
            response['content'] = simplejson.loads(r.content)
	
        try:
            response['json'] = r.json()
        except simplejson.scanner.JSONDecodeError:
            pass

        if r.status_code == 200:
            r_data = simplejson.loads(r.content)
            if r_data.has_key('objects'):
            	response['data'] = r_data['objects']
            elif r_data.has_key('json'):
                response['data'] = r_data['json']
            else:
                response['data'] = r_data
	#print 'RESPONSE=', response
        return response

    def do_post(self, url, data, use_login=False, use_api_key=False,
        use_jwt=False, jwt_settings_key=False, encoding='utf-8', up_file=False, params=False):
        response = {'data':{}, 'status_code':''}
        send_data = {}
        #print 'do post'
        JWT = self.settings.config['JWT_KEY']
        if jwt_settings_key:
            JWT = self.settings.config[jwt_settings_key]
        if use_jwt and not use_api_key:
            #print 'use_jwtuse_jwtuse_jwt'
            headers = {'Authorization':'jwt {0}'.format(JWT)}
            if not up_file:
                headers['Content-type'] = 'application/json'

        elif use_api_key or (self.settings.config['IS_USING_APIKEY'] and not use_login):
            headers = {'Content-type': 'application/json',
                       'Authorization':'ApiKey {0}:{1}'.format(self.settings.config['AUTHORIZATION_EMAIL_VALUE'],
                          self.settings.config['AUTHORIZATION_TOKEN_VALUE'])}

        if use_login:
            session = requests.Session()
            if use_login or (self.login(session, self.settings.config['USERNAME'], self.settings.config['PASS']) and not use_api_key):
                if not up_file:
                    r = session.post(url, data, headers={'Content-type': 'application/json'}, verify=False)#, files=file)
                if up_file:
                    r = session.post(url, data, headers={'Content-type': 'application/json'}, verify=False, files=up_file)

        if not use_login:
            if not up_file:
                r = requests.post(
                    url,
                    data,
                    headers=headers,
                    verify=True )
            if up_file:
                r = requests.post(
                    url,
                    headers=headers,
                    verify=True,
                    files=up_file,
                    data=data)

        response['status_code'] = r.status_code
        try:
            response['headers'] = r.headers
        except:
            response['headers'] = {}

        if r.content and type(r.content) is dict:
        	response['content'] = simplejson.loads(r.content)
        try:
        	response['json'] = r.json()
        except simplejson.scanner.JSONDecodeError:
            pass

        if r.status_code == 200:
            try:
                r_data = simplejson.loads(r.content)
            except:
                response['data'] = r.text
                return response

            if up_file:
                response['data'] = r_data
            elif r_data.has_key('success'):
                if r_data['success']:
                    return response
            else:
                response['data'] = r_data.get('objects',r_data)
        return response

    def do_patch(self, url, data, use_login=False, use_api_key=False,
        use_jwt=False, jwt_settings_key=False, encoding='utf-8', up_file=False, params=False):
        response = {'data':{}, 'status_code':''}
        send_data = {}
        JWT = self.settings.config['JWT_KEY']
        #print 'in do patch'
        if jwt_settings_key:
            JWT = self.settings.config[jwt_settings_key]
        if use_jwt and not use_api_key:
            headers = {'Content-type': 'application/json',
                       'Authorization':'jwt {0}'.format(JWT)}

        elif use_api_key or (self.settings.config['IS_USING_APIKEY'] and not use_login):
            headers = {'Content-type': 'application/json',
                       'Authorization':'ApiKey {0}:{1}'.format(self.settings.config['AUTHORIZATION_EMAIL_VALUE'],
                          self.settings.config['AUTHORIZATION_TOKEN_VALUE'])}

        else:
            use_login = True
            session = requests.Session()
            if use_login or (self.login(session, self.settings.config['USERNAME'], self.settings.config['PASS']) and not use_api_key):
                if not up_file:
                    r = session.patch(url, data, headers={'Content-type': 'application/json'}, verify=False)#, files=file)
                if up_file:
                    r = session.patch(url, data, headers={'Content-type': 'application/json'}, verify=False, files=up_file)
        if not use_login:
            if not up_file:
                r = requests.request("patch",
                    url,
                    data=data,
                    headers=headers,
                    verify=True )
            if up_file:
                r = requests.patch(
                    url,
                    headers=headers,
                    verify=False,
                    files=up_file,
                    data=simplejson.loads(data))

        response['status_code'] = r.status_code

        if r.content and type(r.content) is dict:
            try:
               response['content'] = simplejson.loads(r.content)
            except simplejson.scanner.JSONDecodeError:
                response['content'] = r.content
        try:
        	response['json'] = r.json()
        except simplejson.scanner.JSONDecodeError:
            pass

        if r.status_code == 200:
            response['status_code'] = r.status_code
            response['json'] = r.json()
            response['data'] = simplejson.loads(r.content)
        #print 'response', response
        return response

    def post_forms_answers(self, answers, jwt_settings_key=False):
        answers = [answers,]
        POST_CORRECTLY=0
        errors_json = []
        response = self.post_forms_answers_list(answers, test=False, jwt_settings_key=jwt_settings_key)[0]
        self.thread_result = []
        return response

    def thread_function(self, record, url, jwt_settings_key):
        res = self.dispatch(self.api_url.form['set_form_answer'], data=record, jwt_settings_key=jwt_settings_key)
        if record.has_key('folio'):
            res.update({'folio':record['folio']})
        self.thread_result.append(res)

    def post_forms_answers_list(self, answers, test=False, jwt_settings_key=False):
        if type(answers) == dict:
            answers = [answers,]
        POST_CORRECTLY=0
        errors_json = []
        url = self.api_url.form['set_form_answer']
        if test:
            answers = [answers[0],answers[1]]
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            executor.map(lambda x: self.thread_function(x, url, jwt_settings_key=jwt_settings_key), answers)
        #print ' self.thread_result',  self.thread_result
        #for index, answer in enumerate(answers):
            #print 'answer', answer
        for index, r in enumerate(self.thread_result):
            #print 'r' ,r
            #r = self.dispatch(self.api_url.form['set_form_answer'], data=answer, jwt_settings_key=jwt_settings_key )
            #r = dispatch(api_url['catalog']['set_catalog_answer'], data=answer)
            if r['status_code'] in  (201,200,202,204):
                print "Answer %s saved."%(index + 1)
                POST_CORRECTLY += 1
            else:
                print "Answer %s was rejected."%(index + 1)
                #print 'data',answer
                #print stop_post_forms
                errors_json.append(r)
            #res.append((index, r))
            print 'Se importaron correctamente %s de %s registros'%(POST_CORRECTLY, index+1)
        if errors_json:
            #print 'errors_json=', errors_json
            if test:
                self.settings.GLOBAL_ERRORS.append(errors_json)
        response = self.thread_result
        self.thread_result = []
        return response

    def patch_forms_answers(self, answers, jwt_settings_key=False):
        if type(answers) == dict:
            answers = [answers,]
        return self.patch_forms_answers_list(answers, jwt_settings_key=jwt_settings_key)[0][1]

    def patch_forms_answers_list(self, answers, jwt_settings_key=False):
        if type(answers) == dict:
            answers = [answers,]
        POST_CORRECTLY=0
        errors_json = []
        res = []
        for index, answer in enumerate(answers):
            #print 'answers', answer
            if answer.has_key('_id') and answer['_id']:
                record_id = answer.pop('_id')
            else:
                raise ValueError('The answer must have a record_id')
            url = self.api_url.record['form_answer_patch']['url'] +  str(record_id) + '/'
            method = self.api_url.record['form_answer_patch']['method']
            r = self.dispatch(url=url, method=method, data=answer, jwt_settings_key=jwt_settings_key)
            #r = self.dispatch(api_url['catalog']['set_catalog_answer'], data=answer)
            if r['status_code'] in  (201,200,202,204):
                print "Answer %s saved."%(index + 1)
                POST_CORRECTLY += 1
            else:
                print "Answer %s was rejected."%(index + 1)
                r['id'] = str(record_id)
                errors_json.append(r)
            res.append((index, r))
        print 'Se importaron correctamente %s de %s registros'%(POST_CORRECTLY, len(answers))
        if errors_json:
            print 'errors_json=', errors_json
            self.settings.GLOBAL_ERRORS.append(errors_json)
        return res

    def upload_answers_to_database(self, answers):
        print "> Uploading Content ..."
        user_connection = self.get_user_connection(config['USER_ID'])
        collection = self.create_collection(config['COLLECTION'], user_connection)
        counter = 0
        for answer in answers:
            try:
                document = collection.insert(answer)
            except:
                pass
                #print "The document {0} was not inserted".format(answer)
            finally:
                counter = counter +1

    def pdf_record(self, record_id, template_id=None, upload_data=None, jwt_settings_key=False):
        url = self.api_url.record['get_record_pdf']['url']
        method = self.api_url.record['get_record_pdf']['method']
        body = {
            'answer_uri': '/api/infosync/form_answer/{}/'.format(record_id),
            'filter_id':None,
            'template':template_id,
        }
        response = self.dispatch(url=url, method=method, data=body, jwt_settings_key=jwt_settings_key)
        if upload_data:
            try:
                headers = response.get('headers')
                file_name = headers['Content-Disposition'].split(';')[1].split('=')[1].strip('"').split('.')[0]
            except:
                file_name = upload_data.get('file_name', '{}.pdf'.format(str(ObjectId()))) 
            upload_data.update({'file_name':file_name})
            f = open('/tmp/{}'.format(file_name),'w')
            f.write(response['data'])
            f.close()
            csv_file = open('/tmp/{}'.format(file_name),'rb')
            csv_file_dir = {'File': csv_file}
            upload_url = self.dispatch(self.api_url.form['upload_file'], data=upload_data, up_file=csv_file_dir, jwt_settings_key=jwt_settings_key)
            return upload_url
        return response

    ###
    ### Database Connection
    ###


    def get_mongo_uri(self,db_name):
        param_url = '?authSource={0}'.format(db_name)

        user = self.settings.config['MONGODB_USER']
        password = self.settings.config['MONGODB_PASSWORD']
        mongo_hosts = self.settings.config['MONGODB_HOST']

        if self.settings.config.get('MONGODB_REPLICASET'):
            param_url += '&replicaSet={}'.format(self.settings.config['MONGODB_REPLICASET'])
        if self.settings.config.get('MONGODB_READPREFERENCE'):
            param_url += '&readPreference={}'.format(self.settings.config['MONGODB_READPREFERENCE'])
        if self.settings.config.get('MONGODB_MAX_POOL_SIZE'):
            param_url += '&maxPoolSize={}'.format(self.settings.config['MONGODB_MAX_POOL_SIZE'])
        if self.settings.config.get('MONGODB_MAX_IDLE_TIME'):
            param_url += '&maxidletimems={}'.format(self.settings.config['MONGODB_MAX_IDLE_TIME'])

        MONGODB_URI = 'mongodb://{0}:{1}@{2}/{3}'.format(
            quote_plus(user), quote_plus(password), mongo_hosts, param_url)
        #print 'MONGODB_URI', MONGODB_URI
        return MONGODB_URI

    def get_user_connection(self):
        connection = {}
        if self.settings.config.has_key('ACCOUNT_ID'):
            user_id = self.settings.config['ACCOUNT_ID']
        else:
            user_id = self.settings.config['USER_ID']
        user_db_name = "infosync_answers_client_{0}".format(user_id)
        return self.get_infosync_connection(db_name=user_db_name)

    def get_infosync_connection(self, db_name="infosync"):
        connection = {}
        # if self.settings.config.has_key('ACCOUNT_ID'):
        #     user_id = self.settings.config['ACCOUNT_ID']
        # else:
        #     user_id = self.settings.config['USER_ID']
        if self.settings.config.has_key('MONGODB_URI'):
            connection['client'] = MongoClient(self.settings.config['MONGODB_URI'])
        else:
            mongo_uri = self.get_mongo_uri(db_name)
            connection['client'] = MongoClient(mongo_uri)
        
        connection['db'] = connection['client'][db_name]
        return connection

    def create_collection(self, collection, user_connection):
        if config['CREATE'] and collection in user_connection['db'].collection_names():
            oldCollection = user_connection['db'][collection]
            oldCollection.drop()
        newCollection = Collection(user_connection['db'], collection, create=config['CREATE'])
        return newCollection

    def get_collections(self, collection='form_answer', create=False):
        database = self.get_user_connection()
        return Collection(database['db'], collection, create)

    def get_infsoync_collections(self, collection='form_answer', create=False):
        database = get_infosync_connection()
        return Collection(database['db'], collection, create)

####
#### Catalogos
####

    def post_catalog_answers(self, answers):
        answers = [answers,]
        POST_CORRECTLY=0
        errors_json = []
        return self.post_catalog_answers_list(answers, test=False)[0][1]

    def post_catalog_answers_list(self, answers, test=False):
        if type(answers) == dict:
            answers = [answers,]
        POST_CORRECTLY=0
        errors_json = []
        res = []
        if test:
            answers = [answers[0],answers[1]]
        for index, answer in enumerate(answers):
            # este original se va a quedar despues de migrar al api
            #r = self.dispatch(self.api_url.catalog['set_catalog_answer'], data=answer)
            # este se va a quitar al migrarlo al api
            r = self.__network.dispatch(self.api_url.catalog['set_catalog_answer'], data=answer)
            if r['status_code'] in  (201,200,202,204):
                print "Answer %s saved."%(index + 1)
                POST_CORRECTLY += 1
            else:
                print "Answer %s was rejected."%(index + 1)
                errors_json.append(r)
            res.append((index, r))
            print 'Se importaron correctamente %s de %s registros'%(POST_CORRECTLY, index+1)
        if errors_json:
            if test:
                self.settings.GLOBAL_ERRORS.append(errors_json)
        return res

    def patch_catalog_answers(self, answers):
        if type(answers) == dict:
            answers = [answers,]
        return self.patch_catalog_answers_list(answers)[0][1]

    def patch_catalog_answers_list(self, answers):
        if type(answers) == dict:
            answers = [answers,]
        POST_CORRECTLY=0
        errors_json = []
        res = []
        for index, answer in enumerate(answers):
            '''if answer.has_key('record_id') and answer['record_id']:
                record_id = answer['record_id']
            else:
                raise ValueError('The answer must have a record_id')'''
            url = self.api_url.catalog['update_catalog_answer']['url']
            method = self.api_url.catalog['update_catalog_answer']['method']
            r = self.__network.dispatch(url=url, method=method, data=answer)
            if r['status_code'] in  (201,200,202,204):
                print "Answer %s saved."%(index + 1)
                POST_CORRECTLY += 1
            else:
                print "Answer %s was rejected."%(index + 1)
                #r['id'] = str(record_id)
                errors_json.append(r)
            res.append((index, r))
        print 'Se importaron correctamente %s de %s registros'%(POST_CORRECTLY, len(answers))
        if errors_json:
            print 'errors_json=', errors_json
            self.settings.GLOBAL_ERRORS.append(errors_json)
        return res