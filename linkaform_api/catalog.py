# coding: utf-8
#!/usr/bin/python


from .urls import api_url
import network
#from utils import Cache
import utils
import settings


class Catalog(object):

    '''
    Base class of Catalog take as argument an object with metadata values and answers
    '''
    def __init__(self, **kwargs):
        #self.is_catalog =  kwargs["is_catalog"]
        self.all_catalogs = settings.cache.get_all_items('catalog')
        #self.cagalog_id =
        #self.catalog_answers = {} #self.cahce.get_data('catalog')

    def get_catalog_id(self, catalog_name):
        for item in self.all_catalogs:
            if item['name'] == catalog_name:
                return item['id']
        return False

    def transform_to_catalog_answer(self, answer_json):
        if self.is_catalog:
            answer_json['catalog_id'] = answer_json['form_id']
            answer_json.pop('form_id')
            answer_json.pop('geolocation')
        return answer_json

    def get_catalog(self, catalog_id):
        response = settings.cache.get('catalog', catalog_id)
        if response['status_code'] == 200:
            catalog = response['data'][0]
        else:
            #ValueError("LOAD_DATA_USING {0} is invalid".format(config['LOAD_DATA_USING']))
            raise ValueError("Cant get catalog id %s"%(catalog_id))
        return catalog

    def get_catalog_key_field(self, catalog_id):
        if not catalog_id:
            raise TypeError("Catalog ID is required to proceed!!! Given %s"%catalog_id)
        catalog = self.get_catalog(catalog_id)
        return catalog['key']

    def get_catalog_realation_answer(self, catalog_name, answer):
        result = {}
        data = []
        catalog_id = self.get_catalog_id(catalog_name)
        key_field = self.get_catalog_key_field(catalog_id)
        key = 'answers.%s'%(key_field['field_id'])
        get_relation_answer = self.get_answer_object_id(catalog_id, answer[catalog_name])
        if get_relation_answer:
            return get_relation_answer
        return {}


    def get_answer_object_id(self, catalog_id, key):
        catalog_data = settings.cache.get_data('catalog', catalog_id)
        for answer in catalog_data:
            if unicode(key, 'utf-8') == answer['key']:
                return {'id':answer['id'], 'key':key}
        return False
