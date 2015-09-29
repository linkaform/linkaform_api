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

    

class Trap:
    OUTDOOR = 1
    INDOOR = 2
    UV = 3
    PHEROMONE = 4
    OTHERS = 5

    def get_type_of_trap(self, field_names):
        traps = {
            'ext': self.OUTDOOR,
            'int' : self.INDOOR,
            'luz' : self.UV,
            'fer' : self.PHEROMONE,
            'otra' : self.OTHERS
        }
        for key_trap, value_trap in traps.iteritems():
            for field_name in field_names:          
                if key_trap in field_name:
                    return value_trap
        return -1

        
class FormTrap(Form):
    DEFAULT_FORM_ID = 4535
    
    def __init__(self, **kwargs):        
        super(FormTrap, self).__init__(**kwargs)
        if self.form_id is None:
            self.form_id = self.DEFAULT_FORM_ID
        

    def __str__():
        return super(FormTrap, self).__str__()
    
    def get_form(self):
        return self.clean_file_structure({
            "form_id" : self.form_id,
            "geolocation" : self.geolocation,
            "start_timestamp" : self.start_timestamp,
            "end_timestamp" : self.end_timestamp,
            "answers" : self.get_answers(),
            "created_at" : self.convert_to_epoch(self.created_at),
        })
    
    def get_answers(self):
        answer_keys = self.answers.keys()
        
        if self.created_at is None:
            try:
                self.created_at = self.get_answer_for_field_id(answer_keys, self.answers, 'fecha_creacion', '')
            except:
                self.created_at = ''
                
        if self.form_id is None:        
            self.form_id = self.get_answer_for_field_id(answer_keys, self.answers, 'form_id', 'int')

            
        fields_configuration, fields_definition = self.get_variables_definition(Trap().get_type_of_trap(answer_keys))
        answers = {}
        
        
        for field_form_file, field_form_collection in fields_definition.iteritems():
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
            else:
                raise TypeError("Error to parse a multiple field")
                pass
            
        if (fields_configuration[0] == FieldsType.REPETITIVE_FIELDS):
            answers_repetitive = dict()
            answers_repetitive[fields_configuration[1]] = [answers]
            answers_repetitive["55e85d9f23d3fd0ca23d790a"] = self.convert_to_sting_date(self.created_at)
            answers_repetitive["55e85d9f23d3fd0ca23d7946"] = "17:00:00"
            answers_repetitive["55ee0b3423d3fd6d681b4740"] = self.get_answer_for_field_id(answer_keys, self.answers, 'nombre_cliente', '55ee0b3423d3fd6d681b4740')            
            return answers_repetitive
        else:
            return answers

        
    def get_variables_definition(self, trap_type):
        trap_types =  {
            Trap.OUTDOOR : [(FieldsType.REPETITIVE_FIELDS, '55e85d9f23d3fd0ca23d7918'),
                            {
                                'tipo_dispositivo_ext' : (FieldType.ONE_FIELD, '55e85d9f23d3fd0ca23d7919', ''),
                                'numero_dispositivo_ext' : (FieldType.ONE_FIELD, '55e85d9f23d3fd0ca23d791a', 'int'),
                                'condicion_dispositivo_ext' : (FieldType.GROUP_FIELD, '55e85d9f23d3fd0ca23d791b', ''),
                                'accion_realizada_ext' : (FieldType.GROUP_FIELD, '55e85d9f23d3fd0ca23d791d', ''),
                                'rata_ext' : (FieldType.ONE_FIELD, '55e881dc23d3fd0ca0bdde64', 'int'),
                                'raton_ext' : (FieldType.ONE_FIELD, '55e881dc23d3fd0ca0bdde65', 'int'),
                                'cucaracha_alemana_ext' : (FieldType.ONE_FIELD, '55e881dc23d3fd0ca0bdde66', 'int'),
                                'cucaracha_americana_ext' : (FieldType.ONE_FIELD, '55e881dc23d3fd0ca0bdde67', 'int'),
                                'hormiga_ext' : (FieldType.ONE_FIELD, '55e881dc23d3fd0ca0bdde68', 'int'),
                                'mosca_ext' : (FieldType.ONE_FIELD, '55e881dc23d3fd0ca0bdde69', 'int'),
                                'palomilla_ext' : (FieldType.ONE_FIELD, '55e8bf7323d3fd685b7ff0cf', 'int'),
                                'gorgojo_ext' : (FieldType.ONE_FIELD, '55e8bf7323d3fd685b7ff0d0', 'int'),
                                'otra_ext' : (FieldType.ONE_FIELD, '55ee015723d3fd65cb47fbe2', 'int'),
                                'descripcion_otra_ext' : (FieldType.ONE_FIELD, '55eef43f23d3fd6d6a65d4da', '')
                            }],            
            Trap.INDOOR : [ (FieldsType.REPETITIVE_FIELDS, '55e85d9f23d3fd0ca23d791f'),
                            {
                                'tipo_dispositivo_int' : (FieldType.ONE_FIELD, '55e85d9f23d3fd0ca23d7920', ''),
                                'numero_dispositivos_int' : (FieldType.ONE_FIELD, '55e85d9f23d3fd0ca23d7921', 'int'),
                                'condicion_dispositivo_int' : (FieldType.GROUP_FIELD, '55e85d9f23d3fd0ca23d7922', ''),
                                'accion_realizada_int' : (FieldType.GROUP_FIELD, '55e85d9f23d3fd0ca23d7924', ''),
                                'rata_int' : (FieldType.ONE_FIELD, '55e85d9f23d3fd0ca23d7925', 'int'),
                                'raton_int' : (FieldType.ONE_FIELD, '55e8875323d3fd0ca1472827', 'int'),
                                'cucaracha_alemana_int' : (FieldType.ONE_FIELD, '55e8875323d3fd0ca1472828', 'int'),
                                'cucaracha_americana_int' : (FieldType.ONE_FIELD, '55e8875323d3fd0ca1472829', 'int'),
                                'hormiga_int' : (FieldType.ONE_FIELD, '55e889ea23d3fd0ca0bdde72', 'int'),
                                'mosca_int' : (FieldType.ONE_FIELD, '55e8875323d3fd0ca147282a', 'int'),
                                'palomilla_int' : (FieldType.ONE_FIELD, '55e8bfe923d3fd685de86e35', 'int'),
                                'gorgojo_int' : (FieldType.ONE_FIELD, '55e8bfe923d3fd685de86e36', 'int'),
                                'otra_int' : (FieldType.ONE_FIELD, '55ee065b23d3fd6d6a65d45d', 'int'),
                                'descripcion_otra_int' : (FieldType.ONE_FIELD, '55eef47523d3fd6d69400649', '')
                            }],
            Trap.UV : [ (FieldsType.REPETITIVE_FIELDS, '55e85d9f23d3fd0ca23d7926'),
                        {
                            'tipo_dispositivo_luz' : (FieldType.ONE_FIELD, '55e85d9f23d3fd0ca23d7927', ''),
                            'numero_dispositivo_luz' : (FieldType.ONE_FIELD, '55e85d9f23d3fd0ca23d7928', 'int'),
                            'condicion_dispositivo_luz' : (FieldType.GROUP_FIELD, '55e85d9f23d3fd0ca23d7929', ''),
                            'accion_realizada_luz' : (FieldType.GROUP_FIELD, '55e85d9f23d3fd0ca23d792b', ''),
                            'mosca_luz' : (FieldType.ONE_FIELD, '55e88ab323d3fd0ca23d79d8', 'int'),
                            'mosca_fruta_luz' : (FieldType.ONE_FIELD, '55e88ab323d3fd0ca23d79d6', 'int'),
                            'mosquita_drenaje_luz' : (FieldType.ONE_FIELD, '55e8cc0223d3fd685de86e53', 'int'),
                            'mosquito_luz' : (FieldType.ONE_FIELD, '55e88ab323d3fd0ca23d79d9', 'int'),
                            'gorgojo_luz' : (FieldType.ONE_FIELD, '55e88ab323d3fd0ca23d79da', 'int'),
                            'palomilla_luz' : (FieldType.ONE_FIELD, '55e8c14f23d3fd685de86e37', 'int'),
                            'termita_luz' : (FieldType.ONE_FIELD, '55e88ab323d3fd0ca23d79db', 'int'),
                            'hormiga_luz' : (FieldType.ONE_FIELD, '55e88ab323d3fd0ca23d79d7', 'int'),
                            'otra_luz' : (FieldType.ONE_FIELD, '55ee06bf23d3fd6d6a65d460', 'int'),
                            'descripcion_otra_luz' : (FieldType.ONE_FIELD, '55eef4a823d3fd6d6a65d4db', '')
                        }],
            Trap.PHEROMONE : [(FieldsType.REPETITIVE_FIELDS, '55e85d9f23d3fd0ca23d792d'),
                              {
                                  'tipo_dispositivo_fer' : (FieldType.ONE_FIELD, '55e85d9f23d3fd0ca23d792e', ''),
                                  'numero_dispositivo_fer' : (FieldType.ONE_FIELD, '55e85d9f23d3fd0ca23d792f', 'int'),
                                  'condicion_dispositivo_fer' : (FieldType.GROUP_FIELD, '55e85d9f23d3fd0ca23d7930', ''),
                                  'accion_dispositivo_fer' : (FieldType.GROUP_FIELD, '55e85d9f23d3fd0ca23d7932', ''),
                                  'cucaracha_alemana_fer' : (FieldType.ONE_FIELD, '55e88c1123d3fd0ca147282d', 'int'),
                                  'gorgojo_fer' : (FieldType.ONE_FIELD, '55e88c1123d3fd0ca1472830', 'int'),
                                  'palomilla_fer' : (FieldType.ONE_FIELD, '55e88c1123d3fd0ca147282e', 'int'),
                                  'mosca_fer' : (FieldType.ONE_FIELD, '55e88c1123d3fd0ca147282f', 'int'),
                                  'otra_fer' : (FieldType.ONE_FIELD, '55e8c2ce23d3fd685de86e38', 'int'),
                                  'descripcion_otra_fer' : (FieldType.ONE_FIELD, '55e8c2ce23d3fd685de86e39', '')
                              }],
            
            Trap.OTHERS : [(FieldsType.REPETITIVE_FIELDS, '55e85d9f23d3fd0ca23d7934'),
                           {
                               'tipo_dispositivo_otra' : (FieldType.ONE_FIELD, '55e85d9f23d3fd0ca23d7935', ''),
                               'numero_dispositivo_otra' : (FieldType.ONE_FIELD, '55e85d9f23d3fd0ca23d7936', 'int'),
                               'condicion_dispositivo_otra' : (FieldType.GROUP_FIELD, '55e85d9f23d3fd0ca23d7937', ''),
                               'accion_dispositivo_otra' : (FieldType.GROUP_FIELD, '55e85d9f23d3fd0ca23d7939', ''),
                               'cantidad_plaga_encontrada_otra' : (FieldType.ONE_FIELD, '55e8c39e23d3fd685cc98b12', 'int'),
                               'descripcion_plaga_encontrada_otra' : (FieldType.ONE_FIELD, '55ee084c23d3fd6d6940061f', '')
                           }]
        }
        return trap_types[trap_type]

class FormAreaDevice(Form):
    DEFAULT_FORM_ID = 4536
    
    def __init__(self, **kwargs):
        super(FormAreaDevice, self).__init__(**kwargs)
        if self.form_id is None:
                    self.form_id = self.DEFAULT_FORM_ID


    def get_form(self):
        return self.clean_file_structure({
            "form_id" : self.form_id,
            "geolocation" : self.geolocation,
            "start_timestamp" : self.start_timestamp,
            "end_timestamp" : self.end_timestamp,
            "answers" : self.get_answers(),
            "created_at" : self.convert_to_epoch(self.created_at), #do not change 'created at' order, it affects the result            
        })

    def get_answers(self):
        answer_keys = self.answers.keys()

        if self.created_at is None:
            try:
                self.created_at = self.get_answer_for_field_id(answer_keys, self.answers, 'fecha_creacion', '')
            except:
                self.created_at = ''

        if self.form_id is None:
            self.form_id = self.get_answer_for_field_id(answer_keys, self.answers, 'form_id', 'int')
        
        fields = self.get_variables_definition()
        answers = {}            
        for field_form_file, field_form_collection in fields.iteritems():
            if field_form_collection[0][0] == FieldType.ONE_FIELD:
                answers[field_form_collection[0][1]] = self.get_answer_for_field_id(answer_keys, self.answers, field_form_file, field_form_collection[0][2])
            elif field_form_collection[0][0] == FieldsType.REPETITIVE_FIELDS:
                answers_aux = dict()
                print field_form_collection                
                for f_field_form_file, f_field_form_collection in field_form_collection[1].iteritems():
                    answers_aux[f_field_form_collection[1]] = self.get_answer_for_field_id(answer_keys, self.answers, f_field_form_file, f_field_form_collection[2])
                answers[field_form_collection[0][1]] = [answers_aux]
        return answers

    def get_variables_definition(self):
        '''
        Return dictionary where key is the defined field and
        the value is an array of the field id and type (empty means string)
        '''
        return {
            'numero_cliente':[(FieldType.ONE_FIELD,'55e8768e23d3fd0ca23d79b9','')],
            'nombre_cliente':[(FieldType.ONE_FIELD,'55eefe6923d3fd6d681b475a','')],
            'sucursal':[(FieldType.ONE_FIELD,'55eefe6923d3fd6d681b475b','int')],
            'fecha_instalacion':[(FieldType.ONE_FIELD,'55e8768e23d3fd0ca23d79ba','')],
            'dispositivo':[(FieldsType.REPETITIVE_FIELDS,'55e8d30d23d3fd685de86e5f'), {
                'area_instalacion':(FieldType.ONE_FIELD,'55e9b6c723d3fd685de86e76','int'),
                'frecuencia_servicio':(FieldType.ONE_FIELD,'55e9b6c723d3fd685de86e77','int'),
                'tipo_dispositivo':(FieldType.ONE_FIELD,'55e9b6c723d3fd685de86e78','int'),
                'numero_dispositivo':(FieldType.ONE_FIELD,'55e9b6c723d3fd685de86e79','int')
            }],
            'tecnico_instala':[(FieldType.ONE_FIELD,'55e87e4823d3fd0ca23d79ca','int')],
            'responsable_empresa':[(FieldType.ONE_FIELD,'55e87e4823d3fd0ca23d79cb','int')],
            'firma_responsable':[(FieldType.ONE_FIELD,'55e87e4823d3fd0ca23d79cc','int')]        
        }

class FormClient(Form):
    DEFAULT_FORM_ID = 4534
    
    def __init__(self, **kwargs):
        super(FormClient, self).__init__(**kwargs)
        if self.form_id is None:
            self.form_id = self.DEFAULT_FORM_ID
        

    def get_form(self):
        return self.clean_file_structure({
            "form_id" : self.form_id,
            "geolocation" : self.geolocation,
            "start_timestamp" : self.start_timestamp,
            "end_timestamp" : self.end_timestamp,          
            "answers" : self.get_answers(),
            "created_at" : self.convert_to_epoch(self.created_at), #do not change 'created at' order, it affects the result                        
        })

    def get_answers(self):
        answer_keys = self.answers.keys()

        if self.created_at is None:
            try:
                self.created_at = self.get_answer_for_field_id(answer_keys, self.answers, 'fecha_creacion', '')
            except:
                self.created_at = ''

        if self.form_id is None:
            self.form_id = self.get_answer_for_field_id(answer_keys, self.answers, 'form_id', 'int')

        fields = self.get_variables_definition()
        answers_to_export = {}
        for field_form_file, field_form_collection in fields.iteritems():
            answers_to_export[field_form_collection[1]] = self.get_answer_for_field_id(answer_keys, self.answers, field_form_file, field_form_collection[2])
        return answers_to_export

    def get_variables_definition(self):
        '''
        Return dictionary where key is the defined field and
        the value is an array of the field id and type (empty means string)
        '''
        return {
            'numero_cliente':(FieldType.ONE_FIELD, '55e85d9723d3fd0ca1472801', 'int'),
            'nombre_comercial':(FieldType.ONE_FIELD, '55e85d9723d3fd0ca1472802', ''),
            'nombre_cliente':(FieldType.ONE_FIELD, '55e85d9723d3fd0ca1472803', ''),
            'registro_federal_contribuyentes':(FieldType.ONE_FIELD, '55e85d9723d3fd0ca1472804', ''),
            'calle':(FieldType.ONE_FIELD, '55e85d9723d3fd0ca1472805', ''),
            'numero':(FieldType.ONE_FIELD, '55e85d9723d3fd0ca1472806', 'int'),
            'colonia':(FieldType.ONE_FIELD, '55e85d9723d3fd0ca1472807', ''),
            'municipio':(FieldType.ONE_FIELD, '55e85d9723d3fd0ca1472808', ''),
            'estado':(FieldType.ONE_FIELD, '55e85d9723d3fd0ca1472809', ''),
            'pais':(FieldType.ONE_FIELD, '55e85d9723d3fd0ca147280a', ''),
            'codigo_postal':(FieldType.ONE_FIELD, '55e85d9723d3fd0ca147280b', ''),
            'telefono':(FieldType.ONE_FIELD, '55e85d9723d3fd0ca147280c', 'int'),
            'contacto':(FieldType.ONE_FIELD, '55e85d9723d3fd0ca147280d', ''),
            'correo_electronico':(FieldType.ONE_FIELD, '55e85d9723d3fd0ca147280e', '')
        }
        
    
def warning(*objs):
    '''
    To print stuff at stderr
    '''
    output = "warning:%s\n" % objs
    stderr.write(output)


def get_form_model_from_filename(filename):
    file_name = file_path.split('/').pop()
    form_keys = FILENAME_FORM_MAP.keys()
    for form_key in form_keys:
        if form_key in file_name:
            return FILENAME_FORM_MAP[form_key]
    return -1

def load_answers(metadata, file_path):
    load_file = get_file_to_import(file_path)
    answers = []
    for answer_line in load_file:
        form = get_form_model_from_filename(file_path)(
            **{
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
USERNAME = 'solucionpc@infosync.mx'
PASS = 'infosync'

#4534 - Clients
#4535 - Traps
#4536 - Devices
FORMS_TO_PASS = [4534, 4535, 4536]


KEYS_POSITION = {}

FILE_PATH_DIR = '/var/tmp/spc/'

FILENAME_FORM_MAP = {
    'trampa' : FormTrap,
    'dispositivos': FormAreaDevice,
    'clientes': FormClient    
}

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
            if len(answers) > 0:
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
