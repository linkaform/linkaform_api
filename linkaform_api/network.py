# coding: utf-8
#!/usr/bin/python

import requests, sys, simplejson, simplejson, time, threading, concurrent.futures
from bson import json_util, ObjectId
from urllib.parse import quote
import psycopg2

from pymongo import MongoClient
from pymongo.collection import Collection
requests.packages.urllib3.disable_warnings()


def unlist(arg):
    if type(arg) == list and len(arg) > 0:
        return unlist(arg[0])
    return arg

class Network:

    def __init__(self, settings={}):
        #linkaform api
        from linkaform_api import urls
        self.settings = settings
        self.api_url = urls.Api_url(settings)
        self.thread_result = []

    def login(self, session, username, password=None, get_jwt=False ,api_key=None, get_user=True):
        #data = simplejson.dumps({"password": self.settings.config['PASS'], "username": self.settings.config['USERNAME']})
        if api_key:
            data = {"username":username, "api_key": api_key}
        else:
            data = {"password": self.settings.config['PASS'], "username": self.settings.config['USERNAME']}

        response = self.dispatch(self.api_url.globals['login'], data=data, use_login=True)
        if get_user and response['status_code'] != 400:
            if response.get('content'):
                return response['content']
            if response.get('json'):
                return response['json']

        if get_jwt and response['status_code'] != 400:
            if response.get('content'):
                return response['content']['jwt']

            if response.get('json'):
                return response['json']['jwt']

        return response['status_code'] == 200

    def get_url_method(self, url_method={}, url='', method=''):
        if not url and url_method.get('url'):
            url = url_method['url']
        elif not url:
            raise Exception('No URL found')

        if not method and url_method.get('method'):
            method = url_method['method']
        elif not method:
            raise Exception ('No Method found')

        return url, method.upper()

    def dispatch(self, url_method={}, url='', method='', data={}, params={}, use_login=False, use_api_key=False, use_jwt=False,
            jwt_settings_key='JWT_KEY', encoding='utf-8', up_file=False, count=0, format_response=True):
        #must use the url_method or a url and method directly
        #url_method is a {} with a key url and method just like expres on urls
        #url defines the url to make the call
        #method is the method to use
        #use_login -Optinal- forces the dispatch to be made by login method, if not will use  the config method
        #use_api_key -Optinal- forces the dispatch to be made by api_key method, if not will use  the config method
        url, method = self.get_url_method(url_method, url=url, method=method)
        response = False
        if type(data) in (dict,str) and not up_file:
            data = simplejson.dumps(data, default=json_util.default, for_json=True)

        use_jwt = self.settings.config['USE_JWT']
        if method == 'GET':
            params = params if params else {}
            response = self.do_get(url, params=params, use_login=use_login, use_api_key=use_api_key,
                use_jwt=use_jwt, jwt_settings_key=jwt_settings_key)
        else:
            if (data == '{}' or not data) and method in ('POST', 'PATCH'):
                raise ValueError('No data to post, check you post method')

            if method == 'POST':
                response = self.do_post(url, data, use_login, use_api_key, use_jwt=use_jwt,
                    jwt_settings_key=jwt_settings_key, up_file=up_file)
            elif method == 'PATCH':
                response = self.do_patch(url, data, use_login, use_api_key, use_jwt=use_jwt,
                    jwt_settings_key=jwt_settings_key, up_file=up_file)
            elif method == 'DELETE':
                response = self.do_delete(url, data, use_login, use_api_key, use_jwt=use_jwt,
                    jwt_settings_key=jwt_settings_key, up_file=up_file)

        if response['status_code'] == 502:
            if count < 11 :
                count = count + 1
                time.sleep(5)
                self.dispatch(url_method=url_method, url=url, method=method, data=data, params=params,
                    use_login=use_login, use_api_key=use_api_key, use_jwt=use_jwt, jwt_settings_key=jwt_settings_key,
                    encoding=encoding, up_file=up_file, count=count)

        return response

    def do_get(self, url, params={}, use_login=False, use_api_key=False, use_jwt=False, jwt_settings_key=False):
        response = {'data':{}, 'status_code':''}
        JWT = self.settings.config['JWT_KEY']
        if jwt_settings_key:
            JWT = self.settings.config[jwt_settings_key]

        if use_jwt and not use_api_key:
            headers = {
                'Content-type': 'application/json',
                'Authorization':'Bearer {0}'.format(JWT)
            }

        elif use_api_key or (self.settings.config['IS_USING_APIKEY'] and not use_login):
            AUTHORIZATION_EMAIL_VALUE = self.settings.config.get('AUTHORIZATION_EMAIL_VALUE')
            AUTHORIZATION_TOKEN_VALUE = self.settings.config.get('AUTHORIZATION_TOKEN_VALUE')
            username = self.settings.config.get('USERNAME',AUTHORIZATION_EMAIL_VALUE)
            api_key = self.settings.config.get('API_KEY', self.settings.config.get('APIKEY'))
            if not api_key:
                api_key =AUTHORIZATION_TOKEN_VALUE
            headers = {
                'Content-type': 'application/json',
                'Authorization':'ApiKey {0}:{1}'.format(username, api_key)
            }
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
            response['content'] = simplejson.loads(r.content)

        try:
            response['json'] = r.json()
        except simplejson.scanner.JSONDecodeError:
            pass

        if r.status_code == 200:
            r_data = unlist(simplejson.loads(r.content))
            if r_data and r_data.get('objects'):
                response['data'] = r_data['objects']
            elif r_data and r_data.get('json'):
                response['data'] = r_data['json']
            else:
                response['data'] = r_data
        return response

    def do_post(self, url, data, use_login=False, use_api_key=False, use_jwt=False, jwt_settings_key=False, encoding='utf-8',
            up_file=False, params=False, unformatted_response=False):
        response = {'data':{}, 'status_code':''}
        send_data = {}
        JWT = self.settings.config['JWT_KEY']
        if jwt_settings_key:
            JWT = self.settings.config[jwt_settings_key]
        if use_jwt and not use_api_key:
            headers = {'Authorization':'Bearer {0}'.format(JWT)}
            if not up_file:
                headers['Content-type'] = 'application/json'
        elif use_api_key or (self.settings.config['IS_USING_APIKEY'] and not use_login):
            username = self.settings.config.get('USERNAME',self.settings.config.get['AUTHORIZATION_EMAIL_VALUE'])
            api_key = self.settings.config.get('API_KEY',self.settings.config.get['AUTHORIZATION_TOKEN_VALUE'])
            headers = {
                'Content-type': 'application/json',
                'Authorization':'ApiKey {0}:{1}'.format(username, api_key)
            }
        if use_login:
            session = requests.Session()
            if use_login or (self.login(session, self.settings.config['USERNAME'], self.settings.config['PASS']) and not use_api_key):
                if not up_file:
                    r = session.post(url, data, headers={'Content-type': 'application/json'}, verify=False)#, files=file)

                if up_file:
                    r = session.post(url, data, headers={'Content-type': 'application/json'}, verify=False, files=up_file)

        if not use_login:
            if not up_file:
                r = requests.post(url, data, headers=headers, verify=True)

            if up_file:
                r = requests.post(url, headers=headers, verify=True, files=up_file, data=data)

        if unformatted_response:
            response = r
        else:
            response['status_code'] = r.status_code
            if r.content and type(r.content) is dict:
                response['content'] = simplejson.loads(r.content)

            try:
                response['json'] = r.json()
            except simplejson.scanner.JSONDecodeError:
                pass

            if r.status_code == 200:
                try:
                    r_data = simplejson.loads(r.content)
                    # Agrego esto porque cuando se ejecuta una eliminacion de registro de catalogo el resultado es algo como:
                    # [{'ok': True, 'id': '05d7caf176a5cdd658cca083829b21a4'}]
                    if type(r_data) == list:
                        response['data'] = r_data
                        return response
                except:
                    response['data'] = r.text
                    return response

                if up_file:
                    response['data'] = r_data
                elif r_data.get('success'):
                    if r_data['success']:
                        return response
                else:
                    response['data'] = r_data.get('objects', r_data)
                    response['statud_code'] = r.status_code
            else:
                try:
                    response['data'] = r.text
                except:
                    try:
                        response['data'] = r.content
                    except:
                        response['data'] = r

        return response

    def do_patch(self, url, data, use_login=False, use_api_key=False, use_jwt=False, jwt_settings_key=False, encoding='utf-8',
            up_file=False, params=False, unformatted_response=False):
        response = {'data':{}, 'status_code':''}
        send_data = {}
        JWT = self.settings.config['JWT_KEY']
        if jwt_settings_key:
            JWT = self.settings.config[jwt_settings_key]

        if use_jwt and not use_api_key:
            headers = {
                'Content-type': 'application/json',
                'Authorization':'Bearer {0}'.format(JWT)
            }
        elif use_api_key or (self.settings.config['IS_USING_APIKEY'] and not use_login):
            username = self.settings.config.get('USERNAME',self.settings.config.get['AUTHORIZATION_EMAIL_VALUE'])
            api_key = self.settings.config.get('API_KEY',self.settings.config.get['AUTHORIZATION_TOKEN_VALUE'])
            headers = {
                'Content-type': 'application/json',
                'Authorization':'ApiKey {0}:{1}'.format(username, api_key)
            }
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
                r = requests.request('patch', url, data=data, headers=headers, verify=True)

            if up_file:
                r = requests.patch(url, headers=headers, verify=False, files=up_file, data=simplejson.loads(data))

        if unformatted_response:
            response = r
        else:
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

        return response

    def do_delete(self, url, data, use_login=False, use_api_key=False, use_jwt=False, jwt_settings_key=False, encoding='utf-8',
            up_file=False, params=False):
        response = {'data':{}, 'status_code':''}
        send_data = {}
        JWT = self.settings.config['JWT_KEY']

        if jwt_settings_key:
            JWT = self.settings.config[jwt_settings_key]

        if use_jwt and not use_api_key:
            headers = {
                'Content-type': 'application/json',
                'Authorization':'Bearer {0}'.format(JWT)
            }

        elif use_api_key or (self.settings.config['IS_USING_APIKEY'] and not use_login):
            username = self.settings.config.get('USERNAME',self.settings.config.get['AUTHORIZATION_EMAIL_VALUE'])
            api_key = self.settings.config.get('API_KEY',self.settings.config.get['AUTHORIZATION_TOKEN_VALUE'])
            headers = {
                'Content-type': 'application/json',
                'Authorization':'ApiKey {0}:{1}'.format(username, api_key)
            }

        else:
            use_login = True
            session = requests.Session()
            if use_login or (self.login(session, self.settings.config['USERNAME'], self.settings.config['PASS']) and not use_api_key):
                if not up_file:
                    r = session.delete(url, data, headers={'Content-type': 'application/json'}, verify=False)#, files=file)

                if up_file:
                    r = session.delete(url, data, headers={'Content-type': 'application/json'}, verify=False, files=up_file)
        if not use_login:
            if not up_file:
                r = requests.request('delete', url, data=data, headers=headers, verify=True)

            if up_file:
                r = requests.delete(url, headers=headers, verify=False, files=up_file, data=simplejson.loads(data))

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

        return response

    def post_forms_answers(self, answers, jwt_settings_key=False):
        answers = [answers,]
        POST_CORRECTLY=0
        errors_json = []
        response = self.post_forms_answers_list(answers, test=False, jwt_settings_key=jwt_settings_key)[0]
        self.thread_result = []
        return response

    def thread_function(self, record, url, jwt_settings_key):
        res = self.dispatch(url, data=record, jwt_settings_key=jwt_settings_key)
        if record.get('folio'):
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
        #print(' self.thread_result',  self.thread_result)
        #for index, answer in enumerate(answers):
            #print('answer', answer)
        for index, r in enumerate(self.thread_result):
            #print('r' ,r)
            #r = self.dispatch(self.api_url.form['set_form_answer'], data=answer, jwt_settings_key=jwt_settings_key )
            #r = dispatch(api_url['catalog']['set_catalog_answer'], data=answer)
            if r['status_code'] in  (201,200,202,204):
                print("Answer %s saved."%(index + 1))
                POST_CORRECTLY += 1
            else:
                print("Answer %s was rejected."%(index + 1))
                #print('data',answer)
                #print(stop_post_forms)
                errors_json.append(r)
            #res.append((index, r))
            print('Se importaron correctamente %s de %s registros'%(POST_CORRECTLY, index+1))
        if errors_json:
            #print('errors_json=', errors_json)
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
        record_id = ''
        for index, answer in enumerate(answers):
            if answer.get('deleted_objects'):
                print('deleting objects...')
                url = self.api_url.record['form_answer_patch']['url'] 
            else:
                if answer.get('_id') and answer['_id']:
                    record_id = answer.pop('_id')
                    url = self.api_url.record['form_answer_patch']['url'] +  str(record_id) + '/'
                else:
                    raise ValueError('The answer must have a record_id')
            method = self.api_url.record['form_answer_patch']['method']
            r = self.dispatch(url=url, method=method, data=answer, jwt_settings_key=jwt_settings_key)
            #r = self.dispatch(api_url['catalog']['set_catalog_answer'], data=answer)
            if r['status_code'] in  (201,200,202,204):
                print("Answer %s saved."%(index + 1))
                POST_CORRECTLY += 1
            else:
                print("Answer %s was rejected."%(index + 1))
                r['id'] = str(record_id)
                errors_json.append(r)
            res.append((index, r))
        print('Se importaron correctamente %s de %s registros'%(POST_CORRECTLY, len(answers)))
        if errors_json:
            print('errors_json=', errors_json)
            self.settings.GLOBAL_ERRORS.append(errors_json)
        return res

    def upload_answers_to_database(self, answers):
        user_connection = self.get_user_connection(config['USER_ID'])
        collection = self.create_collection(config['COLLECTION'], user_connection)
        counter = 0
        for answer in answers:
            try:
                document = collection.insert(answer)
            except:
                pass
                #print("The document {0} was not inserted".format(answer))
            finally:
                counter = counter +1

    def try_get_pdf_multi_record(self, cr_downloads, name_pdf_record, number_try=0):
        pdf_in_mongo = cr_downloads.find_one({'name': name_pdf_record, '$or':[{'status': 'done'},{'path': {'$regex': '.zip$'}}]}, {'path':1, 'status':1})
        if pdf_in_mongo:
            return pdf_in_mongo
        elif number_try == 60:
            return {'error': 'No se pudo obtener el archivo PDF'}
        time.sleep(2)
        new_number_try = number_try + 1
        return self.try_get_pdf_multi_record(cr_downloads, name_pdf_record, number_try=new_number_try)

    def pdf_record(self, record_id, template_id=None, upload_data=None, send_url=False, name_pdf='', jwt_settings_key=False):
        url = self.api_url.record['get_record_pdf']['url']
        method = self.api_url.record['get_record_pdf']['method']
        body = {
            'answer_uri': '/api/infosync/form_answer/{}/'.format(record_id),
            'filter_id':None,
            'template':template_id,
        }

        if type(record_id) == list:
            name_full_pdf = '{}_{}'.format( name_pdf, str( ObjectId() ) )
            url = self.api_url.record['get_pdf_multi_records']['url']
            method = self.api_url.record['get_pdf_multi_records']['method']
            body.pop('answer_uri')
            body.update({
                'archived': False,
                'merge': True,
                'name': name_full_pdf,
                'records_uri': record_id,
                'notify_by_email': False
            })

        
        if send_url:
            body.update({
                'send_url': send_url
            })
        response = self.dispatch(url=url, method=method, data=body, jwt_settings_key=jwt_settings_key)
        if type(record_id) == list and response.get('status_code',0) == 202:
            cr_downloads = self.get_collections( collection='download_history' )
            # db.download_history.findOne({name:'1234567' , 'status':'done'}, {path:1, status:1})
            #pdf_in_mongo = cr_downloads.find_one({'name': name_full_pdf, 'status': 'done'}, {'path':1, 'status':1})
            pdf_in_mongo = self.try_get_pdf_multi_record(cr_downloads, name_full_pdf)
            return pdf_in_mongo

        if upload_data:
            try:
                file_name = upload_data.get('file_name', '{}.pdf'.format(str(ObjectId())))
            except:
                headers = response.get('headers')
                file_name = headers['Content-Disposition'].split(';')[1].split('=')[1].strip('"').split('.')[0]
            upload_data.update({'file_name':file_name})
            f = open('/tmp/{}'.format(file_name),'w')
            if response.get('status_code') == 200:
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


    def get_mongo_passowrd(self):
        return self.get_mongo_password()

    def get_mongo_password(self):
        if not self.settings.config.get('MONGODB_PASSWORD'):
            # db_pass = self.db_password()
            response = self.dispatch(self.api_url.globals['db_password'], use_api_key=True)
            if response['status_code'] == 201:
                self.settings.config['MONGODB_PASSWORD'] = response['json']['mongo_password']
                return True
            else:
                msg = 'Could not get database password, please check your account_settings, '
                msg += ' and make sure you APIKEY parameter is correctly setup '
                raise BaseException(msg)
                return False
        return True

    def get_mongo_uri(self,db_name):
        param_url = '?authSource={0}'.format(db_name)
        user = self.settings.config['MONGODB_USER']
        if not user:
            user = "account_%s"%(self.settings.config['ACCOUNT_ID'])
        if not self.settings.config.get('MONGODB_PASSWORD'):
            self.get_mongo_password()
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
            quote(user), quote(password), mongo_hosts, param_url)
        return MONGODB_URI

    def get_user_connection(self):
        connection = {}
        if self.settings.config.get('ACCOUNT_ID'):
            user_id = self.settings.config['ACCOUNT_ID']
        else:
            user_id = self.settings.config['USER_ID']
        user_db_name = "infosync_answers_client_{0}".format(user_id)
        return self.get_infosync_connection(db_name=user_db_name)

    def get_infosync_connection(self, db_name="infosync"):
        connection = {}
        # if self.settings.config.get('ACCOUNT_ID'):
        #     user_id = self.settings.config['ACCOUNT_ID']
        # else:
        #     user_id = self.settings.config['USER_ID']
        if self.settings.config.get('MONGODB_URI'):
            connection['client'] = MongoClient(self.settings.config['MONGODB_URI'])
        else:
            mongo_uri = self.get_mongo_uri(db_name)
            connection['client'] = MongoClient(mongo_uri)
        connection['authsource'] ='admin'
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

    def postgres_cr(self):
        db_name = self.settings.config.get('PG_NAME')
        db_password = self.settings.config.get('PG_PASSWORD')
        db_user = self.settings.config.get('PG_USER')
        db_host = self.settings.config.get('PG_HOST')
        db_port = self.settings.config.get('PG_PORT')
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                port=db_port,
                host=db_host)
        except Exception as e:
            print("I am unable to connect to the database")
            print(e)
            sys.exit()
        return conn.cursor()




####
#### Catalogos
####

    def post_catalog_answers(self, answers, jwt_settings_key=False):
        answers = [answers,]
        POST_CORRECTLY=0
        errors_json = []
        return self.post_catalog_answers_list(answers, test=False, jwt_settings_key=jwt_settings_key)[0]

    def post_catalog_answers_list(self, answers, test=False, jwt_settings_key=False):
        if type(answers) == dict:
            answers = [answers,]
        POST_CORRECTLY=0
        errors_json = []
        url = self.api_url.catalog['set_catalog_answer']
        #print('*************************** url',url)
        #print('*************************** answers',answers)
        if test:
            answers = [answers[0],answers[1]]
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            executor.map(lambda x: self.thread_function(x, url, jwt_settings_key=jwt_settings_key), answers)
        for index, r in enumerate(self.thread_result):
            if r['status_code'] in  (201,200,202,204):
                print("Answer %s saved."%(index + 1))
                POST_CORRECTLY += 1
            else:
                print("Answer %s was rejected."%(index + 1))
                errors_json.append(r)
            print('Se importaron correctamente %s de %s registros'%(POST_CORRECTLY, index+1))
        if errors_json:
            if test:
                self.settings.GLOBAL_ERRORS.append(errors_json)
        response = self.thread_result
        self.thread_result = []
        return response

    def patch_catalog_answers(self, answers, jwt_settings_key=False):
        if type(answers) == dict:
            answers = [answers,]
        return self.patch_catalog_answers_list(answers, jwt_settings_key=jwt_settings_key)[0][1]

    def patch_catalog_answers_list(self, answers, jwt_settings_key=False):
        if type(answers) == dict:
            answers = [answers,]
        POST_CORRECTLY=0
        errors_json = []
        res = []
        for index, answer in enumerate(answers):
            '''if answer.get('record_id') and answer['record_id']:
                record_id = answer['record_id']
            else:
                raise ValueError('The answer must have a record_id')'''
            url = self.api_url.catalog['update_catalog_answer']['url']
            if answer.get('_id'):
                url += answer['_id'] +'/'
            method = self.api_url.catalog['update_catalog_answer']['method']
            r = self.dispatch(url=url, method=method, data=answer, jwt_settings_key=jwt_settings_key)
            if r['status_code'] in  (201,200,202,204):
                print("Answer %s saved."%(index + 1))
                POST_CORRECTLY += 1
            else:
                print("Answer %s was rejected."%(index + 1))
                #r['id'] = str(record_id)
                errors_json.append(r)
            res.append((index, r))
        print('Se importaron correctamente %s de %s registros'%(POST_CORRECTLY, len(answers)))
        if errors_json:
            print('errors_json=', errors_json)

            self.settings.GLOBAL_ERRORS.append(errors_json)
        return res
