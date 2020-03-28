# coding: utf-8
#!/usr/bin/python

import time, datetime, concurrent.futures

#import threading
#import concurrent.futures
#from forms import Form
import network

class Cache(object):

    def __init__(self, settings={}):
        self.items = {}
        self.items_data = {}
        self.items_fields = {}
        self.settings = settings
        from urls import Api_url
        self.api_url = Api_url(settings)
        self.network = network.Network(self.settings)
        self.thread_dict = {}

    def assigne_user_records(self, user_id, record_id_list, send_email=False, 
        send_push_notification=False, jwt_settings_key=False):
        url_method = self.api_url.record['assigne_user']
        data = {'user_id': user_id, 'records': record_id_list,
                  'send_push_notification': send_push_notification,
                  'send_mail': send_email}
        response = self.network.dispatch(url_method=url_method, data=data, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']
        return response

    def assigne_connection_records(self, connection_id, record_id_list, user_of_connection=False, 
        send_email=False, send_push_notification=False, jwt_settings_key=False):
        url_method = self.api_url.record['assigne_connection']
        data = {'connection_id': connection_id, 'records': record_id_list,
                  'send_push_notification': send_push_notification,
                  'send_mail': send_email}
        if user_of_connection:
            data['userOfConnection'] = user_of_connection
        response = self.network.dispatch(url_method=url_method, data=data, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']
        return response

    def drop_fields_for_patch(self, record):
        fields_to_drop = ['end_date','editable','updated_at','duration','index', 
                        'created_at', 'version', 'start_date', 'updated_by','voucher' ,
                        'voucher_id','connection_record_id','other_versions','mobile_record_id']
        for field in fields_to_drop:
            try:
                record.pop(field)
            except KeyError:
                pass
        return record

    def ftp_upload(self, server, username, password, file_name, file_path):
        import ftplib
        session = ftplib.FTP(server, username, password)
        file = open(file_path,'rb')                  
        session.storbinary('STOR {}'.format(file_name), file)     
        file.close()                                   
        session.quit()
        return True

    def get(self, item_type, item_id):
        if not self.items.has_key(item_type):
            #self.items[item_type] = self.get_all_items(item_type)
            self.items[item_type] = {}
        if not self.items[item_type].has_key(item_id):
            self.items[item_type][item_id] = self.get_item_id(item_type, item_id)
        return self.items[item_type][item_id]

    def get_data(self, item_type, item_id, refresh=False):
        if not self.items_data.has_key(item_type):
            self.items_data[item_type] = {}
        if not self.items_data[item_type].has_key(item_id):
            self.items_data[item_type][item_id] = self.get_item_answer(item_type, item_id)
        return self.items_data[item_type][item_id]

    def get_item_fields(self, item_type, item_id, refresh=False):
        if not self.items_fields.has_key(item_type):
            self.items_fields[item_type] = {}
        if not self.items_fields[item_type].has_key(item_id):
            self.items_fields[item_type][item_id] = self.get_item_fields(item_type, item_id)
        return self.items_fields[item_type][item_id]

    def get_item_answer(self, item_type, item_id, jwt_settings_key=False):
        if item_type =='form':
            url = self.api_url.form['form_answer']['url'] + str(item_id)
            method = self.api_url.form['form_answer']['method']
        if item_type =='catalog':
            url = self.api_url['catalog']['catalog_answer']['url'] + str(item_id)
            method = self.api_url['catalog']['catalog_answer']['method']
        response = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']
        return False

    def get_item_fields(self, item_type, item_id, jwt_settings_key=False):
        if item_type =='form':
            url = self.api_url.form['get_form_id_fields']['url'] + str(item_id)
            method = self.api_url.form['get_form_id_fields']['method']
        if item_type =='catalog':
            url = self.api_url['catalog']['catalog_id_fields']['url'] + str(item_id)
            method = self.api_url['catalog']['catalog_id_fields']['method']
        response = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']
        return False

    def get_form_id_fields(self, form_id, jwt_settings_key=False):
        url = self.api_url.form['get_form_id_fields']['url']+str(form_id)
        method = self.api_url.form['get_form_id_fields']['method']
        response = self.network.dispatch(url=url, method=method, use_api_key=False, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']
        return False

    def get_all_items(self, item_type, jwt_settings_key=False):
        if item_type =='form':
            return self.get_all_forms()
        if item_type == 'catalog':
            return self.get_all_catalogs()

    def get_item_id(self, item_type, item_id, jwt_settings_key=False):
        if item_type =='form':
            url = self.api_url.form['get_form_id']['url'] + str(item_id)
            method = self.api_url.form['get_form_id']['method']
        if item_type =='catalog':
            url = self.api_url['catalog']['get_catalog_id']['url'] + str(item_id)
            method = self.api_url['catalog']['get_catalog_id']['method']
        response = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        return response

    def get_all_forms(self, use_jwt=False, jwt_settings_key=False):
        #TODO UPDATE SELF.ITESM
        #recives the url name on the config file,GET_FORMS or GET_CATALOGS
        items = []
        if use_jwt:
            all_items = self.network.dispatch(self.api_url.form['all_forms'], use_jwt=use_jwt, jwt_settings_key=jwt_settings_key)
        all_items = self.network.dispatch(self.api_url.form['all_forms'], jwt_settings_key=jwt_settings_key)
        objects = all_items['data']
        for obj in objects:
            if obj['itype'] == 'form':# or obj['itype'] == 'catalog':
                    items.append(obj)
        return items

    def get_all_connections(self, jwt_settings_key=False):
        #TODO UPDATE SELF.ITESM
        #Returns all the connections
        connections = []
        all_connections = self.network.dispatch(self.api_url['connecions']['all_connections'], jwt_settings_key=jwt_settings_key)
        objects = all_connections['data']
        return objects

    def get_form_users(self, form_id, include_users=True, include_connections=True, 
        include_owner=True, jwt_settings_key=False):
        #Returns all the form usrs... by default includes users and connections
        connections = []
        post_json = self.api_url.get_users_url()['get_form_users']
        url = post_json['url'].format(form_id)
        response = self.network.dispatch(url=url, method=post_json['method'], jwt_settings_key=jwt_settings_key)
        all_form_users = response.get('data', [])
        if not include_connections:
            [all_form_users.pop(pos) for pos, user in enumerate(all_form_users) if user['is_connection']]
        if not include_users:
            [all_form_users.pop(pos) for pos, user in enumerate(all_form_users) if not user['is_connection']]
        if include_owner:
            all_form_users.append(response.get('json',{}).get('owner', {}))
        return all_form_users

    def get_form_connections(self, form_id, jwt_settings_key=False):
        #TODO UPDATE SELF.ITESM
        #Returns all the connections
        connections = []
        post_json = self.api_url.get_connections_url()['form_connections']
        post_json['url'] = post_json['url'] + str(form_id)
        form_connections = self.network.dispatch(post_json, jwt_settings_key=jwt_settings_key)
        objects = form_connections['data']
        return objects

    def get_connection_by_id(self, connection_id, jwt_settings_key=False):
        #TODO UPDATE SELF.ITESM
        #Returns the connections info
        url = self.api_url.connecions['connection_by_id']['url'] + str(connection_id) + '/'
        method = self.api_url.connecions['connection_by_id']['method']
        connection = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        objects = connection['data']
        return objects

    def get_all_users(self, jwt_settings_key=False):
        all_users = self.network.dispatch(self.api_url.users['all_users'], jwt_settings_key=jwt_settings_key)
        objects = all_users['data']
        return objects

    def get_user_by_id(self, user_id, jwt_settings_key=False):
        #TODO UPDATE SELF.ITESM
        #Returns all the connections
        connections = []
        url = self.api_url.users['user_by_id']['url'] + str(user_id) + '/'
        method = self.api_url.users['user_by_id']['method']
        user = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        objects = user['data']
        return objects

    def get_from_fields(self, form_id, jwt_settings_key=False):
        field = []
        url = self.api_url.form['get_form_fields']['url'] + str(form_id) + '/'
        method = self.api_url.form['get_form_fields']['method']
        fields =  self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        objects = fields['data']
        return objects

    def get_user_fileshare(self, form_id, user_id, jwt_settings_key=False):
        url_list = self.api_url.connecions['user_fileshare']['url'].split('&')
        url = url_list[0] + str(form_id)
        url += '&' + url_list[1] + str(user_id)
        method = self.api_url.form['user_fileshare']['method']
        response = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        return response

    def get_record_answer(self, params = {}, jwt_settings_key=False):
        if not params:
            params = {'limit':20,'offset':0}
        response = self.network.dispatch(self.api_url.record['form_answer'], params=params, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']
        return False
   
    def get_metadata(self, form_id=False, user_id=False):
        time_started = time.time()
        metadata = {
            "form_id" : form_id,
            "geolocation": [-100.3862645,25.644885499999997],
            "geolocation_method":{"method": "HTML5", "accuracy": 0},
            "start_timestamp" : time.time(),
            "end_timestamp" : time.time(),
        }
        if user_id:
            metadata['user_id'] = int(user_id)
        if not form_id:
            metadata.pop('form_id')
        return metadata

    def guess(self, value, answer):
        count = last_find = valuation = 0
        was_int = False
        org_value = value
        if type(answer) == int:
            was_int = True
            answer = str(answer)
        for letter in answer:
            index = value.find(letter)
            if index >= 0:
                count+=1
                if index == last_find:
                    count = count * 2
                    if was_int and index == 0:
                        count = count + 3
                value = value[:index] + value[index+1:]
                last_find = index
        return (count, org_value)

    def make_infosync_select_json(self, answer, element, best_effort=False):
        if type(answer) != str:
                answer = str(answer)
        try:
            answer = answer.decode('utf-8')
        except Exception as e:
            print 'error decoding', e
        if element.has_key('options') and  element.has_key('options'):
            options = element['options']
            default = False
            best_guess = (0,0)
            #print 'options', options
            for opt in options:
                #print 'opt', opt['value']
                #print 'opt type', type(opt['value'])
                if answer == opt['value']:
                    return opt['value']
                if answer.lower().replace(' ', '_') == opt['value']:
                    return opt['value']
                elif answer == opt['label']:
                    return opt['value']
                elif opt.has_key('selected') and opt['selected']:
                    default = opt['value']
                elif opt.has_key('default') and opt['default']:
                    default = opt['value']
                if best_effort:
                    best_guess_opt = self.guess(opt['value'], answer)
                    if best_guess_opt[0] > best_guess[0]:
                        best_guess = best_guess_opt
            if best_guess[0] > 0:
                return best_guess[1]
            if default:
                return default
        return False


        raise ValueError('element should have the keys field_type and field_id')

    def make_infosync_json(self, answer, element, best_effort=False):
        #answer: The answer or answer of certain field
        #element: should be the field for the answer
        #this should contain ['field_type'] and ['field_id']
        #If best_effort is selected then it will try the best options
        # a select field has
        #if answer or answer == 0:
        if answer or (answer==0 and element.has_key('field_type') and element['field_type'] in ('integer','float','decimal')):
            try:
                if not element.has_key('field_type') or not element.has_key('field_id'):
                    raise ValueError('element should have the keys field_type and field_id')
                if element['field_type'] in ('text', 'textarea', 'email', 'password'):
                    return {element['field_id']:str(answer)}
                if element['field_type'] in ('select-one', 'radio', 'select'):
                    answer = self.make_infosync_select_json(answer, element, best_effort)
                    if answer or answer == 0:
                        return {element['field_id']:answer}
                if element['field_type'] in ('checkbox'):
                    answer_list = []
                    for answer in answer.split(','):
                        answer = self.make_infosync_select_json(answer, element, best_effort)
                        if answer:
                            answer_list.append(answer)
                    if answer_list:
                        return {element['field_id']:answer_list}
                if element['field_type'] in ('integer'):
                    return {element['field_id']:int(answer)}
                if element['field_type'] in ('decimal','float'):
                    return {element['field_id']:float(answer)}
                if element['field_type'] in ('date', 'time', 'datetime'):
                    date_str = self.validate(str(answer), check=element['field_type'])
                    return {element['field_id']:date_str}
            except ValueError, e:
                #print 'error', e
                #print 'value', answer
                return {}
        return {}

    def thread_function_dict(self, record, data,  jwt_settings_key):
        #if record not in self.thread_dict.keys():
        data['folios'] = [record]
        res = self.network.dispatch(self.api_url.record['form_answer_patch_multi'], data=data, 
            jwt_settings_key=jwt_settings_key)
        self.thread_dict[record] = res
        #logging.info("Finishing with code"%(record, res))

    def patch_multi_record(self, answers, form_id, folios=[], record_id=[], jwt_settings_key=False, threading=False):
        if not answers or not (folios or record_id):
            print 'patch_multi_record >> no obtubo answers o folios'
            return {}
        data = {}
        data['answers'] = answers
        data['form_id'] = form_id

        if folios and not record_id:
            data['folios'] = folios

        elif not folios and record_id:
            data['records'] = record_id
        else:
            data['records'] = record_id

        data['form_id'] = form_id
        
        if threading:
            with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
                if data.get('records', False):
                    records = data.pop('records')
                    for record in records:
                        data['records'] = [record]
                        executor.map(lambda x: self.thread_function_dict(x, data, 
                            jwt_settings_key=jwt_settings_key), [record])
                elif data.get('folios', False):
                    folios = data.pop('folios')
                    for folio in folios:
                        executor.map(lambda x: self.thread_function_dict(x, data, 
                            jwt_settings_key=jwt_settings_key), [folio])
            return  self.thread_dict
        
        return self.network.dispatch(self.api_url.record['form_answer_patch_multi'], data=data, 
            jwt_settings_key=jwt_settings_key)

    def thread_function_bulk_patch(self, data, form_id,  jwt_settings_key):
        #if record not in self.thread_dict.keys():
        data['form_id'] = form_id
        #print 'data=', data

        res = self.network.dispatch(self.api_url.record['form_answer_patch_multi'], data=data, 
            jwt_settings_key=jwt_settings_key)
        #print 'res=',res
        if data.get('folio'):
            self.thread_dict[data['folio']] = res
        else:
            self.thread_dict[data['records']] = res
        #logging.info("Finishing with code"%(record, res))

    def bulk_patch(self, records, form_id, jwt_settings_key=False, threading=False):
        # if not records:
        #     print 'bulk_patch >> no obtubo answers o folios'
        #     return {}
        # if not records.get('folios') or records.get('records'):
        #     print 'no folio provided'
        #     return {}
        if threading:
            with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
                for data in records:
                    executor.map(lambda x: self.thread_function_bulk_patch(x, form_id, 
                        jwt_settings_key=jwt_settings_key), [data])
            return  self.thread_dict
        return self.network.dispatch(self.api_url.record['form_answer_patch_multi'], data=data, jwt_settings_key=jwt_settings_key)

    def post_upload_file(self, data, up_file, jwt_settings_key=False):
        #data:
        #up_file:
        upload_url = self.network.dispatch(self.api_url.form['upload_file'], data=data, up_file=up_file, jwt_settings_key=jwt_settings_key)
        return upload_url

    def patch_record(self, data, record_id=None, jwt_settings_key=False):
        #If no record_id is send, it is asuemed that the record_id
        #all ready comes inside the data dictionary
        if record_id:
            data['_id'] = record_id
        return self.network.patch_forms_answers(data , jwt_settings_key=jwt_settings_key)

    def patch_record_list(self, data, jwt_settings_key=False):
        #If no record_id is send, it is asuemed that the record_id
        #all ready comes inside the data dictionary
        return self.network.patch_forms_answers_list(data, jwt_settings_key=jwt_settings_key)

    def post_forms_answers(self, answers, test=False, jwt_settings_key=False):
        print 'post_forms_answers', jwt_settings_key
        return self.network.post_forms_answers(answers, jwt_settings_key=jwt_settings_key)

    def post_forms_answers_list(self, answers, test=False, jwt_settings_key=False ):
        print 'utls post_forms_answers_list'
        return self.network.post_forms_answers_list(answers, jwt_settings_key=jwt_settings_key)

    def validate(self, date_str, check='date'):
        #check args date, time or datetime
        if check == 'datetime':
            check_str = '%Y-%m-%d %H:%M:%S'
            date_str = date_str=str(date_str)[:19]
        elif check == 'time':
            check_str = '%H:%M:%S'
            date_str = str(date_str)[:8]
        else:
            check_str = '%Y-%m-%d'
            date_str = str(date_str)[:10]
        try:
            datetime.datetime.strptime(date_str, check_str)
            return date_str
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    def get_jwt(self, user, password, get_jwt=True):
        session = False
        jwt = self.network.login(session, user, password, get_jwt=True)
        return jwt


def warning(*objs):
    '''
    To print stuff at stderr
    '''
    output = "warning:%s\n" % objs
    stderr.write(output)
