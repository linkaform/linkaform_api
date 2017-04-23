# coding: utf-8
#!/usr/bin/python
import time
import requests
import simplejson

FORM_ANSWER_URL = "https://grover.info-sync.com/api/infosync/form_answer/"
LOGIN_URL = "http://grover.info-sync.com/api/infosync/user_admin/login/"
USERNAME = 'josepato@infosync.mx'
PASS = '654321'
#forma alimento infosync
FORM_ID = 3222
TIME_STARTED = time.time()
KEYS_POSITION = {}
#IMPORT SANFANDILA
#Form Producción Sanfandila
#Forma Clasificadora
FORM_ID=2810
#group_fields = {'553e557d01a4de236b93927a':True, '553e557d01a4de236b93927b':True, '553e64d801a4de236987831c':True}
file_path = '/tmp/clasificadora_sanfandila.csv'
#Forma Mortandad Liebres
FORM_ID=2654
#group_fields = {'553e64d801a4de236987831c':True, '553e557d01a4de236b93927b':True}
file_path = '/tmp/mortandad_liebres_sanfandila.csv'
#Forma Mortandad Viboras
FORM_ID=2652
#group_fields = {'553e64d801a4de236987831c':True, '553e557d01a4de236b93927b':True}
file_path = '/tmp/mortandad_viboras_sanfandila.csv'

#FORMA PRODUCCION
FORM_ID = 2712
group_fields = {'5538255501a4de2369878203':True, '5538255501a4de2369878204':True}
file_path = '/tmp/beto/Produccion.csv'

#Forma de Alimentos
FORM_ID=2713
group_fields = {'5538265001a4de236b938e7c':True, '5538265001a4de236b938e7d':True}
file_path = '/tmp/beto/Alimento.csv'

#Forma Mortandad San Diego 1
FORM_ID=3398
file_path = '/tmp/beto/Mortalidad San Diego1.csv'

#Forma Mortandad San Diego 2
FORM_ID=3399
file_path = '/tmp/beto/Mortalidad San Diego2.csv'

#Forma Mortandad Palomas3
FORM_ID=2639
file_path = '/tmp/beto/Mortalidad Palomas3.csv'

#Forma Mortandad Palomas2
FORM_ID=2638
file_path = '/tmp/beto/Mortalidad Palomas2.csv'

#Forma Mortandad Palomas1
FORM_ID=2650
file_path = '/var/tmp/beto/Mortalidad Palomas1.csv'

#Forma Mortandad Huejote1
FORM_ID=3406
file_path = '/var/tmp/beto/Mortalidad Huejote1.csv'


#Forma Mortandad Huejote3
FORM_ID=3408
file_path = '/var/tmp/beto/Mortalidad Huejote3.csv'

#Forma Mortandad Huejote2
FORM_ID=3407
file_path = '/var/tmp/beto/Mortalidad Huejote2.csv'

#Forma Mortandad Ermita
FORM_ID=2667
file_path = '/var/tmp/beto/Mortalidad Ermita.csv'

metadata = { 'form_id':FORM_ID,
    'lat':25.644885499999997,
    'glong':-100.3862645,
    'start_time':time.time()}

def load_answers(metadata, file_path):
    load_file = get_file_to_import(file_path)
    answers = []
    for answer_line in load_file:
        answers.append(form_file_config_mortandad_ermita(metadata, answer_line))
    return answers

def login(session, username, password):
    r = session.post(LOGIN_URL, data = simplejson.dumps({"password": PASS, "username": USERNAME}))
    return r.status_code == 200

def post_answers(session, answers):
    POST_CORRECTLY=0
    errors_json = []
    for index, answer in enumerate(answers):
        print 'sending answer number ', index
        #print 'answer', answer
        #continue
        r = session.post(FORM_ANSWER_URL, data = simplejson.dumps(answer), headers={'Content-type': 'application/json'}, verify=False)
        print '... time ....', int(time.time() - TIME_STARTED)
        #print dsa
        if r.status_code == 201:
            print "Answer %s saved."%(index + 1)
            POST_CORRECTLY += 1
        else:
            print "Answer %s was rejected."%(index + 1)
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

def get_answer_for_field_id(answer_keys, answer, field_id):
    records = [ids for ids in answer_keys if field_id in ids]
    if len(records) == 1:
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

def form_file_config_alimento(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "answers":{
        "5538265001a4de236b938e74":get_answer_for_field_id(answer_keys, answer,'5538265001a4de236b938e74'),
        "5538265001a4de236b938e75":get_answer_for_field_id(answer_keys, answer,'5538265001a4de236b938e75'),
        "5538265001a4de236b938e7b":get_group_list(group_fields, answer, answer_keys)
        }
    }
    return file_structure

def form_file_config_produccion(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "answers":{
        "5538255501a4de23698781fb":get_answer_for_field_id(answer_keys, answer,'5538255501a4de23698781fb'),
        "5538264201a4de236b938e73":get_answer_for_field_id(answer_keys, answer,'5538264201a4de236b938e73'),
        "5538255501a4de2369878202":get_group_list(group_fields, answer, answer_keys),
        "5538255501a4de2369878205": "Respuesta Importada"
        }
    }
    return file_structure

def form_file_config_clasificadora(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "answers":{
        "553e557d01a4de236b939277":get_answer_for_field_id(answer_keys, answer,'553e557d01a4de236b939277'),
        "553e557d01a4de236b939278":get_answer_for_field_id(answer_keys, answer,'553e557d01a4de236b939278'),
        "553e557d01a4de236b939279":get_group_list(group_fields, answer, answer_keys),
        "553e557d01a4de236b93927c": "Respuesta Importada"
        }
    }
    return file_structure

def form_file_config_mortandad_liebres(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "answers":{
        "552fc75201a4de289005537b":get_answer_for_field_id(answer_keys, answer,'552fc75201a4de289005537b'),
        "552fc75201a4de289005537c":get_answer_for_field_id(answer_keys, answer,'552fc75201a4de289005537c'),
        "552fc75201a4de2890055381": get_answer_for_field_id(answer_keys, answer,'552fc75201a4de2890055381'),
        }
    }
    return file_structure

def form_file_config_mortandad_viboras(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "answers":{
        "552fc36801a4de2890055363":get_answer_for_field_id(answer_keys, answer,'552fc36801a4de2890055363'),
        "552fc36801a4de2890055364":get_answer_for_field_id(answer_keys, answer,'552fc36801a4de2890055364'),
        "552fc36801a4de2890055369":get_answer_for_field_id(answer_keys, answer,'552fc36801a4de2890055369'),
        }
    }
    return file_structure

def form_file_config_mortandad_sandiego1(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "answers":{
        "55899c9401a4de2ea94629e7":get_answer_for_field_id(answer_keys, answer,'55899c9401a4de2ea94629e7'),
        "55899c9401a4de2ea94629e8":get_answer_for_field_id(answer_keys, answer,'55899c9401a4de2ea94629e8'),
        "55899c9401a4de2ea94629ea":get_answer_for_field_id(answer_keys, answer,'55899c9401a4de2ea94629ea'),
        }
    }
    return file_structure

def form_file_config_mortandad_sandiego2(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "answers":{
        "55899ce801a4de2ea94629f4":get_answer_for_field_id(answer_keys, answer,'55899ce801a4de2ea94629f4'),
        "55899ce801a4de2ea94629f5":get_answer_for_field_id(answer_keys, answer,'55899ce801a4de2ea94629f5'),
        "55899ce801a4de2ea94629f7":get_answer_for_field_id(answer_keys, answer,'55899ce801a4de2ea94629f7'),
        }
    }
    return file_structure

def form_file_config_mortandad_palomas3(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "answers":{
        "552e89da01a4de28900552ed":get_answer_for_field_id(answer_keys, answer,'552e89da01a4de28900552ed'),
        "552e89da01a4de28900552ee":get_answer_for_field_id(answer_keys, answer,'552e89da01a4de28900552ee'),
        "552e89da01a4de28900552f3":get_answer_for_field_id(answer_keys, answer,'552e89da01a4de28900552f3'),
        }
    }
    return file_structure

def form_file_config_mortandad_palomas2(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "answers":{
        "552e89ae01a4de288eebef32":get_answer_for_field_id(answer_keys, answer,'552e89ae01a4de288eebef32'),
        "552e89ae01a4de288eebef33":get_answer_for_field_id(answer_keys, answer,'552e89ae01a4de288eebef33'),
        "552e89ae01a4de288eebef38":get_answer_for_field_id(answer_keys, answer,'552e89ae01a4de288eebef38'),
        }
    }
    return file_structure

def form_file_config_mortandad_palomas1(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "answers":{
        "552fc35b01a4de288f4275cf":get_answer_for_field_id(answer_keys, answer,'552fc35b01a4de288f4275cf'),
        "552fc35b01a4de288f4275d0":get_answer_for_field_id(answer_keys, answer,'552fc35b01a4de288f4275d0'),
        "552fc35b01a4de288f4275d5":get_answer_for_field_id(answer_keys, answer,'552fc35b01a4de288f4275d5'),
        }
    }
    return file_structure

def form_file_config_mortandad_huejote1(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "answers":{
        "5589a03701a4de7bba84fb2f":get_answer_for_field_id(answer_keys, answer,'5589a03701a4de7bba84fb2f'),
        "5589a03701a4de7bba84fb30":get_answer_for_field_id(answer_keys, answer,'5589a03701a4de7bba84fb30'),
        "5589a03701a4de7bba84fb32":get_answer_for_field_id(answer_keys, answer,'5589a03701a4de7bba84fb32'),
        }
    }
    return file_structure

def form_file_config_mortandad_huejote2(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "answers":{
        "5589a09c01a4de7bba84fb4d":get_answer_for_field_id(answer_keys, answer,'5589a09c01a4de7bba84fb4d'),
        "5589a09c01a4de7bba84fb4e":get_answer_for_field_id(answer_keys, answer,'5589a09c01a4de7bba84fb4e'),
        "5589a09c01a4de7bba84fb50":get_answer_for_field_id(answer_keys, answer,'5589a09c01a4de7bba84fb50'),
        }
    }
    return file_structure

def form_file_config_mortandad_huejote3(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "answers":{
        "5589a0bc01a4de7bba84fb55":get_answer_for_field_id(answer_keys, answer,'5589a0bc01a4de7bba84fb55'),
        "5589a0bc01a4de7bba84fb56":get_answer_for_field_id(answer_keys, answer,'5589a0bc01a4de7bba84fb56'),
        "5589a0bc01a4de7bba84fb58":get_answer_for_field_id(answer_keys, answer,'5589a0bc01a4de7bba84fb58'),
        }
    }
    return file_structure

def form_file_config_mortandad_ermita(metadata, answer):
    answer_keys = answer.keys()
    file_structure = {
    "form_id": metadata['form_id'],
    "geolocation":[metadata['lat'],metadata['glong']],
    "start_timestamp":metadata['start_time'],
    "end_timestamp":metadata['start_time'],
    "answers":{
        "552fdbf501a4de288f4275e8":get_answer_for_field_id(answer_keys, answer,'552fdbf501a4de288f4275e8'),
        "552fdbf501a4de288f4275e9":get_answer_for_field_id(answer_keys, answer,'552fdbf501a4de288f4275e9'),
        "552fdbf501a4de288f4275ee":get_answer_for_field_id(answer_keys, answer,'552fdbf501a4de288f4275ee'),
        }
    }
    return file_structure

if __name__ == "__main__":
    print "Loading answers... FORM", FORM_ID
    answers = load_answers(metadata, file_path)
    if len(answers) > 0:
        print "%s answers loaded."%len(answers)
        session = requests.Session()
        # Log In
        if login(session, USERNAME, PASS):
            print "User logged in."
            post_answers(session, answers, )
        else:
            print "Invalid login."
    else:
        print "No answers loaded."
