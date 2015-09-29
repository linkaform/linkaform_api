# coding: utf-8
#!/usr/bin/python
import time
import requests
import simplejson
import os, re

from datetime import datetime
from sys import stderr
from re import findall
from csv import reader


class FieldType:
    GROUP_FIELD = 1
    ONE_FIELD = 2

class FieldsType:
    NON_REPETITIVE_FIELDS = 3
    REPETITIVE_FIELDS = 4
    
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


    def __str__(self):
        return "------------\nProperties of Form\nFORM ID: {0}\nGEOLOCATION: {1}\nSTART TIMESTAMP: {2}\nEND TIMESTAMP: {3}\nCREATED AT: {4}\nANSWERS: {5}\n-------------".format(self.form_id, self.geolocation, self.start_timestamp, self.end_timestamp, self.created_at, self.answers)
        
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
        
    def get_answer_for_field_id(self, answers_key, answer, field_id, field_type=''):
        '''
        Get the answer of a field id; given a list of the posible answers, the answer and the field
        '''
        records = [ids for ids in answers_key if field_id in ids]
        if len(records) == 1:
            if field_type=='int':
                try:
                    return int(answer[records[0]])
                except ValueError:
                    return answer[records[0]]
            elif field_type=='float':
                try:
                    return float(answer[records[0]])
                except ValueError:
                    return answer[records[0]]
            elif field_type=='date':
                try:
                    return float(answer[records[0]])
                except ValueError:
                    return answer[records[0]]
            else:
                return answer[records[0]].decode("latin-1")
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

    
class AlimentForm(Form):

    ALIMENTO_RECIBIDO = 3015
    PESO_SEMANAL = 4627
    ALIMENTO_CONSUMO_DIARIO = 3295
    PEDIDO_ALIMENTO_SEMANAL = 2925
    VENTAS_Y_TRANSPASOS = 2754
    CERDOS_RECIBIDOS = 2760
    MORTALIDADES_MODULOS = 3288
    MORTALIDADES_SANFANDILA_A_B_C = 4706

    def __init__(self, **kwargs):        
        super(AlimentForm, self).__init__(**kwargs)
        if self.form_id is None:
            self.form_id = self.get_form_id(kwargs["file_path"])
        

    def __str__():
        return super(AlimentForm, self).__str__()
    
    def get_form(self):
        return self.clean_file_structure({
            "form_id" : self.form_id,
            "geolocation" : self.geolocation,
            "start_timestamp" : self.start_timestamp,
            "end_timestamp" : self.end_timestamp,
            "answers" : self.get_answers()
            #"created_at" : self.convert_to_epoch(self.created_at),
        })

    def get_form_id(self, filename):
        form_id_filenames_map = {
            self.ALIMENTO_RECIBIDO : 'alimento_recibido',
            self.PESO_SEMANAL : 'peso_semanal',
            self.ALIMENTO_CONSUMO_DIARIO : 'alimento_consumo_diario',            
            self.PEDIDO_ALIMENTO_SEMANAL : 'pedido_alimento_semanal',            
            self.VENTAS_Y_TRANSPASOS : 'ventas_y_transpasos',            
            self.CERDOS_RECIBIDOS : 'cerdos_recibidos',            
            self.MORTALIDADES_MODULOS : 'cerdos_recibidos',            
            self.MORTALIDADES_SANFANDILA_A_B_C : 'mortalidades_sanfandila_a_b_c'
        }        

        for key, value in form_id_filenames_map.iteritems():
            if value in filename:
                return key
        raise ValueError("invalid filename!")
    
    
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

            
                            
    
    def get_variables_definition(self):
        form_id_fields_map =  {
            self.ALIMENTO_RECIBIDO : [{
                'fecha' : (FieldType.ONE_FIELD, 'f', ''),
                'granja' : (FieldType.ONE_FIELD, 'g', ''),
                'alimento' : (FieldsType.REPETITIVE_FIELDS, 'a', {
                    'tipo_alimento' : (FieldType.ONE_FIELD, 't', ''),
                    'origen_alimento' : (FieldType.ONE_FIELD, 'o', 'int'),
                    'cantidad' : (FieldType.ONE_FIELD, 'c', 'int')
                })
            }],

            self.PESO_SEMANAL : [{
                'fecha' : (FieldType.ONE_FIELD, '', ''),
                'granja' : (FieldType.ONE_FIELD, '', ''),
                'tamaño_muestra' : (FieldType.ONE_FIELD, '', 'int'),
                'kilos_total' : (FieldType.ONE_FIELD, '', 'int')
            }],
            
            self.ALIMENTO_CONSUMO_DIARIO : [{
                'fecha' : (FieldType.ONE_FIELD, '', ''),
                'granja' : (FieldType.ONE_FIELD, '', ''),
                'alimento' : (FieldsType.REPETITIVE_FIELDS, '', {
                    'tipo_alimento' : (FieldType.ONE_FIELD, '', ''),
                    'origen_alimento' : (FieldType.ONE_FIELD, '', 'int'),
                    'cantidad' : (FieldType.ONE_FIELD, '', 'int')
                })
            }],
            
            self.PEDIDO_ALIMENTO_SEMANAL : [{
                'numero_semana_pedido' : (FieldType.ONE_FIELD, '', ''),
                'pedido_alimento' : (FieldsType.REPETITIVE_FIELDS, '', {
                    'tipo_alimento' : (FieldType.ONE_FIELD, '', ''),
                    'cantidad' : (FieldType.ONE_FIELD, '', 'int'),
                    'dia' : (FieldType.ONE_FIELD, '', ''),                    
                }),
                'granja' : (FieldType.ONE_FIELD, '', '')
            }],
            
            self.VENTAS_Y_TRANSPASOS : [{
                'fecha' : (FieldType.ONE_FIELD, '', ''),
                'granja' : (FieldType.ONE_FIELD, '', ''),                
                'tipo_movimiento' : (FieldsType.REPETITIVE_FIELDS, '', {
                    'movimiento' : (FieldType.ONE_FIELD, '', ''),
                    'traspaso_granja_destino' : (FieldType.ONE_FIELD, '', ''),
                    'cantidad' : (FieldType.ONE_FIELD, '', 'int'),
                    'kilos_totales' : (FieldType.ONE_FIELD, '', 'int'),
                    'dias_totales' : (FieldType.ONE_FIELD, '', 'int'),
                    'lote' : (FieldType.ONE_FIELD, '', ''),
                    'flujo' : (FieldType.ONE_FIELD, '', '')
                })
            }]
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
        form = AlimentForm(
            **{
                "file_path" : file_path,
                "form_id" : metadata['form_id'],
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
    r = session.post(LOGIN_URL, data = simplejson.dumps({"password": PASS, "username": USERNAME}))
    return r.status_code == 200

def post_answers(session, answers):
    POST_CORRECTLY=0
    errors_json = []
    for index, answer in enumerate(answers):
        r = session.post(FORM_ANSWER_URL, data = simplejson.dumps(answer, encoding='latin-1'), headers={'Content-type': 'application/json'}, verify=False)
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

def get_file_to_import(file_path):
    #reads the csv file and imports it
    csv_file = open(file_path, 'r')
    field_ids = csv_file.next()
    field_ids = field_ids.strip('\n')    
    field_ids = field_ids.split(',')
    answer = []
    for line in reader(csv_file):
        line_answer = {}
        for position in range(len(field_ids)):
            line_answer.update({field_ids[position].replace('\r',''):line[position].replace('\r','')})
        answer.append(line_answer)
    return answer



FORM_ANSWER_URL = "https://grover.info-sync.com/api/infosync/form_answer/"
LOGIN_URL = "http://grover.info-sync.com/api/infosync/user_admin/login/"
USERNAME = '<cliente>@infosync.mx'
PASS = '<password>'


KEYS_POSITION = {}

FILE_PATH_DIR = ''#'/var/tmp/'


if __name__ == "__main__":
    files = os.popen('ls %s' % FILE_PATH_DIR)    
    all_files = files.read().split('\n')
    for file_name in all_files:
        if file_name:
            file_path = FILE_PATH_DIR + file_name
            time_started = time.time()
            metadata = {
                'form_id' : None,
                'lat' : 25.644885499999997,
                'glong' : -100.3862645,
                'start_timestamp' : time.time(),
                'created_at' : None
            }
            answers = load_answers(metadata, file_path)
            print "Total answers: ",len(answers)
            try:
                print answers[0]
                print answers[1]
                print answers[2]
                print answers[3]
            except:
                pass
            if False:#len(answers) > 0:
                print "%s answers loaded." % len(answers)                
                session = requests.Session()
                # Log In
                if login(session, USERNAME, PASS):                    
                    print "User logged in.",
                    post_answers(session, answers, )
                else:
                    print "Invalid login."
            else:
                print "No answers loaded."


        # for field_form_file, field_form_collection in fields_definition.iteritems():
        #     if field_form_collection[0] == FieldType.ONE_FIELD:
        #         result = self.get_answer_for_field_id(answer_keys, self.answers, field_form_file, field_form_collection[2])
        #         if field_form_collection[2] == 'int' and result == '':
        #             result = 0                
        #         answers[field_form_collection[1]] = result
        #     elif field_form_collection[0] == FieldType.GROUP_FIELD:
        #         try:
        #             answers_in_group = field_form_file.split(',')
        #             answers_list_group = list()
        #             for answer in answers_in_group:
        #                 answers_list_group.append(self.get_answer_for_field_id(answer_keys, self.answers, field_form_file, field_form_collection[2]))
        #             answers[field_form_collection[1]] = answers_list_group
        #         except:
        #             raise TypeError("Error to parse a multiple field")
        #     elif field_form_collection[0] == FieldsType.REPETITIVE_FIELDS):
        #         answers_repetitive_fields = dict()
        #         for field_key, field_value in field_form_collection[2]:
        #         answers[fields_configuration[1]] = [answers]

        #     else
        #         raise TypeError("Error to parse a multiple field")            
