# coding: utf-8
#!/usr/bin/python

import time

#from forms import Form
import network
from urls import api_url

class Cache(object):

    def __init__(self):
        self.items = {}
        self.items_data = {}
        self.items_fields = {}


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
            url = api_url['form']['form_answer']['url'] + str(item_id)
            method = api_url['form']['form_answer']['method']
        if item_type =='catalog':
            url = api_url['catalog']['catalog_answer']['url'] + str(item_id)
            method = api_url['catalog']['catalog_answer']['method']
        response = network.dispatch(url=url, method=method)
        if response['status_code'] == 200:
            return response['data']
        return False

    def get_item_fields(self, item_type, item_id):
        if item_type =='form':
            url = api_url['form']['get_form_id_fields']['url'] + str(item_id)
            method = api_url['form']['get_form_id_fields']['method']
        if item_type =='catalog':
            url = api_url['catalog']['catalog_id_fields']['url'] + str(item_id)
            method = api_url['catalog']['catalog_id_fields']['method']
        response = network.dispatch(url=url, method=method)
        if response['status_code'] == 200:
            return response['data']
        return False

    def get_form_id_fields(self, form_id):
        url = api_url['form']['get_form_id_fields']['url']+str(form_id)
        method = api_url['form']['get_form_id_fields']['method']
        response = network.dispatch(url=url, method=method, use_api_key=False)
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
            url = api_url['form']['get_form_id']['url'] + str(item_id)
            method = api_url['form']['get_form_id']['method']
        if item_type =='catalog':
            url = api_url['catalog']['get_catalog_id']['url'] + str(item_id)
            method = api_url['catalog']['get_catalog_id']['method']
        response = network.dispatch(url=url, method=method)
        return response

    def get_all_forms(self):
        #TODO UPDATE SELF.ITESM
        #recives the url name on the config file,GET_FORMS or GET_CATALOGS
        items = []
        all_items = network.dispatch(api_url['form']['all_forms'])
        objects = all_items['data']
        for obj in objects:
            if obj['itype'] == 'form':# or obj['itype'] == 'catalog':
                    items.append(obj)
        return items

    def get_all_catalogs(self):
        #TODO UPDATE SELF.ITESM
        #recives the url name on the config file,GET_FORMS or GET_CATALOGS
        items = []
        all_items = network.dispatch(api_url['catalog']['all_catalogs'])
        objects = all_items['data']
        for obj in objects:
            if obj['itype'] == 'catalog':# or obj['itype'] == 'catalog':
                    items.append(obj)
        return items

    def get_all_connections(self):
        #TODO UPDATE SELF.ITESM
        #Returns all the connections
        connections = []
        all_connections = network.dispatch(api_url['connecions']['all_connections'])
        objects = all_connections['data']
        return objects

    def get_all_users(self):
        #TODO UPDATE SELF.ITESM
        #Returns all the connections
        connections = []
        all_users = network.dispatch(api_url['users']['all_users'])
        objects = all_users['data']
        return objects


    def get_record_answer(self, params = {}):
        if not params:
            params = {'limit':20,'offset':0}
        response = network.dispatch(api_url['record']['form_answer'], params=params)
        if response['status_code'] == 200:
            return response['data']
        return False

    def post_upload_file(self, data, up_file):
        upload_url = network.dispatch(api_url['form']['upload_file'], data=data, up_file=up_file)
        return upload_url


    def patch_record(self, data, record_id):
        return network.patch_forms_answers(data, record_id)


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

    def make_infosync_json(self, answer, element):
        #answer: The answer or answer of certain field
        #element: should be the field for the answer
        #this should contain ['field_type'] and ['field_id']
        if answer:
            try:

                if not element.has_key('field_type') or not element.has_key('field_id'):
                    raise ValueError('element should have the keys field_type and field_id')
                if element['field_type'] in ('text', 'radio', 'textarea', 'email', 'password'):
                    return {element['field_id']:str(answer)}
                if element['field_type'] in ('select-one', 'radio', 'select'):
                    print 'answer++++++++++++++++++++++++++++++++++', answer
                    answer = str(answer).lower().replace(' ', '_')
                    return {element['field_id']:answer}
                if element['field_type'] in ('checkbox'):
                    return {element['field_id']:answer.split(',')}
                if element['field_type'] in ('integer'):
                    return {element['field_id']:int(answer)}
                if element['field_type'] in ('decimal','float'):
                    return {element['field_id']:float(answer)}
                if element['field_type'] in ('date'):
                    return {element['field_id']:str(answer)[:10]}
            except ValueError, e:
                #print 'error', e
                #print 'value', answer
                return {}
        return {}

def warning(*objs):
    '''
    To print stuff at stderr
    '''
    output = "warning:%s\n" % objs
    stderr.write(output)
