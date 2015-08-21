# coding: utf-8
#!/usr/bin/python
import time
import requests
import simplejson
import os
from datetime import datetime


FORM_ANSWER_URL = "https://grover.info-sync.com/api/infosync/form_answer/"
LOGIN_URL = "http://grover.info-sync.com/api/infosync/user_admin/login/"
USERNAME = 'logistorage.infosync@gmail.com'
PASS = '654321'



#forma alimento infosync
KEYS_POSITION = {}
#IMPORT SANFANDILA
#Form Producción Sanfandila
#Forma Clasificadora
file_path_dir = '/var/tmp/logistorage/Junio/'
files = os.popen('ls %s'%file_path_dir)
all_files = files.read().split('\n')


def load_answers(metadata, file_path):
    load_file = get_file_to_import(file_path)
    answers = []
    for answer_line in load_file:
        answers.append(form_file_config_control_salidas(metadata, answer_line))
    return answers

def login(session, username, password):
    r = session.post(LOGIN_URL, data = simplejson.dumps({"password": PASS, "username": USERNAME}))
    return r.status_code == 200

def post_answers(session, answers):
    POST_CORRECTLY=0
    errors_json = []
    for index, answer in enumerate(answers):
        #print 'sending answer number ', index
        #print 'answer', answer
        #continue
        r = session.post(FORM_ANSWER_URL, data = simplejson.dumps(answer), headers={'Content-type': 'application/json'}, verify=False)
        #print '... time ....', int(time.time() - TIME_STARTED)
        #print dsa
        if r.status_code == 201:
            #print "Answer %s saved."%(index + 1)
            POST_CORRECTLY += 1
        else:
            print "Answer %s was rejected."%(index + 1)
            print 'r.content', r.content
            #print 'answer=', answer
            response = simplejson.loads(r.content)
            print '----------------------------------'
            print "Response: "
            print simplejson.dumps(response, indent=4)
            errors_json.append(response)
            print '----------------------------------'
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
    for line in csv_file:
        line = line.strip('\n')
        line = line.split(',')
        line_answer = {}
        for position in range(len(field_ids)):
            line_answer.update({'%s_'%position+field_ids[position]:line[position]})
        answer.append(line_answer)
    return answer

def get_group_list(group_fields, answer, answer_keys):
    group_list = []
    set_record_order(group_fields, answer, answer_keys)
    for answer in KEYS_POSITION.values():
        pass_required = True
        group = {}
        for field_id, required in group_fields.iteritems():
            if answer.has_key(field_id) and answer[field_id]:
                group.update({field_id:answer[field_id]})
            elif required:
                pass_required = False
            else:
                continue
        if pass_required:
            group_list.append(group)
    return group_list

def get_answer_for_field_id(answer_keys, answer, field_id, field_type=''):
    records = [ids for ids in answer_keys if field_id in ids]
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
        else:
                return answer[records[0]]         
    else:
        return ""

def set_record_order(group_fields, answer, answer_keys ):
    for field_id in group_fields.keys():
        records = [ids for ids in answer_keys if field_id in ids]
        if len(records) :
            keys_position = {}
            for field in records:
                fkey, fid =field.split('_')
                keys_position.update({int(fkey):{fid:answer[field]}})
            positions = keys_position.keys()
            positions.sort()
            get_group_order_dict(positions,keys_position)
    return True

def get_group_order_dict(positions, keys_position):
    result = {}
    count = 0 
    for position_id in positions:
        result.update({count:keys_position[position_id]})
        update_key_position(count, keys_position[position_id])
        count += 1
    return True

def update_key_position(count, answer):
    if KEYS_POSITION.has_key(count):
        KEYS_POSITION[count].update(answer)
    else:
        KEYS_POSITION[count] = answer
    return True

def convert_to_epoch(strisodate):
    try:
        date_object = datetime.strptime(strisodate, '%Y-%m-%d')
    except ValueError:
        date_object = datetime.strptime(strisodate,  '%m/%d/%y')
    return int(date_object.strftime("%s"))

def form_file_config_control_salidas(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "created_at": convert_to_epoch(get_answer_for_field_id(answer_keys, answer,'created_at')),
    "answers":{
        "5591627901a4de7bb8eb1ad4":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1ad4'),
        "5591627901a4de7bb8eb1ad5":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1ad5'),
        "55917c1701a4de7bb94f87ef":get_answer_for_field_id(answer_keys, answer,'55917c1701a4de7bb94f87ef'),
        "5591627901a4de7bb8eb1ad7":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1ad7'),
        "559174f601a4de7bb94f87eb":get_answer_for_field_id(answer_keys, answer,'559174f601a4de7bb94f87eb'),
        "5591627901a4de7bb8eb1ad8":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1ad8'),
        "5591647401a4de7bb94f87d1":get_answer_for_field_id(answer_keys, answer,'5591647401a4de7bb94f87d1'),
        "5591627901a4de7bb8eb1ad9":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1ad9', 'int'),
        "559167ed01a4de7bba852991":get_answer_for_field_id(answer_keys, answer,'559167ed01a4de7bba852991', 'int'),
        "5591627901a4de7bb8eb1ada":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1ada', 'int'),
        "559167ed01a4de7bba852992":get_answer_for_field_id(answer_keys, answer,'559167ed01a4de7bba852992', 'int'),
        "5591627901a4de7bb8eb1adb":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1adb', 'int'),
        "5591627901a4de7bb8eb1adc":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1adc', 'int'),
        "559167ed01a4de7bba852993":get_answer_for_field_id(answer_keys, answer,'559167ed01a4de7bba852993', 'float'),
        "559167ed01a4de7bba852994":get_answer_for_field_id(answer_keys, answer,'559167ed01a4de7bba852994', 'int'),
        "5591627901a4de7bb8eb1add":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1add', 'float'),
        "5591627901a4de7bb8eb1ade":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1ade', 'int'),
        "55916a6f01a4de7bba852997":get_answer_for_field_id(answer_keys, answer,'55916a6f01a4de7bba852997', 'int'),
        "5591627901a4de7bb8eb1adf":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1adf', 'float'),
        "5591627901a4de7bb8eb1ae0":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1ae0', 'int'),
        "55916a6f01a4de7bba852998":get_answer_for_field_id(answer_keys, answer,'55916a6f01a4de7bba852998', 'int'),
        "55916a6f01a4de7bba852999":get_answer_for_field_id(answer_keys, answer,'55916a6f01a4de7bba852999', 'int'),
        "55916a6f01a4de7bba85299a":get_answer_for_field_id(answer_keys, answer,'55916a6f01a4de7bba85299a', 'int'),
        "55916a6f01a4de7bba85299b":get_answer_for_field_id(answer_keys, answer,'55916a6f01a4de7bba85299b', 'int'),
        "55916a6f01a4de7bba85299c":get_answer_for_field_id(answer_keys, answer,'55916a6f01a4de7bba85299c', 'int'),
        "55916a6f01a4de7bba85299d":get_answer_for_field_id(answer_keys, answer,'55916a6f01a4de7bba85299d', 'int'),
        "55916a6f01a4de7bba85299e":get_answer_for_field_id(answer_keys, answer,'55916a6f01a4de7bba85299e', 'int'),
        "55916a6f01a4de7bba85299f":get_answer_for_field_id(answer_keys, answer,'55916a6f01a4de7bba85299f', 'int'),
        "55916a6f01a4de7bba8529a0":get_answer_for_field_id(answer_keys, answer,'55916a6f01a4de7bba8529a0', 'int'),
        "5591627901a4de7bb8eb1ae1":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1ae1', 'int'),
        "5591627901a4de7bb8eb1ae2":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1ae2', 'int'),
        "55916a6f01a4de7bba8529a1":get_answer_for_field_id(answer_keys, answer,'55916a6f01a4de7bba8529a1', 'int'),
        "55916a6f01a4de7bba8529a2":get_answer_for_field_id(answer_keys, answer,'55916a6f01a4de7bba8529a2', 'int'),
        "559174f601a4de7bb94f87ec":get_answer_for_field_id(answer_keys, answer,'559174f601a4de7bb94f87ec', 'int'),
        "559174f601a4de7bb94f87ed":get_answer_for_field_id(answer_keys, answer,'559174f601a4de7bb94f87ed'),
        }
    }
    return clean_file_structure(file_structure)

def form_file_config_unidad_espacio_miller(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "created_at": convert_to_epoch(get_answer_for_field_id(answer_keys, answer,'created_at')),
    "answers":{
        "5591627901a4de7bb8eb1ad4":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1ad4'),
        "5591627901a4de7bb8eb1ad5":get_answer_for_field_id(answer_keys, answer,'5591627901a4de7bb8eb1ad5'),
        "559a966d23d3fd7010c63053":get_answer_for_field_id(answer_keys, answer,'559a966d23d3fd7010c63053'),
        "558d685701a4de7bba85289f":get_answer_for_field_id(answer_keys, answer,'558d685701a4de7bba85289f', 'float'),
        }
    }
    return clean_file_structure(file_structure)

def clean_file_structure(file_structure):
    answers = {}
    for key in file_structure['answers']:
        if file_structure['answers'][key]:
            answers.update({key:file_structure['answers'][key]})
    file_structure['answers'] = answers
    return file_structure

if __name__ == "__main__":
    for file_name in all_files:
        print '-----------------'
        if file_name:
            file_path = file_path_dir + file_name
            print 'file_path=',file_path
            TIME_STARTED = time.time()
            FORM_ID = int(file_name.split('_')[1].split('.')[0])
            metadata = { 'form_id':FORM_ID,
                'lat':25.644885499999997,
                'glong':-100.3862645, 
                'start_time':time.time()}
            print "Loading answers... FORM", FORM_ID
            answers = load_answers(metadata, file_path)
            if len(answers) > 0:
                print "%s answers loaded."%len(answers)
                session = requests.Session()
                # Log In
                if login(session, USERNAME, PASS):
                    print "User logged in.", 
                    post_answers(session, answers, )
                else:
                    print "Invalid login."
            else:
                print "No answers loaded."
