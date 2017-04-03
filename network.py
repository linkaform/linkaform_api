# coding: utf-8
#!/usr/bin/python

import requests, simplejson
from pymongo import MongoClient
from pymongo.collection import Collection


class Network:

    def __init__(self, settings={}):
        #linkaform api
        from urls import Api_url
        self.settings = settings
        self.api_url = Api_url(settings)

    def login(self, session, username, password):
        #data = simplejson.dumps({"password": self.settings.config['PASS'], "username": self.settings.config['USERNAME']})
        data = {"password": self.settings.config['PASS'], "username": self.settings.config['USERNAME']}
        response = self.dispatch(self.api_url.globals['login'], data=data, use_login=True)
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
                use_login=False, use_api_key=False, encoding='utf-8', up_file=False):
        #must use the url_method or a url and method directly
        #url_method is a {} with a key url and method just like expres on urls
        #url defines the url to make the call
        #method is the method to use
        #use_login -Optinal- forces the dispatch to be made by login method, if not will use  the config method
        #use_api_key -Optinal- forces the dispatch to be made by api_key method, if not will use  the config method
        url, method = self.get_url_method(url_method, url=url, method=method)
        response = False
        if type(data) in (dict,str):
            data = simplejson.dumps(data, encoding)
        #print 'data=', data
        #print 'url=', url
        #print 'method', method
        if method == 'GET':
            if params:
                response = self.do_get(url, params=params, use_login=use_login, use_api_key=use_api_key)
            else:
                response = self.do_get(url, use_login=use_login, use_api_key=use_api_key)
        if method == 'POST':
            if data == '{}' or not data:
                raise  ValueError('No data to post, check you post method')
            response = self.do_post(url, data, use_login, use_api_key, up_file=up_file)
        if method == 'PATCH':
            if data == '{}' or not data:
                raise  ValueError('No data to post, check you post method')
            response = self.do_patch(url, data, use_login, use_api_key, up_file=up_file)
        return response


    def do_get(self, url, params= {}, use_login=False, use_api_key=False):
        response = {'data':{}, 'status_code':''}
        if use_api_key or (self.settings.config['IS_USING_APIKEY'] and not use_login):
            headers={'Content-type': 'application/json','Authorization':'ApiKey {0}:{1}'.format(self.settings.config['AUTHORIZATION_EMAIL_VALUE'],
            self.settings.config['AUTHORIZATION_TOKEN_VALUE'])}
            if params:
                r = requests.get(url, params=params, headers={'Content-type': 'application/json','Authorization':'ApiKey {0}:{1}'.format(self.settings.config['AUTHORIZATION_EMAIL_VALUE'],
                self.settings.config['AUTHORIZATION_TOKEN_VALUE'])},verify=False)
            else:
                r = requests.get(url, headers={'Content-type': 'application/json','Authorization':'ApiKey {0}:{1}'.format(self.settings.config['AUTHORIZATION_EMAIL_VALUE'],
                self.settings.config['AUTHORIZATION_TOKEN_VALUE'])},verify=False)
        if use_login or not self.settings.config['IS_USING_APIKEY'] or r.status_code == 401:
        #if r.status_code == 401:
            session = requests.Session()
            if self.login(session, self.settings.config['USERNAME'], self.settings.config['PASS']):
                #url =dset_url + ' '/api/infosync/get_form/?form_id=10378'
                #print 'login -------------------------------------'
                if params:
                    r = session.get(url, params=params, headers={'Content-type': 'application/json'}, verify=True)
                else:
                    r = session.get(url, headers={'Content-type': 'application/json'}, verify=True)
            else:
                raise Exception('Cannot login, please check user and password, or network connection!!!')

        response['status_code'] = r.status_code
        if r.content:
        	response['content'] = simplejson.loads(r.content)
        try:
        	response['json'] = r.json()
        except simplejson.scanner.JSONDecodeError:
            pass

        if r.status_code == 200:
            r_data = simplejson.loads(r.content)
            response['data'] = r_data['objects']
        return response


    def do_post(self, url, data, use_login=False, use_api_key=False, encoding='utf-8' ,up_file=False):
        response = {'data':{}, 'status_code':''}
        send_data = {}
        if use_api_key or (self.settings.config['IS_USING_APIKEY'] and not use_login):
            if not up_file:
                #print 'url', url
                #print 'data', data
                r = requests.post(
                    url,
                    data,
                    headers={'Content-type': 'application/json',
                            'Authorization':'ApiKey {0}:{1}'.format(self.settings.config['AUTHORIZATION_EMAIL_VALUE'],
                            self.settings.config['AUTHORIZATION_TOKEN_VALUE'])},
                            verify=True )
            if up_file:
                r = requests.post(
                    url,
                    # User este header para solo datos de una forma sin archivos (imagenes, archivo, etc)
                    # 'Content-type': 'application/x-www-form-urlencoded',
                    headers={
                    'Authorization':'ApiKey {0}:{1}'.format(self.settings.config['AUTHORIZATION_EMAIL_VALUE'],
                        self.settings.config['AUTHORIZATION_TOKEN_VALUE'])},
                    verify=True,
                    files=up_file,
                    data=simplejson.loads(data))

        else:
            session = requests.Session()
            if use_login or (self.login(session, self.settings.config['USERNAME'], self.settings.config['PASS']) and not use_api_key):
                if not up_file:
                    r = requests.post(url, data, headers={'Content-type': 'application/json'}, verify=False)#, files=file)
                if up_file:
                    r = requests.post(url, data, headers={'Content-type': 'application/json'}, verify=False, files=up_file)

        response['status_code'] = r.status_code
        if r.content:
        	response['content'] = simplejson.loads(r.content)
        try:
        	response['json'] = r.json()
        except simplejson.scanner.JSONDecodeError:
            pass

        if r.status_code == 200:
            r_data = simplejson.loads(r.content)
            if up_file:
                response['data'] = r_data
            elif r_data.has_key('success'):
                if r_data['success']:
                    return response
            else:
                response['data'] = r_data['objects']
        return response


    def do_patch(self, url, data, use_login=False, use_api_key=False, encoding='utf-8' ,up_file=False):
        response = {'data':{}, 'status_code':''}
        send_data = {}
        if use_api_key or (self.settings.config['IS_USING_APIKEY'] and not use_login):
            if not up_file:
                # print 'headers=', {'Content-type': 'application/json',
                #             'Authorization':'ApiKey {0}:{1}'.format(self.settings.config['AUTHORIZATION_EMAIL_VALUE'],
                #             self.settings.config['AUTHORIZATION_TOKEN_VALUE'])}
                #
                r = requests.request("patch",
                    url,
                    data=data,
                    headers={'Content-type': 'application/json',
                            'Authorization':'ApiKey {0}:{1}'.format(self.settings.config['AUTHORIZATION_EMAIL_VALUE'],
                            self.settings.config['AUTHORIZATION_TOKEN_VALUE'])},
                    verify=True )
            if up_file:
                r = requests.patch(
                    url,
                    # User este header para solo datos de una forma sin archivos (imagenes, archivo, etc)
                    # 'Content-type': 'application/x-www-form-urlencoded',
                    headers={
                    'Authorization':'ApiKey {0}:{1}'.format(self.settings.config['AUTHORIZATION_EMAIL_VALUE'],
                        self.settings.config['AUTHORIZATION_TOKEN_VALUE'])},
                    verify=False,
                    files=up_file,
                    data=simplejson.loads(data))
        else:
            session = requests.Session()
            if use_login or (self.login(session, self.settings.config['USERNAME'], self.settings.config['PASS']) and not use_api_key):
                if not up_file:
                    print 'haria el patch por session que daba el 500'
                    #r = requests.patch(url, data, headers={'Content-type': 'application/json'}, verify=False)#, files=file)
                if up_file:
                    print 'haria el patch por session que daba el 500'
                    #r = requests.patch(url, data, headers={'Content-type': 'application/json'}, verify=False, files=up_file)


        response['status_code'] = r.status_code
        if r.content:
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
        return response


    def post_forms_answers(self, answers):
        answers = [answers,]
        POST_CORRECTLY=0
        errors_json = []
        return self.post_forms_answers_list(answers, test=False)[0][1]


    def post_forms_answers_list(self, answers, test=False):
        if type(answers) == dict:
            answers = [answers,]
        POST_CORRECTLY=0
        errors_json = []
        res = []
        if test:
            answers = [answers[0],answers[1]]
        for index, answer in enumerate(answers):
            #print 'answer', answer
            r = self.dispatch(self.api_url.form['set_form_answer'], data=answer)
            #r = dispatch(api_url['catalog']['set_catalog_answer'], data=answer)
            if r['status_code'] in  (201,200,202,204):
                print "Answer %s saved."%(index + 1)
                POST_CORRECTLY += 1
            else:
                print "Answer %s was rejected."%(index + 1)
                #print 'data',answer
                #print stop_post_forms
                errors_json.append(r)
            res.append((index, r))
            print 'Se importaron correctamente %s de %s registros'%(POST_CORRECTLY, index+1)
        if errors_json:
            #print 'errors_json=', errors_json
            if test:
                self.settings.GLOBAL_ERRORS.append(errors_json)
        return res


    def patch_forms_answers(self, answers):
        if type(answers) == dict:
            answers = [answers,]
        return self.patch_forms_answers_list(answers)[0][1]


    def patch_forms_answers_list(self, answers):
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
            r = self.dispatch(url=url, method=method, data=answer)
            #r = self.dispatch(api_url['catalog']['set_catalog_answer'], data=answer)
            if r['status_code'] in  (201,200,202,204):
                print "Answer %s saved."%(index + 1)
                POST_CORRECTLY += 1
            else:
                print 'url', url
                print "Answer %s was rejected."%(index + 1)
                r['id'] = str(record_id)
                errors_json.append(r)
            res.append((index, r))
        print 'Se importaron correctamente %s de %s registros'%(POST_CORRECTLY, index+1)
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


    ###
    ### Database Connection
    ###


    def get_user_connection(self):
        connection = {}
        user_id = self.settings.config['USER_ID']
        if not self.settings.config.has_key('REPLICASET'):
            self.settings.config['REPLICASET'] = ''
        if self.settings.config.has_key('MONGODB_URI'):
            print 'url=', self.settings.config['MONGODB_URI']
            connection['client'] = MongoClient(self.settings.config['MONGODB_URI'])
        elif self.settings.config.has_key('PORT'):
            connection['client'] = MongoClient(self.settings.config['MONGODB_HOST'],self.settings.config['MONGODB_PORT'], replicaset=self.settings.config['REPLICASET'])
        else:
            connection['client'] = MongoClient(self.settings.config['MONGODB_HOST'], replicaset=self.settings.config['REPLICASET'] )
        user_db_name = "infosync_answers_client_{0}".format(user_id)
        if not user_db_name:
            return None
        connection['db'] = connection['client'][user_db_name]
        return connection


    def get_infosync_connection(self):
        connection = {}
        user_id = self.settings.config['USER_ID']
        if not self.settings.config.has_key('REPLICASET'):
            self.settings.config['REPLICASET'] = ''
        if self.settings.config.has_key('MONGODB_URI'):
            connection['client'] = MongoClient(self.settings.config['MONGODB_URI'])
        elif self.settings.config.has_key('PORT'):
            connection['client'] = MongoClient(self.settings.config['MONGODB_HOST'],self.settings.config['MONGODB_PORT'], replicaset=self.settings.config['REPLICASET'])
        else:
            connection['client'] = MongoClient(self.settings.config['MONGODB_HOST'], replicaset=self.settings.config['REPLICASET'] )
        db_name = "infosync"
        if not db_name:
            return None
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
