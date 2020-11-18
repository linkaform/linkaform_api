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

from .urls import api_url
import network
#from utils import Cache
import utils
import settings
from catalog import Catalog

class FieldType:
    GROUP_FIELD = 1
    ONE_FIELD = 2
    NON_REPETITIVE_FIELDS = 3
    REPETITIVE_FIELDS = 4
    CATALOG = 5

class Item(object):

    def __init__(self, **kwargs):
        self.all_forms = self.get_all_items('form')
        self.all_catalogs = self.get_all_items('catalog')
        self.form_id = self.get_item_id_from_file(kwargs['file_name'], 'form')
        self.catalog_id = self.get_item_id_from_file(kwargs['file_name'], 'catalog')
        self.geolocation = kwargs["geolocation"]
        self.start_timestamp = kwargs["start_timestamp"]
        self.end_timestamp = kwargs["start_timestamp"]
        #self.created_at = kwargs["created_at"]
        #self.answers = kwargs["answers"]
        #self.is_catalog =  kwargs["is_catalog"]
        self.catalog = Catalog()

    def get_all_items(self, itype):
        items = settings.cache.get_all_items(itype)
        res = []
        if not items:
            items = []
        for item in items:
            res.append({'id': item['id'], 'name':item['name'], 'type':item['itype']})
        return res

    def get_item_id_from_file(self, file_path, item_type=False):
        #print('self, tendra ya todas las formsa', self.all_forms)
        filename = file_path.strip(settings.config['FILE_PATH_DIR']).split('.')[0]
        item_id = False
        if item_type == 'form' or not item_type:
            for form in self.all_forms:
                if filename == form['name']:
                    print('==================================================')
                    item_id = form['id']
                    return item_id
        if item_type == 'catalog' or not item_type:
            for form in self.all_catalogs:
                if filename == form['name']:
                    print('##################catalog', form['id'])
                    item_id = form['id']
                    return item_id
        if not item_id and not item_type:
            raise ValueError("invalid filename! %s" (filename))
        return item_id

    def get_variables_definition(self):
        fields_list = []
        print('self catalog id', self.catalog_id)
        print('self form id', self.form_id)
        if self.form_id:
        #revisar porque get items fields no regresa los campos de la forma
            fields = settings.cache.get_item_fields('form', self.form_id)
            print('fields', fields)
        if self.catalog_id:
            fields = settings.cache.get_item_fields('catalog', self.catalog_id)
        if fields:
            for field in fields[0]['fields']:
                fields_list.append(self.prepare_field_definitin(field))
        print('fields_list' ,fields_list)
        return fields_list

    def prepare_field_definitin(self, field):
        field_dir = {}
        fields_type = 2
        if field['field_type'] == 'group' or field.get('group') and field['group'].get('group_id'):
            fields_type = 1
        field_dir[field['label']] = (fields_type, field['field_id'], field['field_type'])
        return field_dir

    def get_answer_for_field_id(self, answers_key, answer, field_id, field_type=''):
        '''
        Get the answer of a field id; given a list of the posible answers, the answer and the field
        '''
        records = list()
        for ids in answers_key:
            #ids = ids.replace(' ', '')
            if field_id == ids:
                records.append(ids)
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
                if answer[records[0]]:
                    catalog_answer = self.catalog.get_catalog_realation_answer(records[0], answer)
                    return [catalog_answer,]
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

    def get_answers(self, answer_line):
        answer_keys = answer_line.keys() #self.answers.keys()
        try:
            self.created_at = self.get_answer_for_field_id(answer_keys, answer_line, 'fecha_creacion', '')
        except:
            self.created_at = ''
        ret = self.recursive_extraction_answers(self.get_variables_definition(), answer_line)
        return ret

    def recursive_extraction_answers(self, configuration, answer_line):
        answers = {}
        answer_keys = answer_line.keys()
        print('.')
        for item in configuration:
            settings.GLOBAL_VAR['count'] += 1
            if isinstance(item, dict):
                for field_form_file, field_form_collection in item.iteritems():
                    if field_form_collection[0] == FieldType.ONE_FIELD:
                        result = self.get_answer_for_field_id(answer_keys, answer_line, field_form_file, field_form_collection[2])
                        if field_form_collection[2] == 'int' and result == '':
                            result = 0
                        if field_form_collection[0] == FieldType.CATALOG and result:
                            result = {'data':result}
                        answers[field_form_collection[1]] = result
                        #print('asi va quedando answers')
                        #print('one line answers=',answers)
                    elif field_form_collection[0] == FieldType.GROUP_FIELD:
                        try:
                            answers_in_group = field_form_file.split(',')
                            answers_list_group = list()
                            for answer in answers_in_group:
                                answers_list_group.append(self.get_answer_for_field_id(answer_keys, self.answers, field_form_file, field_form_collection[2]))
                            answers[field_form_collection[1]] = answers_list_group
                        except:
                            raise TypeError("Error to parse a multiple field")
                    elif field_form_collection[0] ==  FieldsType.REPETITIVE_FIELDS:
                        answers[field_form_collection[1]] = [self.recursive_extraction_answers(field_form_collection, answer_keys)]
                    else:
                        raise TypeError("Error to parse configuration")
        return answers



class Form(Item):

    '''
    Base class of Form take as argument an object with metadata values and answers
    '''

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
            #"created_at" : self.created_at,
            #"answers" : self.answers
        }

    def get_form_data(self, form_id):
        form_data = settings.cache.get('form', form_id)
        form_more_data = settings.cache.get_data('form', form_id)
        return True

# class Catalog(Item):
#
#     '''
#     Base class of Form take as argument an object with metadata values and answers
#     '''
#
#     def __str__(self):
#         return "------------\nProperties of Catalog\Catalog ID: {0}\nANSWERS: {1}\n-------------".\
#         format(self.catalog_id, self.answers)
#
#     def get_catalog(self):
#         '''
#         Get the values of the object Catalog as a dictionary
#         '''
#         return {
#             "catalog_id" : self.catalog_id,
#         }
#
#     def get_catalog_data(self, catalog_id):
#         catalog_data = settings.cache.get('catalog', catalog_id)
#         print('catalog_data', catalog_data)
#         form_more_data = settings.cache.get_data('catalog', catalog_id)
#         print('more data', form_more_data)
#         return True
