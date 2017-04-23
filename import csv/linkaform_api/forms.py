# coding: utf-8
#!/usr/bin/python

# import time
# import requests
# import simplejson
# import os, re
#
# from pymongo import MongoClient
# from pymongo.collection import Collection
# from datetime import datetime
# from sys import stderr, argv
#
# from re import findall

class Form(object):

    '''
    Base class of Form take as argument an object with metadata values and answers
    '''
    def __init__(self, **kwargs):

        self.form_id = kwargs["form_id"]
        self.geolocation = kwargs["geolocation"]
        self.start_timestamp = kwargs["start_timestamp"]
        self.end_timestamp = kwargs["start_timestamp"]
        self.created_at = kwargs["created_at"]
        self.answers = kwargs["answers"]
        self.is_catalog =  kwargs["is_catalog"]
        self.all_catalogs = self.get_all_forms('GET_CATALOGS')

    def __str__(self):
        return "------------\nProperties of Form\nFORM ID: {0}\nGEOLOCATION: {1}\nSTART\
        TIMESTAMP: {2}\nEND TIMESTAMP: {3}\nCREATED AT: {4}\nANSWERS: {5}\n-------------".\
        format(self.form_id, self.geolocation, self.start_timestamp, self.end_timestamp, self.created_at, self.answers)

    def get_form(self):
        '''
        Get the values of the object Form as a dictionary
        '''
        return {
            "form_id" : self.form_id,
            "geolocation" : self.geolocation,
            "start_timestamp" : self.start_timestamp,
            "end_timestamp" : self.end_timestamp,
            "created_at" : self.created_at,
            "answers" : self.answers
        }

    @staticmethod
    def get_all_forms(item_type='GET_FORMS'):
        #recives the url name on the config file,GET_FORMS or GET_CATALOGS
        items_ids = []
        session = requests.Session()
        url = config[item_type]
        if config['IS_USING_APIKEY']:
            r = session.get(url, headers={'Content-type': 'application/json', 'Authorization':'ApiKey {0}:{1}'.format(config['AUTHORIZATION_EMAIL_VALUE'], config['AUTHORIZATION_TOKEN_VALUE'])}, verify=False)
        if login(session, config['USERNAME'], config['PASS']):
            print "User logged in.",url
            r = session.get(url, headers={'Content-type': 'application/json'}, verify=False)
        if r.status_code == 200:
            response = simplejson.loads(r.content)
            objects = response['objects']
            for obj in objects:
                print 'obj', obj['itype']
                if obj['itype'] == 'form' or obj['itype'] == 'catalog':
                        items_ids.append(obj['id'])
        items_ids.append({'name':'Tipo Asentamiento', 'id':1880})
        items_ids.append({'name':'Municipio Sepomex', 'id':1878})
        items_ids.append({'name':'Estado Sepomex', 'id':1882})
        items_ids.append({'name':'Ciudad', 'id':1881})
        return items_ids

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
        url = config['GET_CATALOG_DATA'] + str(catalog_id)
        print 'url', url
        #catalog_json = rest_call('get', url)
        query = {'catalog_id':catalog_id}
        collection = get_collection_connection('infosync', 'catalog_data')
        print 'query', query
        res = collection.find(query)
        return res

    def get_catalog_key_field(self, catalog_id):
        if not catalog_id:
            raise TypeError("Catalog ID is required to proceed!!! Given %s"%catalog_id)
        catalog = self.get_catalog(catalog_id)
        print ' catalog', catalog.count()
        if catalog.count() != 1:
            raise TypeError("Found non or More than one catalog find")
        catalog_json = catalog.next()
        fields = catalog_json['fields']
        for field in fields:
            if field.has_key('is_key') and field['is_key']:
                return field
        return False

    def get_catalog_realation_answer(self, catalog_name, answer):
        result = {}
        data = []
        print 'answer', answer
        print 'catalog_name', catalog_name
        catalog_id = self.get_catalog_id(catalog_name)
        print 'catalog_id', catalog_id
        key_field = self.get_catalog_key_field(catalog_id)
        key = 'answers.%s'%(key_field['field_id'])
        print ' key', key
        query = {'catalog_id':catalog_id, key:answer[catalog_name]  }
        print 'query', query
        collection = get_collection_connection('infosync', 'catalog_answer')
        res = collection.find(query)
        res = res.next()
        print 'res', res
        print 'id', res['_id']
        data.append({'id':res['id'], 'key':answer[catalog_name]})
        print not_now
        catalog
        {'catalog_id':1881,'answers.56998b0641ee487a9d5595d0':"Anáhuac"}
        res = collection.find()

    def get_answer_for_field_id(self, answers_key, answer, field_id, field_type=''):
        '''
        Get the answer of a field id; given a list of the posible answers, the answer and the field
        '''
        print 'field',field_type
        records = list()
        print 'answers_key',answers_key
        for ids in answers_key:
            #ids = ids.replace(' ', '')
            if field_id == ids:
                records.append(ids)
        print 'records',records
        if len(records) == 1:
            if field_type=='int':
                try:
                    return int(answer[records[0]])
                except ValueError:
                    return 0
            elif field_type=='float':
                try:
                    return float(answer[records[0]])
                except ValueError:
                    return 0
            elif field_type=='date':
                try:
                    return self.convert_to_sting_date(answer[records[0]])
                except ValueError:
                    return answer[records[0]]
            elif field_type=='select':
                try:
                    return answer[records[0]].lower().replace(' ','_')
                except ValueError:
                    return answer[records[0]]
            elif field_type=='catalog':
                print '-----------------------------    '
                print 'catalogo field',field_type
                print 'answer',answer
                print 'record', records[0]
                print answer[records[0]]
                if answer[records[0]]:
                    catalog_answer = self.get_catalog_realation_answer(records[0], answer)
                    print fda
                return ""
            else:
                return answer[records[0]].decode("utf-8")
        else:
            return ""

    def clean_file_structure(self, file_structure):
        answers = {}
        for key in file_structure['answers']:
            if file_structure['answers'][key]:
                answers.update({key:file_structure['answers'][key]})
        file_structure['answers'] = answers
        return file_structure

    def convert_to_epoch(self, strisodate):
        strisodate2 = re.sub(' ','',strisodate)
        strisodate2 = strisodate2.split(' ')[0]
        try:
            date_object = datetime.strptime(strisodate2, '%Y-%m-%d')
        except ValueError:
            date_object = datetime.strptime(strisodate2[:8],  '%d/%m/%y')
        return int(date_object.strftime("%s"))

    def convert_to_sting_date(self, strisodate):
        strisodate2 = re.sub(' ','',strisodate)
        strisodate2 = strisodate2.split(' ')[0]
        try:
            date_object = datetime.strptime(strisodate2, '%Y-%m-%d')
        except ValueError:
            date_object = datetime.strptime(strisodate2[:8],  '%d/%m/%y')
        return date_object.strftime('%Y-%m-%d')

    def get_answers(self):
        answer_keys = self.answers.keys()
        if self.created_at is None:
            try:
                self.created_at = self.get_answer_for_field_id(answer_keys, self.answers, 'fecha_creacion', '')
            except:
                self.created_at = ''
        return self.recursive_extraction_answers(self.get_variables_definition(), answer_keys)

    def recursive_extraction_answers(self, configuration, answer_keys):
        answers = {}
        print 'configuration', configuration
        print 'answer keys', answer_keys
        print 'answer', self.answers
        for item in configuration:
            if isinstance(item, dict):
                for field_form_file, field_form_collection in item.iteritems():
                    if field_form_collection[0] == FieldType.ONE_FIELD:
                        result = self.get_answer_for_field_id(answer_keys, self.answers, field_form_file, field_form_collection[2])
                        if field_form_collection[2] == 'int' and result == '':
                            result = 0
                        answers[field_form_collection[1]] = result
                        #print 'asi va quedando answers'
                        #print 'one line answers=',answers
                    elif field_form_collection[0] == FieldType.GROUP_FIELD:
                        try:
                            answers_in_group = field_form_file.split(',')
                            answers_list_group = list()
                            for answer in answers_in_group:
                                answers_list_group.append(self.get_answer_for_field_id(answer_keys, self.answers, field_form_file, field_form_collection[2]))
                            answers[field_form_collection[1]] = answers_list_group
                        except:
                            raise TypeError("Error to parse a multiple field")
                    elif field_form_collection[0] == FieldsType.REPETITIVE_FIELDS:
                        answers[field_form_collection[1]] = [self.recursive_extraction_answers(field_form_collection, answer_keys)]
                    else:
                        raise TypeError("Error to parse configuration")
            print recursive_extraction_answers
        return answers
