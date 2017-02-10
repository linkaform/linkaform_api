#####
# Made by Jose Patricio VM
#####
# Script para generar pacos a partir de ordenes de Servicio de PCI Industrial
#
#
#####
import wget
import pyexcel
import datetime ,time

from linkaform_api import settings
from linkaform_api import network, utils

from script_get_ordenes_liquidadas import get_files2upload

mongo_hosts = 'db2.linkaform.com:27017,db3.linkaform.com:27017,db4.linkaform.com:27017'
#mongo_hosts = "127.0.0.1"
mongo_replicaSet = 'linkaform_replica'
MONGO_READPREFERENCE='primary'

MAX_POOL_SIZE = 50
WAIT_QUEUE_TIMEOUT = 1000
MONGODB_URI = 'mongodb://%s/?replicaSet=%s&readPreference=%s'%(mongo_hosts, mongo_replicaSet, MONGO_READPREFERENCE)

EXPEDIENTES = ['2220573',2220573,'2221071',2221071]

lkf_api = utils.Cache()


config = {
    'USERNAME' : 'jgemayel@pcindustrial.com.mx',
    #'USERNAME' : 'josepato@infosync.mx',
    'PASS' : '123456',
    'COLLECTION' : 'form_answer',
    #'HOST' : 'db3.linkaform.com',
    'MONGODB_URI':MONGODB_URI,
    #'MONGODB_PASSWORD': mongodb_password_here
    'PORT' : 27017,
    'USER_ID' : 1259,
    'KEYS_POSITION' : {},
    'IS_USING_APIKEY' : True,
    'AUTHORIZATION_EMAIL_VALUE' : 'jgemayel@pcindustrial.com.mx',
    'AUTHORIZATION_TOKEN_VALUE' : '5883aea4cb2aa56d690de473af0d6a5672b32709',
}


settings.config = config
cr = network.get_collections()

#Nombre del campo en la la Forma: Nombre en el Archvio
equivalcens_map = {'Clase de Servicio':['CLASE_SERV',],
                    'Fecha Contratada':['F_CONTRATA',],
                    'Estatus':['ESTATUS de Orden',],
                    'Metros Bajante':['MTS. BAJANTE (PARALELO)',],
                    'Tipo de Tarea':['TIPO TAREA'],
                    'Tipo':['TIPO'],
                    'Clase de Servicio': ['CLASE_SERV','Clase', 'Clase Servicio', 'Clase de Servicio'],
                    'Etapa': ['Etapa'],
                    'Dilacion':['Dilacion',],
                    'Folio': ['Folio','Folio Pisa','FolioPisa'],
                    'Expediente':['EXP. TEC.',],
                    'Expediente':['EXPEDIENTE',]}





def read_file(file_url):
    #sheet = pyexcel.get_sheet(file_name="bolsa.xlsx")
    sheet = pyexcel.get_sheet(url = file_url)
    records = sheet.array
    header = records.pop(0)
    header = [col.lower().replace(' ', '_') for col in header]
    return header, records


def download_file(url):
    fileb = wget.download(url)
    return fileb


def get_element_dict(field):
    return {'field_id':field['field_id'], 'field_type':field['field_type'], 'label':field['label'], 'options':field['options']}


def get_record_folio(header_dict, record):
    if 'folio' in header_dict.keys():
        folio_col = header_dict['folio']
    if 'folio_pisa' in header_dict.keys():
        folio_col = header_dict['folio_pisa']
    return record[folio_col]


########
######## Check asignations | Revisa Asignaciones
########
def get_asignacion_pci_col(header_dict):
    option_list = []
    if 'expediente' in header_dict.keys():
        option_list.append(header_dict['expediente'])
    return option_list


def query_get_expedientes():
    query = {'form_id':  11132, 'deleted_at' : {'$exists':False}}
    select_columns = {'answers.f11132000000000000000001.f111320000000000000000c2':1}
    return query, select_columns


def get_expedientes():
    query, select_columns = query_get_expedientes()
    expedientes = cr.find(query, select_columns)
    result = []
    for answer in expedientes:
        if answer.has_key('answers') and answer['answers'].has_key('f11132000000000000000001'):
            exp_list = answer['answers']['f11132000000000000000001']
            result += [ exp['f111320000000000000000c2'] for exp in exp_list]
    return result


def check_assignation(exp_cols, record):
    is_assigned = False
    expedientes = get_expedientes()
    for col in exp_cols:
        try:
            if int(record[col]) in expedientes:
                is_assigned = {True:record[col]}
            else:
                is_assigned = {False: record[col]}
        except ValueError:
            continue
    return is_assigned

#######


def make_header_dict(header):
    ### Return the directory with
    ### the column name : column number
    header_dict = {}
    for position in range(len(header)):
        header_dict[str(header[position]).lower().replace(' ' ,'_')] = position
    return header_dict


def get_pos_field_id_dict(header, form_id=10540, cope=''):
    #form_id=10378 el id de bolsa
    #pos_field_id ={3: {'field_type': 'text', 'field_id': '584648c8b43fdd7d44ae63d1'}, 9: {'field_type': 'text', 'field_id': '58464a29b43fdd773c240163'}, 51: {'field_type': 'integer', 'field_id': '584648c8b43fdd7d44ae63d0'}}
    #return pos_field_id
    pos_field_id = {}
    form_fields = lkf_api.get_form_id_fields(form_id)
    header_dict = make_header_dict(header)
    if len(form_fields) > 0:
        fields = form_fields[0]['fields']
        fields_json = {}
        ####
        #### For para obtener columnas esecificas del tipo de servicio
        ####
        for folio_key in equivalcens_map['Folio']:
            folio_key = folio_key.lower().replace(' ','_')
            if folio_key in header_dict.keys():
                pos_field_id[header_dict[folio_key]] = {'scritp_type':'folio'}
        for folio_key in equivalcens_map['Etapa']:
            folio_key = folio_key.lower().replace(' ','_')
            if folio_key in header_dict.keys():
                pos_field_id[header_dict[folio_key]] = {'scritp_type':'etapa'}
        for folio_key in equivalcens_map['Tipo']:
            folio_key = folio_key.lower().replace(' ','_')
            if folio_key in header_dict.keys():
                pos_field_id[header_dict[folio_key]] = {'scritp_type':'tipo'}
        for folio_key in equivalcens_map['Clase de Servicio']:
            folio_key = folio_key.lower().replace(' ','_')
            if folio_key in header_dict.keys():
                pos_field_id[header_dict[folio_key]] = {'scritp_type':'clase'}
        for folio_key in equivalcens_map['Tipo de Tarea']:
            folio_key = folio_key.lower().replace(' ','_')
            if folio_key in header_dict.keys():
                pos_field_id[header_dict[folio_key]] = {'scritp_type':'tipo de tarea'}
        ###
        ###
        for field in fields:
            label = field['label'].lower().replace(' ' ,'')
            label_underscore = field['label'].lower().replace(' ' ,'_')
            if label_underscore == 'cope':
                pos_field_id = update_pos_field_id(pos_field_id, position=cope, field=field)
            if label_underscore == 'clase':
                pos_field_id = update_pos_field_id(pos_field_id, position='clase', field=field, scritp_type='clase')
            if label_underscore == 'tipo':
                pos_field_id = update_pos_field_id(pos_field_id, position='tipo', field=field, scritp_type='tipo')
            if label_underscore == 'etapa':
                pos_field_id = update_pos_field_id(pos_field_id, position='etapa', field=field, scritp_type='etapa')
            if label_underscore == 'tipo_de_tarea':
                pos_field_id = update_pos_field_id(pos_field_id, position='tipo de tarea', field=field, scritp_type='tipo de tarea')
            if label in header_dict.keys():
                pos_field_id = update_pos_field_id(pos_field_id, position=header_dict[label], field=field)
            elif label_underscore in header_dict.keys():
                pos_field_id = update_pos_field_id(pos_field_id, position=header_dict[label_underscore], field=field)
                #pos_field_id[header_dict[label_underscore]].update(get_element_dict(field))
            elif field['label'] in equivalcens_map.keys():
                for eqv_label in equivalcens_map[field['label']]:
                    header_lable = eqv_label.lower().replace(' ' ,'')
                    header_lable_under = eqv_label.lower().replace(' ' ,'_')
                    if header_lable in header_dict.keys():
                        pos_field_id = update_pos_field_id(pos_field_id, position=header_dict[header_lable], field=field)
                    elif header_lable_under in header_dict.keys():
                        pos_field_id = update_pos_field_id(pos_field_id, position=header_dict[header_lable_under], field=field)
    return pos_field_id


def update_pos_field_id(pos_field_id, position, field, scritp_type=''):
    if pos_field_id.has_key(position):
        pos_field_id[position].update(get_element_dict(field))
    else:
        pos_field_id[position] = get_element_dict(field)
    if scritp_type:
        pos_field_id[position]['scritp_type'] = scritp_type
    if not pos_field_id[position].has_key('scritp_type'):
        pos_field_id[position]['scritp_type'] = ''
    return pos_field_id


def addMultipleChoice(answer, element):
    return True


def set_status_values(pos_field_id, record):
    custom_answer = {}
    #set status de la orden
    custom_answer['f1054000a030000000000002'] = 'por_asignar'
    return custom_answer

def set_prioridad_value(form_field_id, record):
    print 'form_field_id=', form_field_id
    print 'record=', record
    print '============================================='
    print 'ME quede revisando el darle un valor aproximadao a los campos select'
    print 'definitivamente que tenemos que hacer algo en al api, o no ponerlo o poner un opc de best efort'
    print stop
####
#### Record Not Assinged
####


def query_folio_preorder(form_id , folio):
    query = {'form_id':  form_id, 'deleted_at' : {'$exists':False}, 'folio':str(folio)}
    select_columns = {'folio':1, 'answers':1}
    return query, select_columns


def get_folio_preorder(form_id, folio):
    query, select_columns = query_folio_preorder(form_id, folio)
    record = cr.find(query, select_columns)
    if record.count() >= 1:
        return record
    return False


def record_not_assigned(record, metadata, pre_os_field_id, folio):
    ###
    ### returns a dict with the instruccions of create or update
    ###
    metadata['form_id'] = 11149
    existing_record = get_folio_preorder(metadata['form_id'], folio)
    result = {'create': {}}
    if not existing_record:
        result['create'] = create_preorder_format(record, metadata, pre_os_field_id, folio)
    else:
        result['update'] = update_preorder_format(existing_record, record, metadata, pre_os_field_id, folio, is_update=True)
    return result


def assigned_record_validations(this_record):
    ### Valida Etapa
    is_valid = False
    #print 'this_record=',this_record
    if this_record.has_key('etapa'):
        #print ' etapa=', this_record['etapa']
        if this_record['etapa'] in ['PB','pb','PS','ps']:
            #print stop
            is_valid =  True
    ### Valida Autorizacion
    if this_record.has_key('tipo'):
        #print 'tipo', this_record['tipo']
        if this_record['tipo'] in ['A9']:
            is_valid =  'Requires Authorization'
    ### Check
    return is_valid


#def requires_autorization(this_record):

def assigned_record(record, metadata, pos_field_id, pre_os_field_id, folio, is_assigned):
    ###
    ### returns a dict with the instruccions of create or update
    ###
    metadata['form_id'] = 10540
    existing_record_preorder = get_folio_preorder(11149, folio)
    existing_record = get_folio_preorder(metadata['form_id'], folio)
    result = {'create': {}}
    #revisa preordenes
    if existing_record_preorder and is_assigned.has_key(False):
        print '############### borrar la orden ya que no se asigno a PCI ###############3'
        ###TODO guardar todas las no asignadas para poder hacer comparativas
        return result
    if existing_record_preorder and is_assigned.has_key(True):
        # Es una preorden que se acaba de asignar a PCI
        expediente = is_assigned['True']
        metadata['form_id'] = 11149
        existing_record_preorder = validate_status(existing_record_preorder)
        if existing_record_preorder:
            result['update'] = update_preorder_format(existing_record_preorder, record, metadata, pre_os_field_id, folio, is_update=True)
            #TODO ASGINAR A USARIO
    #revisa ordenes
    if not existing_record and is_assigned.has_key(True):
        this_record = create_preorder_format(record, metadata, pos_field_id, folio)
        is_valid = assigned_record_validations(this_record)
        if is_valid:
            if is_valid == 'Requires Authorization':
                existing_record_authorization = get_folio_preorder(11173, folio)
                if existing_record_authorization:
                    authorization_record = existing_record_authorization.next()
                    if True: #in_authorization_status(authorization_record):
                        metadata['form_id'] = 11173
                        authorization_record = validate_status(authorization_record)
                        if authorization_record:
                            aa = update_preorder_format(authorization_record, record, metadata, pos_field_id, folio, is_update=True)
                            result['update'] = aa #update_preorder_format(authorization_record, record, metadata, pos_field_id, folio)
                else:
                    result['create'] = update_authorization_record(this_record)
            else:
                result['create'] = this_record
    if existing_record and is_assigned.has_key(True):
        existing_record = existing_record.next()
        existing_record = validate_status(existing_record)
        if existing_record:
            result['update'] = update_preorder_format(existing_record, record, metadata, pos_field_id, folio, is_update=True)
    return result


def validate_status(record):
    status = get_record_status(record)
    if status == 'objetada':
        record['answers']['f1054000a030000000000002'] = 'reasigada'
        return record
    if status in ('liquidada', 'ejecutada_-_no_liquidada','pendiente', 'autorizado','asignada'):
        return False
    ### Cualquier otro status regresa lo mismo que tenia
    # if status in ('por_asignar', 'sin_asignar','reasigada'):
    #     return record
    return record


def get_record_status(answers):
    if answers.has_key('answers'):
        answers = answers['answers']
    if answers.has_key('f1054000a030000000000002') and answers['f1054000a030000000000002']:
        return answers['f1054000a030000000000002']
    if answers.has_key('f1114900a010000000000010') and answers['f1114900a010000000000010']:
        return answers['f1114900a010000000000010']
    if answers.has_key('f1054000a010000000000013') and answers['f1054000a010000000000013']:
        return answers['f1054000a010000000000013']
    return False


def update_authorization_record(this_record):
    this_record['form_id'] = 11173
    if this_record.has_key('answers'):
        this_record['answers']['f1054000a010000000000013'] = 'por_autorizar'
    else:
        this_record['answers'] = {'f1054000a010000000000013':'por_autorizar'}
    return this_record


def in_authorization_status(authorization_record):
    if authorization_record.has_key('answers') and authorization_record['answers'].has_key('f1054000a010000000000013'):
        status = authorization_record['answers']['f1054000a010000000000013']
        if status == 'por_autorizar':
            return True
    return False


def update_preorder_format(existing_record, record, metadata, pre_os_field_id, folio, is_update=False):
    try:
        actual_record = existing_record.next()
    except AttributeError:
        #its being send on a dictionary all ready
        actual_record = existing_record
    this_record = create_preorder_format(record, metadata, pre_os_field_id, folio, is_update)
    this_record['_id'] = actual_record['_id']
    for key in actual_record['answers'].keys():
        if this_record['answers'].has_key(key):
            continue
        else:
            this_record['answers'][key] = actual_record['answers'][key]
    return this_record


def create_preorder_format(record, metadata, pre_os_field_id, folio, is_update=False):
    ###
    ### Craete new record
    ###
    this_record = {}
    answer = {}
    this_record.update(metadata)
    etapa = tipo = tipo_de_tarea = clase = False
    for pos, element in pre_os_field_id.iteritems():
        if element['scritp_type'] == 'folio' and type(pos) == int:
            this_record.update({'folio': str(record[pos])})
        elif element['scritp_type'] == 'etapa' and type(pos) == int:
            if record[pos]:
                etapa = True
                this_record.update({'etapa': str(record[pos])})
        elif element['scritp_type'] == 'tipo' and type(pos) == int:
            if record[pos]:
                tipo = True
                this_record.update({'tipo': str(record[pos])})
        elif element['scritp_type'] == 'clase' and type(pos) == int:
            if record[pos]:
                clase = True
                this_record.update({'clase': str(record[pos])})
        elif element['scritp_type'] == 'tipo de tarea' and type(pos) == int:
            if record[pos]:
                tipo_de_tarea = True
                this_record.update({'tipo de tarea': str(record[pos])})
        if type(pos) != int:
            if pos not in ['clase','tipo','tipo de tarea', 'etapa']:
                answer.update(lkf_api.make_infosync_json(pos, element))
        else:
            answer.update(lkf_api.make_infosync_json(record[pos], element))
    if not etapa:
        this_record.update({'etapa': get_etapa_tipo_class(this_record, 'etapa')})
    if not tipo:
        this_record.update({'tipo': get_etapa_tipo_class(this_record, 'tipo')})
    if not clase:
        this_record.update({'clase': get_etapa_tipo_class(this_record, 'clase')})
    if not tipo_de_tarea:
        this_record.update({'tipo de tarea': make_tipo_de_tarea(this_record)})
    if not etapa or not tipo or not clase or not tipo_de_tarea:
        for pos, element in pre_os_field_id.iteritems():
            if element['scritp_type'] == 'etapa' and not etapa:
                answer.update(lkf_api.make_infosync_json(this_record['etapa'], element))
            if element['scritp_type'] == 'tipo' and not tipo:
                answer.update(lkf_api.make_infosync_json(this_record['tipo'], element))
            if element['scritp_type'] == 'clase' and not clase:
                answer.update(lkf_api.make_infosync_json(this_record['clase'], element))
            if element['scritp_type'] == 'tipo de tarea' and not tipo_de_tarea:
                answer.update(lkf_api.make_infosync_json(this_record['tipo de tarea'], element))
    if not is_update:
        answer.update(set_status_values(pre_os_field_id, record ))
    if this_record.has_key('form_id') and this_record["form_id"] == 11149:
        print 'answer=', answer
        answer.update(set_prioridad_value(pre_os_field_id, record))
    this_record["answers"] = answer
    print 'this_record',this_record
    print stop
    return this_record


def make_tipo_de_tarea(this_record):
    res = ''
    search_keys = ['tipo', 'clase', 'etapa']
    for key in search_keys:
        if this_record.has_key(key) and this_record[key]:
            res += this_record[key]
        else:
            res += '--'
    return res


def get_etapa_tipo_class(this_record, ttype):
    res = ''
    if this_record.has_key('tipo de tarea') and this_record['tipo de tarea']:
        if ttype == 'etapa':
            res = this_record['tipo de tarea'][:6]
            res = res[4:]
        if ttype == 'tipo':
            res = this_record['tipo de tarea'][:2]
        if ttype == 'clase':
            res = this_record['tipo de tarea'][:4]
            res = res[2:]
    return res


def update_preorder(exiting_record, record, metadata, pos_field_id, folio):
    ###
    ### Updates preorder informacion
    ###
    record = exiting_record[0]
    this_record = create_preorder_format(record, metadata, pre_os_field_id, folio)

    return this_record

####
#### END of Record Not Assinged
####

def create_record(pos_field_id, pre_os_field_id, records, header):
    records_to_upload = []
    records_to_update = []
    metadata = lkf_api.get_metadata(form_id=10540, user_id=settings.config['USER_ID'] )
    header_dict = make_header_dict(header)
    exp_cols = get_asignacion_pci_col(header_dict)
    print 'records count', len(records)
    for record in records:
        cont = False
        is_assigned = check_assignation(exp_cols, record)
        folio = get_record_folio(header_dict, record)
        if is_assigned:
            print '*ASSIGNED*'
            this_record = assigned_record(record, metadata, pos_field_id, pre_os_field_id, folio, is_assigned)
        else:
            print '==NOT ASSIGNED=='
            this_record = record_not_assigned(record, metadata, pre_os_field_id, folio)
        # answer = {}
        # this_record = {}
        # count = 0
        # this_record.update(metadata)
        # for pos, element in pos_field_id.iteritems():
        #     count +=1
        #     if element['field_type'] == 'folio':
        #         this_record['folio'] = str(record[pos])
        #     else:
        #         answer.update(lkf_api.make_infosync_json(record[pos], element))
        # answer.update(set_status_values(pos_field_id, record ))
        # this_record["answers"] = answer
        if this_record.has_key('create') and this_record['create']:
            records_to_upload.append(this_record['create'])
        if this_record.has_key('update') and this_record['update']:
            records_to_update.append(this_record['update'])
    print '=========================================='
    if records_to_upload:
        network.post_forms_answers(records_to_upload)
    if records_to_update:
        network.patch_forms_answers(records_to_update,0)
    print 'fin ============================='
    print 'ERROERS', settings.GLOBAL_ERRORS
    return True



def upload_bolsa():
    files = get_files2upload()
    #files = [{u'_id': ('58575ff4b43fdd35e3169665'), u'answers': {u'f1074100a010000000000001': {u'file_name': u'BASE 16-DICIEMBRES10.xls', u'file_url': u'uploads/1259_jgemayel@pcindustrial.com.mx/e201093c634a2a2ff2068b4df622401a2ac90c83.xls'}}}]
    if files:
        for file_url in files:
            if file_url.has_key('answers') and file_url['answers'].has_key('f1074100a010000000000001') \
                and file_url['answers'].has_key('f1074100a0100000000000c1'):
                cope = file_url['answers']['f1074100a0100000000000c1']
                cope = cope.replace('_', ' ').title()
                if file_url['answers']['f1074100a010000000000001'].has_key('file_url'):
                    url = file_url['answers']['f1074100a010000000000001']['file_url']
                    #print 'URL', url
                    if url.find('https') == -1:
                        url = 'https://app.linkaform.com/media/' + url
                    #try:
                    if True:
                        header, records = read_file(url)
                    #except:
                        print '####TODO mandar comunicado de recordad que el formato mandado esta mal'
                        #continue
                    #records = get_rr()
                    pos_field_id = get_pos_field_id_dict(header, 10540, cope=cope)
                    pre_os_field_id = get_pos_field_id_dict(header, 11149, cope=cope)
                    create_record(pos_field_id, pre_os_field_id, records, header)
                else:
                    print 'no file found'
            else:
                print 'no recored found'

upload_bolsa()
