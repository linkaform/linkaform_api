# coding: utf-8
#!/usr/bin/python
import time
import requests
import simplejson
import os, re

from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime
from sys import stderr, argv

from re import findall

# ENUMS
class FieldType:
    GROUP_FIELD = 1
    ONE_FIELD = 2

class FieldsType:
    NON_REPETITIVE_FIELDS = 3
    REPETITIVE_FIELDS = 4

class ImportData:
    MONGO = 1
    REST = 2


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

    def __str__(self):
        return "------------\nProperties of Form\nFORM ID: {0}\nGEOLOCATION: {1}\nSTART\
        TIMESTAMP: {2}\nEND TIMESTAMP: {3}\nCREATED AT: {4}\nANSWERS: {5}\n-------------".\
        format(self.form_id, self.geolocation, self.start_timestamp, self.end_timestamp, self.created_at, self.answers)

    def get_form(self):
        '''
        Get the values of the object Form as a dictionary
        '''
        print ' entra a get form de clase forma'
        return {
            "form_id" : self.form_id,
            "geolocation" : self.geolocation,
            "start_timestamp" : self.start_timestamp,
            "end_timestamp" : self.end_timestamp,
            "created_at" : self.created_at,
            "answers" : self.answers
        }

    def transform_to_catalog_answer(self, answer_json):
        if self.is_catalog:
            answer_json['catalog_id'] = answer_json['form_id']
            answer_json.pop('form_id')
            answer_json.pop('geolocation')
        return answer_json


    def get_answer_for_field_id(self, answers_key, answer, field_id, field_type=''):
        '''
        Get the answer of a field id; given a list of the posible answers, the answer and the field
        '''
        records = list()
        for ids in answers_key:
            ids = ids.replace(' ', '')
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
        for item in configuration:
            if isinstance(item, dict):
                for field_form_file, field_form_collection in item.iteritems():
                    if field_form_collection[0] == FieldType.ONE_FIELD:
                        result = self.get_answer_for_field_id(answer_keys, self.answers, field_form_file, field_form_collection[2])
                        if field_form_collection[2] == 'int' and result == '':
                            result = 0
                        answers[field_form_collection[1]] = result

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
        return answers

class SanfandilaForm(Form):

    CATALOGO_MUNICIPOIO = 1878
    CATALOGO_ZONAS = 1879
    CATALOGO_TIPO_ASENTAMIENTO = 1880
    CATALOGO_CIUDAD = 1881
    CATALOGO_ESTADO = 1882
    TEST_CATALOGO = 1883
    CATALOGO_ASENTAMIENTO = 1884



    def __init__(self, **kwargs):
        super(SanfandilaForm, self).__init__(**kwargs)
        if self.form_id is None:
            self.form_id = self.get_form_id(kwargs["file_path"])

    def __str__():
        return super(SanfandilaForm, self).__str__()

    def get_form(self):
        answer_line = self.clean_file_structure({
            "form_id" : self.form_id,
            "geolocation" : self.geolocation,
            "start_timestamp" : self.start_timestamp,
            "end_timestamp" : self.end_timestamp,
            "answers" : self.get_answers()
            #"created_at" : self.convert_to_epoch(self.created_at),
        })
        return self.transform_to_catalog_answer(answer_line)

    def get_form_id(self, file_path):
        filename = file_path.strip(config['FILE_PATH_DIR']).split('.')[0]
        ### TODO match the filename to the form or catalog to import
        form_id_filenames_map = {
            self.TEST_CATALOGO: 'catalogo_CP_nuevo_leon',
            self.CATALOGO_ESTADO: 'catalogo_estado',
            self.CATALOGO_TIPO_ASENTAMIENTO: 'catalogo_tipo_asentamiento',
            self.CATALOGO_ZONAS: 'catalogo_zonas',
            self.CATALOGO_CIUDAD: 'catalogo_ciudad',
            self.CATALOGO_ASENTAMIENTO: 'catalogo_asentamiento',
            self.CATALOGO_MUNICIPOIO: 'catalogo_municipio',
        }
        # form_id_filenames_map = {
        #      self.TEST_CATALOGO: 'catalogo_CP_nuevo_leon'}

        for key, value in form_id_filenames_map.iteritems():
            if value in filename:
                return key
        raise ValueError("invalid filename!")

    def get_variables_definition(self):
        form_id_fields_map =  {
            self.CATALOGO_CIUDAD : [{
                'd_ciudad' : (FieldType.ONE_FIELD, '56998b0641ee487a9d5595d0', 'text'),
                'c_cve_ciudad' : (FieldType.ONE_FIELD, '56998b0641ee487a9d5595d1', 'text'),
            }],
            self.TEST_CATALOGO : [{
                'd_codigo' : (FieldType.ONE_FIELD, '56998b7141ee487a9d5595da', 'text')
            }],
            self.CATALOGO_ZONAS : [{
                'd_zona' : (FieldType.ONE_FIELD, '5699899841ee487a9d5595cb', 'text'),
            }],
            self.CATALOGO_TIPO_ASENTAMIENTO : [{
                'd_tipo_asenta' : (FieldType.ONE_FIELD, '569989ba41ee487a9d5595cd', 'text'),
                'c_tipo_asenta' : (FieldType.ONE_FIELD, '569989ba41ee487a9d5595ce', 'text'),
            }],
            self.CATALOGO_CIUDAD : [{
                'd_ciudad' : (FieldType.ONE_FIELD, '56998b0641ee487a9d5595d0', 'text'),
                'c_cve_ciudad' : (FieldType.ONE_FIELD, '56998b0641ee487a9d5595d1', 'text'),
            }],
            self.CATALOGO_ESTADO : [{
                'd_estado' : (FieldType.ONE_FIELD, '56998b4041ee487a9d5595d5', 'text'),
                'c_estado' : (FieldType.ONE_FIELD, '56998b4041ee487a9d5595d6', 'text'),
            }],
            self.CATALOGO_ASENTAMIENTO : [{
                'd_estado' : (FieldType.ONE_FIELD, '56998b4041ee487a9d5595d5', 'text'),
                'c_estado' : (FieldType.ONE_FIELD, '56998b4041ee487a9d5595d6', 'text'),
            }],
        }
        return form_id_fields_map[self.form_id]

def warning(*objs):
    '''
    To print stuff at stderr
    '''
    output = "warning:%s\n" % objs
    stderr.write(output)

def load_answers(metadata, file_path):
    load_file = get_file_to_import(file_path)
    answers = []
    for answer_line in load_file:
        form = SanfandilaForm(
            **{
                "file_path" : file_path,
                "form_id" : metadata['form_id'],
                "is_catalog": metadata['is_catalog'],
                "geolocation" : [metadata['lat'], metadata['glong']],
                "start_timestamp" : metadata['start_timestamp'],
                "end_timestamp" : metadata['start_timestamp'],
                "created_at" : metadata['created_at'],
                "answers" : answer_line
            }
        )
        answers.append(form.get_form())
    return answers

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

def get_file_to_import(file_path):
    answers = []
    with open(file_path) as file:
        headers = file.readline().strip().split(',')
        for line in file:
            line = line.strip().split(',')
            field_map = zip(headers, line)
            answers.append(dict(field_map))
    return answers

def file_is_catalogo(file_path):
    prefix = file_path.split('_')[0]
    if prefix == 'catalogo' or prefix == 'catalog':
        return True
    elif 'catalogo' in file_path:
        return True
    elif 'catalog' in file_path:
        return True
    else:
        return False

def get_user_connection(user_id):
    print "> Getting connection ..."
    connection = {}
    connection['client'] = MongoClient(config['HOST'], config['PORT'])
    user_db_name = "infosync_answers_client_{0}".format(user_id)
    if not user_db_name:
        return None
    connection['db'] = connection['client'][user_db_name]
    return connection

def create_collection(collection, user_connection):
    print "> Creating Collection ..."
    if config['CREATE'] and collection in user_connection['db'].collection_names():
        oldCollection = user_connection['db'][collection]
        oldCollection.drop()
    newCollection = Collection(user_connection['db'], collection, create=config['CREATE'])
    return newCollection

def upload_answers_to_database(answers):
    print "> Uploading Content ..."
    user_connection = get_user_connection(config['USER_ID'])
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


config = {
    'FORM_ANSWER_URL' : 'https://bigbird.info-sync.com/api/infosync/form_answer/',
    'CATALOG_ANSWER_URL' : 'https://bigbird.info-sync.com/api/infosync/catalog_answer/',
    'LOGIN_URL' : 'https://bigbird.info-sync.com/api/infosync/user_admin/login/',
    'USERNAME' : 'jpv@info-sync.com',
    'PASS' : '654321',
    'COLLECTION' : 'form_answer',
    'HOST' : 'localhost',
    'PORT' : 27019,
    'USER_ID' : '414',
    'KEYS_POSITION' : {},
    'FILE_PATH_DIR' : '/tmp/sempomex/',
    'IS_USING_APIKEY' : False,
    'AUTHORIZATION_EMAIL_VALUE' : 'infosync@sanfandila.com',
    'AUTHORIZATION_TOKEN_VALUE' : '530bd4396d7ffd9f6ee76aea4f621e7d00cd9e21',
    #'LOAD_DATA_USING' : ImportData.MONGO,
    'LOAD_DATA_USING' : ImportData.REST,
    'CREATE' : False
}


# Sanfandila APIKEY TOKEN
# AUTHORIZATION_EMAIL_VALUE = 'jefatura.ti@sanfandila.com'
# AUTHORIZATION_TOKEN_VALUE = 'fd390bd5e5297edf3a3fa0b759919e88a9334709'


if __name__ == "__main__":
    files = os.popen('ls %s' % config['FILE_PATH_DIR'])
    all_files = files.read().split('\n')
    try:
        test = argv[1]
    except:
        test = False
    GLOBAL_ERRORS = []
    for file_name in all_files:
        if file_name:
            file_path = config['FILE_PATH_DIR'] + file_name
            print "Filename: {0}".format(file_path)
            time_started = time.time()
            metadata = {
                'form_id' : None,
                'lat' : 25.644885499999997,
                'glong' : -100.3862645,
                'start_timestamp' : 123456789,
                'created_at' : None,
                'is_catalog': file_is_catalogo(file_path),
            }
            answers = load_answers(metadata, file_path)
            print "Total answers: ",len(answers)
            try:
                print "Sample of answers:"
                # print answers[0]
                # print answers[1]
                # print answers[2]
                # print answers[3]
            except:
                pass
            if len(answers) > 0:
                print "%s answers loaded." % len(answers)
                if config['LOAD_DATA_USING'] == ImportData.MONGO:
                    upload_answers_to_database(answers)
                elif config['LOAD_DATA_USING'] == ImportData.REST:
                    upload_answers_using_rest(answers, metadata['is_catalog'], test)
                else:
                    raise ValueError("LOAD_DATA_USING {0} is invalid".format(config['LOAD_DATA_USING']))
            else:
                 "No answers loaded."
    if test or len(GLOBAL_ERRORS):
        print '=================== TEST RESULTS ================================'
        print 'total errors', len(GLOBAL_ERRORS)
        for error in GLOBAL_ERRORS:
            print error
