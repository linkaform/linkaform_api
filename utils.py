# coding: utf-8
#!/usr/bin/python

import time, datetime

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


    def get_item_answer(self, item_type, item_id):
        if item_type =='form':
            url = self.api_url.form['form_answer']['url'] + str(item_id)
            method = self.api_url.form['form_answer']['method']
        if item_type =='catalog':
            url = self.api_url['catalog']['catalog_answer']['url'] + str(item_id)
            method = self.api_url['catalog']['catalog_answer']['method']
        response = self.network.dispatch(url=url, method=method)
        if response['status_code'] == 200:
            return response['data']
        return False


    def get_item_fields(self, item_type, item_id):
        if item_type =='form':
            url = self.api_url.form['get_form_id_fields']['url'] + str(item_id)
            method = self.api_url.form['get_form_id_fields']['method']
        if item_type =='catalog':
            url = self.api_url['catalog']['catalog_id_fields']['url'] + str(item_id)
            method = self.api_url['catalog']['catalog_id_fields']['method']
        response = self.network.dispatch(url=url, method=method)
        if response['status_code'] == 200:
            return response['data']
        return False


    def get_form_id_fields(self, form_id):
        url = self.api_url.form['get_form_id_fields']['url']+str(form_id)
        method = self.api_url.form['get_form_id_fields']['method']
        response = self.network.dispatch(url=url, method=method, use_api_key=False)
        if response['status_code'] == 200:
            return response['data']
        return False


    def get_all_items(self, item_type):
        if item_type =='form':
            return self.get_all_forms()
        if item_type == 'catalog':
            return self.get_all_catalogs()


    def get_item_id(self, item_type, item_id):
        if item_type =='form':
            url = self.api_url.form['get_form_id']['url'] + str(item_id)
            method = self.api_url.form['get_form_id']['method']
        if item_type =='catalog':
            url = self.api_url['catalog']['get_catalog_id']['url'] + str(item_id)
            method = self.api_url['catalog']['get_catalog_id']['method']
        response = self.network.dispatch(url=url, method=method)
        return response


    def get_all_forms(self):
        #TODO UPDATE SELF.ITESM
        #recives the url name on the config file,GET_FORMS or GET_CATALOGS
        items = []
        all_items = self.network.dispatch(self.api_url.form['all_forms'])
        objects = all_items['data']
        for obj in objects:
            if obj['itype'] == 'form':# or obj['itype'] == 'catalog':
                    items.append(obj)
        return items


    def get_all_catalogs(self):
        #TODO UPDATE SELF.ITESM
        #recives the url name on the config file,GET_FORMS or GET_CATALOGS
        items = []
        all_items = self.network.dispatch(self.api_url['catalog']['all_catalogs'])
        objects = all_items['data']
        for obj in objects:
            if obj['itype'] == 'catalog':# or obj['itype'] == 'catalog':
                    items.append(obj)
        return items


    def get_all_connections(self):
        #TODO UPDATE SELF.ITESM
        #Returns all the connections
        connections = []
        all_connections = self.network.dispatch(self.api_url['connecions']['all_connections'])
        objects = all_connections['data']
        return objects


    def get_form_connections(self, form_id):
        #TODO UPDATE SELF.ITESM
        #Returns all the connections
        connections = []
        post_json = self.api_url.get_connections_url()['form_connections']
        post_json['url'] = post_json['url'] + str(form_id)
        form_connections = self.network.dispatch(post_json)
        objects = form_connections['data']
        return objects


    def get_all_users(self):
        #TODO UPDATE SELF.ITESM
        #Returns all the connections
        connections = []
        all_users = self.network.dispatch(self.api_url['users']['all_users'])
        objects = all_users['data']
        return objects


    def get_record_answer(self, params = {}):
        if not params:
            params = {'limit':20,'offset':0}
        response = self.network.dispatch(self.api_url.record['form_answer'], params=params)
        if response['status_code'] == 200:
            return response['data']
        return False


    def assigne_user_records(self, user_id, record_id_list, send_email=False, send_push_notification=False):
        url_method = self.api_url.record['assigne_user']
        data = {'user_id': user_id, 'records': record_id_list,
                  'send_push_notification': send_push_notification,
                  'send_mail': send_email}
        response = self.network.dispatch(url_method=url_method, data=data)
        if response['status_code'] == 200:
            return response['data']
        return response


    def assigne_connection_records(self, connection_id, record_id_list, user_of_connection=False, send_email=False, send_push_notification=False):
        url_method = self.api_url.record['assigne_connection']
        data = {'connection_id': connection_id, 'records': record_id_list,
                  'send_push_notification': send_push_notification,
                  'send_mail': send_email}
        if user_of_connection:
            data['userOfConnection'] = user_of_connection
        response = self.network.dispatch(url_method=url_method, data=data)
        if response['status_code'] == 200:
            return response['data']
        return response

    def patch_multi_record(self, answers, form_id, folios=[], record_id=[]):
        if not answers or not (folios or record_id):
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
        return  self.network.dispatch(self.api_url.record['form_answer_patch_multi'], data=data)

    def post_upload_file(self, data, up_file):
        #data:
        #up_file:
        upload_url = self.network.dispatch(self.api_url.form['upload_file'], data=data, up_file=up_file)
        return upload_url


    def patch_record(self, data, record_id=None):
        #If no record_id is send, it is asuemed that the record_id
        #all ready comes inside the data dictionary
        if record_id:
            data['_id'] = record_id
        return self.network.patch_forms_answers(data)


    def patch_record_list(self, data):
        #If no record_id is send, it is asuemed that the record_id
        #all ready comes inside the data dictionary
        return self.network.patch_forms_answers_list(data)


    def post_forms_answers(self, answers, test=False):
        return self.network.post_forms_answers(answers)


    def post_forms_answers_list(self, answers, test=False):
        return self.network.post_forms_answers_list(answers)


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
        if answer:
            try:
                if not element.has_key('field_type') or not element.has_key('field_id'):
                    raise ValueError('element should have the keys field_type and field_id')
                if element['field_type'] in ('text', 'textarea', 'email', 'password'):
                    return {element['field_id']:str(answer)}
                if element['field_type'] in ('select-one', 'radio', 'select'):
                    answer = self.make_infosync_select_json(answer, element, best_effort)
                    if answer:
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


def warning(*objs):
    '''
    To print stuff at stderr
    '''
    output = "warning:%s\n" % objs
    stderr.write(output)
