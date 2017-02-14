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
    'AUTHORIZATION_TOKEN_VALUE' : '829df5615c166a9eb1b7f36f4494b1fe27059644',
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


def make_excel_file(rows):
    #rows = make_array(orders)
    date = time.strftime("%Y_%m_%d")
    file_name = "/tmp/output_%s.xlsx"%(date)
    pyexcel.save_as(array=rows,
        dest_file_name=file_name)
    return file_name


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
    print '###TODO SETUP a priority if the file dosent cotains any'
    return {}
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
                answer.update(lkf_api.make_infosync_json(pos, element, best_effort=True))
        else:
            answer.update(lkf_api.make_infosync_json(record[pos], element, best_effort=True))
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
        answer.update(set_prioridad_value(pre_os_field_id, record))
    this_record["answers"] = answer
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

def update_create_json(create_json, this_record, is_assigned):
    if this_record.has_key('create') and this_record['create']:
        create_json['created']['total'] += 1
        if is_assigned == False:
            create_json['created']['preorder'] += 1
        elif this_record['create']['tipo'] == 'A9':
            create_json['created']['authorization'] += 1
        else:
            create_json['created']['order'] += 1
    if this_record.has_key('update') and this_record['update']:
        create_json['uploaded']['total'] += 1
        if is_assigned == False:
            create_json['uploaded']['preorder'] += 1
        elif this_record['update']['tipo'] == 'A9':
            create_json['uploaded']['authorization'] += 1
        else:
            create_json['uploaded']['order'] += 1
    return create_json


def create_record(pos_field_id, pre_os_field_id, records, header):
    records_to_upload = []
    records_to_update = []
    record_errors = []
    create_json = {'created':{'preorder':0, 'order':0, 'authorization':0 ,'total':0, 'errores':0},
                    'uploaded':{'preorder':0, 'order':0, 'authorization':0, 'total':0, 'errores':0},
                    'file_url' : False}
    metadata = lkf_api.get_metadata(form_id=10540, user_id=settings.config['USER_ID'] )
    header_dict = make_header_dict(header)
    exp_cols = get_asignacion_pci_col(header_dict)
    print 'records count', len(records)
    cc = 0
    for record in records:
        cc += 1
        print '*', cc
        #if cc < 70:
        #    continue
        this_record = {}
        cont = False
        is_assigned = check_assignation(exp_cols, record)
        folio = get_record_folio(header_dict, record)

        if is_assigned:
            this_record = assigned_record(record, metadata, pos_field_id, pre_os_field_id, folio, is_assigned)
        else:
            this_record = record_not_assigned(record, metadata, pre_os_field_id, folio)

        if this_record.has_key('create') and this_record['create']:
            #records_to_upload.append(this_record['create'])
            #if True:
            response = network.post_forms_answers(this_record['create'])
        elif this_record.has_key('update') and this_record['update']:
            #records_to_update.append(this_record['update'])
            #if True:
            response = network.patch_forms_answers(this_record['update'],this_record['update']['_id'])
            #No se subio nada
        else:
            response= {'status_code': 205}

        if response['status_code'] in (200,201,202,204, 205):
            if response['status_code'] != 205:
                create_json.update(update_create_json(create_json, this_record, is_assigned))
        else:
            print '$#@!$#@!%$$##!'
            record_errors.append(record)

    if record_errors:
        print 'errors', len(record_errors)
        create_json['file_url'] = upload_error_file(header, record_errors)
    print 'fin ============================='
    return create_json


def upload_error_file(header, record_errors):
            record_errors.insert(0,header)
            archivo_file_name = make_excel_file(record_errors)
            csv_file = open(archivo_file_name,'rb')
            csv_file_dir = {'File': csv_file}
            upload_data ={'form_id': 10741, 'field_id':'f1074100a010000000000003'}
            upload_url = lkf_api.post_upload_file(data=upload_data, up_file=csv_file_dir)
            csv_file.close()
            file_url = upload_url['data']['file']
            try:
                file_url = upload_url['data']['file']
                record['answers']['f1074100a010000000000003'] ={
                'file_name':'Errores de Carga %s.xlsx'%file_date,
                'file_url':file_url}
            except KeyError:
                print 'could not save file Errores'
            return file_url


def upload_bolsa():
    files = get_files2upload()
    #files = [{u'_id': ('58575ff4b43fdd35e3169665'), u'answers': {u'f1074100a010000000000001': {u'file_name': u'BASE 16-DICIEMBRES10.xls', u'file_url': u'uploads/1259_jgemayel@pcindustrial.com.mx/e201093c634a2a2ff2068b4df622401a2ac90c83.xls'}}}]
    if files:
        file_list = []
        for record in files:
            file_list.append(record.copy())
        for ffile in file_list:
            print 'ffile' ,ffile
            if ffile.has_key('answers'):
                ### Updates. Actualiza el registro y pone procesando
                ffile['answers']['f1074100a010000000000005'] = 'procesando'
                record_id = ffile.pop('_id')
                ffile.update(lkf_api.get_metadata(10741, user_id = settings.config['USER_ID']))
                network.patch_forms_answers(ffile, record_id)
                ffile['_id'] = record_id
        for file_url in file_list:
            if file_url.has_key('answers') and file_url['answers'].has_key('f1074100a010000000000001') \
                and file_url['answers'].has_key('f1074100a0100000000000c1'):
                cope = file_url['answers']['f1074100a0100000000000c1']
                cope = cope.replace('_', ' ').title()
                print '===== starting ======'
                if file_url['answers']['f1074100a010000000000001'].has_key('file_url'):
                    url = file_url['answers']['f1074100a010000000000001']['file_url']
                    print 'URL', url
                    if url.find('https') == -1:
                        url = 'https://app.linkaform.com/media/' + url
                    try:
                        header, records = read_file(url)
                    except:
                        file_url['answers']['f1074100a010000000000002'] = 'El formato del archvio adjunto esta mal. Favor de revisar que el formato sea xlsx o csv. Recuerda actualizar el estatus a Por Cargar'
                        file_url['answers']['f1074100a010000000000005'] = 'error'
                        network.patch_forms_answers(file_url, file_url['_id'])
                        print 'error reading'
                        continue
                    #records = get_rr()
                    pos_field_id = get_pos_field_id_dict(header, 10540, cope=cope)
                    pre_os_field_id = get_pos_field_id_dict(header, 11149, cope=cope)
                    create_json = create_record(pos_field_id, pre_os_field_id, records, header)
                    print 'create_json', create_json
                    file_url.update(get_bolsa_update_communication(file_url, create_json))
                else:
                    file_url['answers']['f1074100a010000000000002'] = 'No se encontro ningun archivo adjunto'
                    file_url['answers']['f1074100a010000000000005'] = 'error'
                    print 'no file found'


                #Actualiza el status del la bolsa
                if settings.GLOBAL_ERRORS:
                    print 'todo with errors'
                    file_url['answers']['f1074100a010000000000004'] = settings.GLOBAL_ERRORS

                network.patch_forms_answers(file_url, file_url['_id'])
            else:
                    print 'no FILE found'
    else:
        print 'no recored found'


def get_bolsa_update_communication(file_url, create_json):
    file_url['answers']['f1074100a010000000000a10'] = create_json['created']['preorder'] or 0
    file_url['answers']['f1074100a010000000000a11'] = create_json['created']['authorization'] or 0
    file_url['answers']['f1074100a010000000000a12'] = create_json['created']['order'] or 0
    file_url['answers']['f1074100a010000000000a13'] = create_json['created']['errores'] or 0
    file_url['answers']['f1074100a010000000000a14'] = create_json['created']['total'] or 0

    file_url['answers']['f1074100a010000000000b10'] = create_json['uploaded']['preorder'] or 0
    file_url['answers']['f1074100a010000000000b11'] = create_json['uploaded']['authorization'] or 0
    file_url['answers']['f1074100a010000000000b12'] = create_json['uploaded']['order'] or 0
    file_url['answers']['f1074100a010000000000b13'] = create_json['uploaded']['errores'] or 0
    file_url['answers']['f1074100a010000000000b14'] = create_json['uploaded']['total'] or 0

    if create_json['file_url']:
        file_url['answers']['f1074100a010000000000002'] = 'Existieron en la carga. %s al crear y %s al acutalizar.\
         Favor ver el archivo Registros no cargados'%(create_json['created']['errores'],create_json['uploaded']['errores'])
        file_url['f1074100a010000000000003'] = create_json['file_url']
        file_url['answers']['f1074100a010000000000005'] = 'error'
    else:
        file_url['answers']['f1074100a010000000000002'] = 'Archivo cargado con exito'
        file_url['answers']['f1074100a010000000000005'] = 'cargado'

    return file_url

# def upload_test():
#     cope='mixcoac'
#     header= [u'folio', u'tipo', u'telefono', u'nombre', u'etapa', u'f_contrata', u'dilacion', u'diletapa', u'central', u'distrito', u'canal', u'of_c', u'area', u'oficina', u'ct', u'cm', u'f_ue', u'clase_serv', u'segmento', u'area_ct', u'segpred', u'nse_amai', u'abc', u'elite', u'sky', u'warzone', u'colonia', u'division', u'subdireccion', u'siglas', u'fol_pisaplex', u'ttarea', u'estado', u'nombretecnico', u'expediente', u'zona', u'idtarea', u'grupoasignacion', u'empresa', u'tipo_sitio', u'poligono-zona', u'prioritaria', u'resynores', u'agrupar27', u'ftth', u'vienede', u'portabilidad', u'etiqueta', u'prioridad', u'agrupadil', u'agrupadiletapa', u'pendiente_puente', u'producto', u'fech_meta', u'sema_aten', u'empresas', u'responsab', u'entity', u'fielder', u'fo']
#     records= [[40627946, u'A0', 5570370944, u'ALVAREZ TREJO LEONOR', u'PF', u'11/28/2016', 51, 43, u'TR_', u'TR_0034', u'', u'LO', u'MIXCOAC', u'LOR', u'SLI', u'CAS', 42710, 10, u'', u'MIXCOAC', u'C-', u'C', 0, 0, 0, 0, u'LOS PADRES', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONCENTRADOR', u'SAN JERONIMO', u'', u'RESIDENCIAL', u'RESIDENCIAL', 0, u'BESTPHONE        ', 1, u'Portabilidad', 1, u'> 25 d\xedas', u'> 25 d\xedas', u'NO', u'ALTAS VOZ', u'23-Jan-17', u'En Tiempo', u'FUERA', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41189934, u'TI', 5556689488, u'NETSHELL SA DE CV', u'Y2', u'12/20/2016', 29, 29, u'SJ_', u'SJ_0029', u'', u'WTG', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'12/20/2016', u'2L', u'CP', u'MIXCOAC', u'C-', u'C+', 1, 0, 0, 1, u'SAN JERONIMO ACULCO', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'SAN JERONIMO', u'', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 1, u'', 0, u'TI', 8, u'> 25 d\xedas', u'> 25 d\xedas', u'NO', u'TI', u'', u'', u'FUERA', u'', u'', u'-', ''], [41250733, u'D3', 5556358515, u'URQUIZA GARCIATORRES JUAN CARL', u'CO', u'12/22/2016', 27, 1, u'SL_', u'SL_0095', u'', u'LO', u'MIXCOAC', u'MIC', u'SLI', u'CAS', u'1/17/2017', u'1L', u'R5', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 0, u'RESIDENCIAL DE TARANGO', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'SANTA LUCIA', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'', 0, u'Cambio Domicilio', 2, u'> 25 d\xedas', 1, u'NO', u'CD INF', u'', u'', u'FUERA', u'', u'', u'-', ''], [41236521, u'TI', 5555503527, u'CANO GARCIA MARIA DEL ROCIO', u'Y2', u'12/22/2016', 27, 27, u'CA_', u'CA_0010', u'', u'WCP', u'MIXCOAC', u'MIC', u'SLI', u'CAS', u'12/22/2016', u'1L', u'R2', u'MIXCOAC', u'A+', u'C+', 1, 0, 0, 0, u'LAS AGUILAS', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'SANTA LUCIA', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'TI', 8, u'> 25 d\xedas', u'> 25 d\xedas', u'NO', u'TI', u'', u'', u'FUERA', u'', u'', u'-', ''], [41408045, u'TV', 5552927878, u'DINTEC CONSULTING SA DE CV', u'PS', u'12/29/2016', 20, 1, u'GI_', u'GI_0029', u'', u'PRM', u'MIXCOAC', u'MIC', u'MIC', u'CAS', u'1/17/2017', u'2L', u'CP', u'MIXCOAC', u'CM', u'A/B', 1, 0, 0, 1, u'FLORIDA', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'SAN JOSE INSURGENTES', u'', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 1, u'', 0, u'1 Play Inf', 6, u'11 a 25 d\xedas', 1, u'NO', u'TV', u'12-Jan-17', u'Fuera de Tiempo', u'ASISTENCIA', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41407830, u'D3', 5555858216, u'MARTINEZ MARTINEZ MARIA ELENA', u'PA', u'12/29/2016', 20, 1, u'BB_', u'BB_0003', u'', u'LO', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'1/17/2017', u'1L', u'R5', u'MIXCOAC', u'C-', u'C+', 1, 0, 0, 0, u'LOMAS DE SAN BERNABE', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONTENEDOR', u'SAN JERONIMO', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'', 0, u'Cambio Domicilio', 2, u'11 a 25 d\xedas', 1, u'NO', u'CD INF', u'', u'', u'FUERA', u'', u'', u'-', ''], [41425665, u'TI', 5555685628, u'MATUK KANAN CARLOS', u'Y2', u'12/30/2016', 19, 19, u'PD_', u'PD_0015', u'', u'LO', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'12/30/2016', u'1L', u'R4', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 0, u'JARDINES DEL PEDREGAL', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONCENTRADOR', u'PEDREGAL', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'TI', 8, u'11 a 25 d\xedas', u'11 a 25 d\xedas', u'NO', u'TI', u'26-Jan-17', u'En Tiempo', u'FUERA', u'JORGE VIVAR', u'SISTEMAS DIVISIONAL', u'-', ''], [41451080, u'TI', 5555507521, u'SOLUCIONES Y CONSTRUCCIONES EC', u'PS', u'1/2/2017', 16, 7, u'GI_', u'GI_0003', u'', u'WMX', u'MIXCOAC', u'MIC', u'MIC', u'CAS', u'1/11/2017', u'2L', u'CM', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 0, u'GUADALUPE INN', u'METRO', u'METRO SUR', u'MIX', 56660028, u'TI2LPAFPI', u'PENDIENTE', u'', u'.', u'MI_GI_01 CTLS', 56660028, u'MI_CTLS', u'', u'EDIFICIO', u'SAN JOSE INSURGENTES', u'', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 1, u'', 0, u'TI', 8, u'11 a 25 d\xedas', u'4 a 10 d\xedas', u'SI', u'TI', u'12-Jan-17', u'Fuera de Tiempo', u'NO ASIGNADO', u'PLANTA', u'OPERACI\xd3N', u'-', u'FO'], [41454533, u'D2', 5522234397, u'LOPEZ MEJIA ANGELA FERNANDA', u'SU', u'1/2/2017', 16, 1, u'RX_', u'RX_0008', u'', u'MI', u'MIXCOAC', u'MIC', u'SLI', u'CAS', u'1/17/2017', u'1L', u'R5', u'MIXCOAC', u'C-', u'D+', 0, 0, 0, 0, u'OLIVAR DEL CONDE 2A SECCION', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONTENEDOR', u'SANTA LUCIA', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'', 0, u'Cambio Domicilio', 2, u'11 a 25 d\xedas', 1, u'NO', u'CD INF', u'', u'', u'FUERA', u'', u'', u'-', ''], [41477098, u'A0', 5555503183, u'SEGOB/INSURGENTES SUR SPF', u'E3', u'1/3/2017', 15, 1, u'SA_', u'SA_0003', u'', u'AC2', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/17/2017', u'2L', u'CM', u'MIXCOAC', u'A+', u'C+', 1, 0, 0, 1, u'SAN ANGEL', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'CORREDOR INSURGENTES', u'CORREDOR INSURGENTES', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 1, u'', 0, u'2 Play Com', 3, u'11 a 25 d\xedas', 1, u'NO', u'ALTAS INF', u'22-Jan-17', u'En Tiempo', u'FUERA', u'CENTRAL', u'CENTRAL', u'-', ''], [41482901, u'D2', 5555952564, u'MONTOYA DUARTE MANUEL', u'E7', u'1/3/2017', 15, 1, u'SA_', u'SA_0058', u'', u'PL', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/17/2017', u'1L', u'R5', u'MIXCOAC', u'C-', u'C', 0, 0, 0, 0, u'PROGRESO', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'PEDREGAL', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'', 0, u'Cambio Domicilio', 2, u'11 a 25 d\xedas', 1, u'NO', u'CD INF', u'22-Jan-17', u'En Tiempo', u'FUERA', u'CENTRAL', u'CENTRAL', u'-', ''], [41482027, u'D2', 5555633850, u'DOMINGUEZ GONZALEZ RITA', u'PS', u'1/3/2017', 15, 1, u'MI_', u'MI_0037', u'', u'MI', u'MIXCOAC', u'MIC', u'MIC', u'TYB', u'1/17/2017', u'1L', u'R5', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 1, u'INSURGENTES MIXCOAC', u'METRO', u'METRO SUR', u'MIX', 56867622, u'D21LP4HPI', u'ASIGNADO', u'CIMAQSA_BOLSA NUEVA COPE MI', 2220100, u'MI_MI_02 INST', 56867622, u'MI_ INST', u'CIMAQSA', u'EDIFICIO', u'MIXCOAC', u'MIXCOAC', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'Cambio Domicilio', 2, u'11 a 25 d\xedas', 1, u'NO', u'CD INF', u'11-Jan-17', u'Fuera de Tiempo', u'CIMAQSA', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41481740, u'TV', 5556524756, u'LUC HAUSE DE BELLER ROSA MARIA', u'PS', u'1/3/2017', 15, 14, u'PD_', u'PD_0133', u'', u'WMX', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/4/2017', u'2L', u'CE', u'MIXCOAC', u'A+', u'C+', 1, 0, 0, 1, u'SANTA TERESA', u'METRO', u'METRO SUR', u'MIX', 56692270, u'TV2LPBD', u'ASIGNADO', u'GARDU\xc3\u2018O CONTRERAS  SANDRA ROCIO', 1404537, u'MI_PD_01 CTLS', 56692270, u'MI_CTLS', u'TELMEX', u'CONCENTRADOR', u'PEDREGAL', u'', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 0, u'', 0, u'1 Play Inf', 6, u'11 a 25 d\xedas', u'11 a 25 d\xedas', u'SI', u'TV', u'13-Jan-17', u'Fuera de Tiempo', u'TELMEX', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41477714, u'TV', 5555688398, u'SANCHEZ HUESCA OLGA', u'PS', u'1/3/2017', 15, 15, u'PD_', u'PD_0005', u'', u'WTL', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/3/2017', u'1L', u'R6', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 0, u'JARDINES DEL PEDREGAL', u'METRO', u'METRO SUR', u'MIX', 56681323, u'TV1LPB', u'ASIGNADO', u'GARDU\xc3\u2018O CONTRERAS  SANDRA ROCIO', 1404537, u'MI_PD_01 INST', 56681323, u'MI_CTLS', u'TELMEX', u'CONCENTRADOR', u'PEDREGAL', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'1 Play Inf', 6, u'11 a 25 d\xedas', u'11 a 25 d\xedas', u'SI', u'TV', u'12-Jan-17', u'Fuera de Tiempo', u'TELMEX', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41500312, u'TI', 5551353993, u'MUCI O MUCI O HECTOR', u'Y2', u'1/4/2017', 14, 14, u'PD_', u'PD_0111', u'', u'WMX', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/4/2017', u'2L', u'CP', u'MIXCOAC', u'A+', u'A/B', 1, 0, 1, 0, u'FUENTES DEL PEDREGAL', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONCENTRADOR', u'PEDREGAL', u'', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 1, u'', 0, u'TI', 8, u'11 a 25 d\xedas', u'11 a 25 d\xedas', u'NO', u'TI', u'10-Jan-17', u'Fuera de Tiempo', u'FUERA', u'JORGE VIVAR', u'SISTEMAS DIVISIONAL', u'-', ''], [41507484, u'A4', 5556806410, u'VARGAS SILVA ENRIQUE', u'PS', u'1/4/2017', 14, 9, u'CA_', u'CA_0025', u'', u'WTX', u'MIXCOAC', u'MIC', u'SLI', u'CAS', u'1/9/2017', 10, u'R6', u'MIXCOAC', u'C-', u'C+', 1, 0, 0, 0, u'UHAB LOMAS DE PLATEROS', u'METRO', u'METRO SUR', u'MIX', 56741487, u'A410PBG', u'ASIGNADO', u'MORENO CRUZ JOSE ARMANDO', 8523039, u'SL_CA_05 INST', 56741487, u'SL_ INST', u'TELMEX', u'EDIFICIO', u'MIXCOAC', u'MIXCOAC', u'RESIDENCIAL', u'RESIDENCIAL', 1, u'', 0, u'1 Play', 7, u'11 a 25 d\xedas', u'4 a 10 d\xedas', u'NO', u'ALTAS VOZ', u'23-Jan-17', u'En Tiempo', u'TELMEX', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41508680, u'D2', 5555758144, u'RICZAM S.DE R.L. DE C.V.', u'EP', u'1/4/2017', 14, 1, u'BY_', u'BY_0001', u'', u'LO', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'1/17/2017', 20, u'CM', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 0, u'RANCHO SAN FRANCISCO', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'GABINETE', u'SAN JERONIMO', u'', u'NO RESIDENCIAL', u'COMERCIAL', 0, u'', 0, u'Cambio Domicilio', 2, u'11 a 25 d\xedas', 1, u'SI', u'CD VOZ', u'', u'', u'FUERA', u'', u'', u'-', ''], [41505088, u'D3', 5554255109, u'MARTINEZ CALDERON AMALIA', u'EQ', u'1/4/2017', 14, 4, u'BB_', u'BB_0013', u'', u'LO', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'1/14/2017', 10, u'R6', u'MIXCOAC', u'C-', u'D+', 0, 0, 0, 0, u'LAS CRUCES', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONTENEDOR', u'SAN JERONIMO', u'', u'RESIDENCIAL', u'RESIDENCIAL', 0, u'', 0, u'Cambio Domicilio', 2, u'11 a 25 d\xedas', u'4 a 10 d\xedas', u'NO', u'CD VOZ', u'', u'', u'FUERA', u'', u'', u'-', ''], [41505963, u'A9', 5521249919, u'ORTEGA MONTES DE OCA MAYRA MIR', u'C6', 42739, 14, 1, u'TY_', u'TY_0110', u'', u'PL', u'MIXCOAC', u'VAL', u'TYB', u'TYB', 42752, u'1L', u'', u'MIXCOAC', u'C-', u'C', 0, 0, 0, 0, u'TACUBAYA', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'MIXCOAC', u'MIXCOAC', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'2 Play Res', 4, u'11 a 25 d\xedas', 1, u'NO', u'ALTAS INF', u'', u'', u'FUERA', u'', u'', u'-', ''], [41529224, u'A0', 5550854142, u'SECRETARIA DE GOBERNACION SERV', u'PO', u'1/5/2017', 13, 1, u'SA_', u'SA_0003', u'', u'AC2', u'MIXCOAC', u'LOR', u'MIC', u'CAS', 42752, u'2L', u'', u'MIXCOAC', u'A+', u'C+', 1, 0, 0, 1, u'SAN ANGEL', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'CORREDOR INSURGENTES', u'CORREDOR INSURGENTES', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 1, u'', 0, u'2 Play Com', 3, u'11 a 25 d\xedas', 1, u'NO', u'ALTAS INF', u'22-Jan-17', u'En Tiempo', u'FUERA', u'ANDRES HDZ', u'CCR', u'-', ''], [41537568, u'A4', 5551356254, u'CERVANTES SUAREZ JUAN CARLOS', u'O2', u'1/5/2017', 13, 1, u'PD_', u'PD_0106', u'', u'API', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/17/2017', 10, u'R5', u'MIXCOAC', u'A+', u'C+', 1, 0, 0, 1, u'SAN JERONIMO ACULCO', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONCENTRADOR', u'PEDREGAL', u'', u'RESIDENCIAL', u'RESIDENCIAL', 1, u'', 0, u'1 Play', 7, u'11 a 25 d\xedas', 1, u'NO', u'ALTAS VOZ', u'23-Jan-17', u'En Tiempo', u'FUERA', u'VICTOR MANOATH ESQUIVEL', u'SISTEMAS COMERCIALES', u'-', ''], [41533915, u'TV', 5551350154, u'TORRES ROCHA ALICIA', u'ES', u'1/5/2017', 13, 1, u'PD_', u'PD_0185', u'', u'PC', u'MIXCOAC', u'LOR', u'MIC', u'CAS', 42752, u'1L', u'R6', u'MIXCOAC', u'A+', u'A/B', 1, 0, 1, 0, u'FUENTES DEL PEDREGAL', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONCENTRADOR', u'PEDREGAL', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'1 Play Inf', 6, u'11 a 25 d\xedas', 1, u'NO', u'TV', u'25-Jan-17', u'En Tiempo', u'FUERA', u'CENTRAL', u'CENTRAL', u'-', ''], [41533792, u'TV', 5556525201, u'Y DESARROLLOS PEDREGAL JUEGOS', u'PS', u'1/5/2017', 13, 13, u'PD_', u'PD_0014', u'', u'WTG', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/5/2017', u'2L', u'C+', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 0, u'JARDINES DEL PEDREGAL', u'METRO', u'METRO SUR', u'MIX', 56709654, u'TV2LPBD', u'ASIGNADO', u'GARDU\xc3\u2018O CONTRERAS  SANDRA ROCIO', 1404537, u'MI_PD_01 CTLS', 56709654, u'MI_CTLS', u'TELMEX', u'CONCENTRADOR', u'PEDREGAL', u'', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 1, u'', 0, u'1 Play Inf', 6, u'11 a 25 d\xedas', u'11 a 25 d\xedas', u'SI', u'TV', u'25-Jan-17', u'En Tiempo', u'TELMEX', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41537578, u'A0', 5591551895, u'COI CENTRO ONCOLOGICO INTERNAC', u'PS', u'1/5/2017', 13, 4, u'TU_', u'TU_0008', u'', u'ACW', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'1/14/2017', u'2L', u'', u'MIXCOAC', u'C-', u'D+', 0, 0, 1, 0, u'EL OCOTAL', u'METRO', u'METRO SUR', u'MIX', 56742470, u'A02LP4D', u'ASIGNADO', u'UNE_BOLSA NUEVA, COPE SL', 2220142, u'SL_TU_02 INST', 56742470, u'SL_ INST', u'TEICO', u'CONCENTRADOR', u'SAN JERONIMO', u'', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 1, u'', 0, u'2 Play Com', 3, u'11 a 25 d\xedas', u'4 a 10 d\xedas', u'NO', u'ALTAS INF', u'07-Jan-17', u'Fuera de Tiempo', u'UNE', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41529420, u'A0', 5556603318, u'PEREZ MARTINEZ OSCAR MARTIN', u'S9', u'1/5/2017', 13, 2, u'CA_', u'CA_0018', u'', u'MI', u'MIXCOAC', u'MIC', u'SLI', u'CAS', u'1/16/2017', u'1L', u'R6', u'MIXCOAC', u'C-', u'C+', 1, 0, 0, 0, u'UHAB LOMAS DE PLATEROS', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'MIXCOAC', u'MIXCOAC', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'TELMEX           ', 1, u'Portabilidad', 1, u'11 a 25 d\xedas', 2, u'NO', u'ALTAS INF', u'21-Jan-17', u'En Tiempo', u'FUERA', u'TIENDAS', u'COMERCIAL', u'-', ''], [41524095, u'A9', 5510569191, u'FLORES MADIN JOSELINE', u'PS', u'1/5/2017', 13, 4, u'SL_', u'SL_0063', u'', u'MI', u'MIXCOAC', u'MIC', u'SLI', u'CAS', u'1/14/2017', u'1L', u'R6', u'MIXCOAC', u'C-', u'D+', 0, 0, 0, 0, u'CORPUS CHRISTI', u'METRO', u'METRO SUR', u'MIX', 56744296, u'A91LP4D', u'ASIGNADO', u'FILIAL ORDENES _ITCR', 2220111, u'SL_UY_01 INST', 56744296, u'SL_ INST', u'ITCR', u'EDIFICIO', u'SANTA LUCIA', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'', 0, u'2 Play Res', 4, u'11 a 25 d\xedas', u'4 a 10 d\xedas', u'NO', u'ALTAS INF', u'', u'', u'ITCR', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41542685, u'A4', 5515202241, u'SAN JERONIMO MOTORS SA DE CV', u'PS', u'1/5/2017', 13, 9, u'SJ_', u'SJ_0041', u'', u'ACW', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'1/9/2017', 20, u'A', u'MIXCOAC', u'A+', u'C+', 1, 0, 0, 1, u'SAN JERONIMO LIDICE', u'METRO', u'METRO SUR', u'MIX', 56741490, u'A420PBD', u'ASIGNADO', u'MORENO CRUZ JOSE ARMANDO', 8523039, u'SL_SJ_03 INST', 56741490, u'SL_ INST', u'TELMEX', u'EDIFICIO', u'SAN JERONIMO', u'', u'NO RESIDENCIAL', u'COMERCIAL', 0, u'', 0, u'PYME', 5, u'11 a 25 d\xedas', u'4 a 10 d\xedas', u'NO', u'ALTAS VOZ', u'15-Jan-17', u'En Tiempo', u'TELMEX', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41529499, u'D2', 5554250768, u'VALENCIA GARCIAJOSE LUIS', u'YS', u'1/5/2017', 13, 2, u'BB_', u'BB_0012', u'', u'LO', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'1/16/2017', u'1L', u'R5', u'MIXCOAC', u'C-', u'D+', 0, 0, 0, 0, u'LAS CRUCES', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONTENEDOR', u'SAN JERONIMO', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'', 0, u'Cambio Domicilio', 2, u'11 a 25 d\xedas', 2, u'NO', u'CD INF', u'', u'', u'FUERA', u'', u'', u'-', ''], [41561924, u'A0', 5555240641, u'PM ONSTREET SADE CV', u'KB', u'1/6/2017', 12, 1, u'SR_', u'SR_0028', u'', u'AG', u'MIXCOAC', u'VAL', u'MIC', u'TYB', u'1/17/2017', u'2L', u'R5', u'MIXCOAC', u'CM', u'A/B', 1, 0, 0, 0, u'DEL VALLE', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'DEL VALLE', u'DEL VALLE', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 1, u'', 0, u'2 Play Com', 3, u'11 a 25 d\xedas', 1, u'NO', u'ALTAS INF', u'22-Jan-17', u'En Tiempo', u'FUERA', u'INFORMATEC', u'TEC', u'-', ''], [41556319, u'TI', 5556811801, u'ROFES GARCIA BARTOLOME', u'PS', u'1/6/2017', 12, 12, u'PD_', u'PD_0055', u'', u'WVA', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/6/2017', u'1L', u'R2', u'MIXCOAC', u'C-', u'C', 0, 0, 0, 0, u'BARRIO SAN FRANCISCO', u'METRO', u'METRO SUR', u'MIX', 56718987, u'TI1LPBFPI', u'PENDIENTE', u'', u'.', u'MI_PD_01 INST', 56718987, u'MI_ INST', u'', u'CONCENTRADOR', u'PEDREGAL', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'TI', 8, u'11 a 25 d\xedas', u'11 a 25 d\xedas', u'NO', u'TI', u'08-Jan-17', u'Fuera de Tiempo', u'NO ASIGNADO', u'PLANTA', u'OPERACI\xd3N', u'-', u'FO'], [41561708, u'A9', 5556674311, u'PARRA RODRIGUEZ JERSAIN', u'PS', u'1/6/2017', 12, 11, u'TU_', u'TU_0010', u'', u'LO', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'1/7/2017', u'1L', u'R6', u'MIXCOAC', u'C-', u'D+', 0, 0, 0, 0, u'PUEBLO NUEVO ALTO', u'METRO', u'METRO SUR', u'MIX', 56723669, u'A91LP4D', u'ASIGNADO', u'UNE_BOLSA NUEVA, COPE SL', 2220142, u'SL_TU_02 INST', 56723669, u'SL_ INST', u'TEICO', u'CONCENTRADOR', u'SAN JERONIMO', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'', 0, u'2 Play Res', 4, u'11 a 25 d\xedas', u'11 a 25 d\xedas', u'NO', u'ALTAS INF', u'22-Dec-16', u'Fuera de Tiempo', u'UNE', u'PLANTA', u'OPERACI\xd3N', u'JUDA CONSTRUCCIONES SA DE CV', ''], [41560378, u'A9', 5550359921, u'LEYVA GONZALEZ JORGE ALBERTO', u'XO', u'1/6/2017', 12, 1, u'SJ_', u'SJ_0047', u'', u'LO', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'1/17/2017', u'1L', u'', u'MIXCOAC', u'A+', u'C+', 1, 0, 0, 1, u'LOMAS QUEBRADAS', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'SAN JERONIMO', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'2 Play Res', 4, u'11 a 25 d\xedas', 1, u'NO', u'ALTAS INF', u'21-Jan-17', u'En Tiempo', u'FUERA', u'GIANLUCA SOTRES D\xcdAZ', u'SISTEMAS GESTION', u'-', ''], [41556596, u'A9', 5556674033, u'ORTEGA REYES BRENDA VIANEY', u'PS', u'1/6/2017', 12, 11, u'TU_', u'TU_0012', u'', u'WFC', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'1/7/2017', u'1L', u'TC', u'MIXCOAC', u'C-', u'D+', 0, 0, 0, 0, u'EL ERMITANO', u'METRO', u'METRO SUR', u'MIX', 56720130, u'A91LP4D', u'ASIGNADO', u'UNE_BOLSA NUEVA, COPE SL', 2220142, u'SL_TU_01 INST', 56720130, u'SL_ INST', u'TEICO', u'CONCENTRADOR', u'SAN JERONIMO', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'', 0, u'2 Play Res', 4, u'11 a 25 d\xedas', u'11 a 25 d\xedas', u'NO', u'ALTAS INF', u'07-Jan-17', u'Fuera de Tiempo', u'UNE', u'PLANTA', u'OPERACI\xd3N', u'JUDA CONSTRUCCIONES SA DE CV', ''], [41554275, u'A9', 5516733754, u'GARCIA NU\xd0EZ ANA MARIA', u'PS', u'1/6/2017', 12, 1, u'UY_', u'UY_0004', u'', u'MI', u'MIXCOAC', u'MIC', u'SLI', u'CAS', u'1/17/2017', u'1L', u'', u'MIXCOAC', u'C-', u'D+', 0, 0, 0, 0, u'2 RIOS', u'METRO', u'METRO SUR', u'MIX', 56870490, u'A91LPBD', u'ASIGNADO', u'HIPOLITO GONZALEZ GERARDO', 8755108, u'SL_UY_01 CTLS', 56870490, u'SL_CTLS', u'TELMEX', u'CONCENTRADOR', u'SANTA LUCIA', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'', 0, u'2 Play Res', 4, u'11 a 25 d\xedas', 1, u'SI', u'ALTAS INF', u'', u'', u'TELMEX', u'PLANTA', u'OPERACI\xd3N', u'MARNA IMAGEN CREATIVA SA DE CV', ''], [41550218, u'A0', 5515203509, u'COMERCIALIZADORA FARMACEUTICA', u'PS', u'1/6/2017', 12, 1, u'TR_', u'TR_0008', u'', u'AC4', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'1/17/2017', u'2L', u'R4', u'MIXCOAC', u'A+', u'C', 0, 0, 0, 1, u'ALCANTARILLA', u'METRO', u'METRO SUR', u'MIX', 56723606, u'A02LPBD', u'ASIGNADO', u'PACHECO BARCENAS ROBERTO', 8747462, u'SL_TR_01 CTLS', 56723606, u'SL_CTLS', u'TELMEX', u'CONCENTRADOR', u'SAN JERONIMO', u'', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 0, u'', 0, u'2 Play Com', 3, u'11 a 25 d\xedas', 1, u'SI', u'ALTAS INF', u'', u'', u'TELMEX', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41549369, u'A0', 5566477090, u'GARCIA PADILLA JULIO CESAR', u'PS', u'1/6/2017', 12, 1, u'TR_', u'TR_0035', u'', u'WTL', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'1/17/2017', u'1L', u'', u'MIXCOAC', u'C-', u'D+', 0, 0, 0, 0, u'PUEBLO SAN BERNABE OCOTEPEC', u'METRO', u'METRO SUR', u'MIX', 56714026, u'A01LP4MPE', u'ASIGNADO', u'FILIAL_UNE_ SL', 2610222, u'SL_TR_03 INST', 56714026, u'SL_ INST', u'UNE', u'CONCENTRADOR', u'SAN JERONIMO', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'BESTPHONE        ', 1, u'Portabilidad', 1, u'11 a 25 d\xedas', 1, u'NO', u'ALTAS INF', u'14-Jan-17', u'Fuera de Tiempo', u'UNE', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41553833, u'A4', 5517130985, u'PEREZ ZAVALETA FELIX FERNANDO', u'PS', u'1/6/2017', 12, 12, u'EY_', u'EY_0002', u'', u'CUJ', u'MIXCOAC', u'MIC', u'SLI', u'CAS', u'1/6/2017', 10, u'R6', u'MIXCOAC', u'C-', u'C+', 1, 0, 0, 1, u'PRESIDENTES', u'METRO', u'METRO SUR', u'MIX', 56717487, u'A410PBG', u'ASIGNADO', u'MORENO CRUZ JOSE ARMANDO', 8523039, u'SL_EY_01 INST', 56717487, u'SL_ INST', u'TELMEX', u'CONTENEDOR', u'SANTA LUCIA', u'', u'RESIDENCIAL', u'RESIDENCIAL', 0, u'', 0, u'1 Play', 7, u'11 a 25 d\xedas', u'11 a 25 d\xedas', u'NO', u'ALTAS VOZ', u'16-Jan-17', u'En Tiempo', u'TELMEX', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41553398, u'A4', 5556813884, u'PULLMAN DE CHIAPAS SA DE CV', u'PS', u'1/6/2017', 12, 6, u'SJ_', u'SJ_0029', u'', u'LO', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'1/12/2017', 20, u'C-', u'MIXCOAC', u'C-', u'C+', 1, 0, 0, 1, u'SAN JERONIMO ACULCO', u'METRO', u'METRO SUR', u'MIX', 56790042, u'A420PBG', u'ASIGNADO', u'MORENO CRUZ JOSE ARMANDO', 8523039, u'SL_SJ_03 INST', 56790042, u'SL_ INST', u'TELMEX', u'EDIFICIO', u'SAN JERONIMO', u'', u'NO RESIDENCIAL', u'COMERCIAL', 1, u'', 0, u'PYME', 5, u'11 a 25 d\xedas', u'4 a 10 d\xedas', u'NO', u'ALTAS VOZ', u'21-Jan-17', u'En Tiempo', u'TELMEX', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41551806, u'A4', 5554237559, u'ROMO MORALES ESPERANZA', u'PS', u'1/6/2017', 12, 9, u'SL_', u'SL_0142', u'', u'API', u'MIXCOAC', u'MIC', u'SLI', u'CAS', u'1/9/2017', 10, u'R5', u'MIXCOAC', u'C-', u'C+', 1, 0, 0, 0, u'LOMAS DE TARANGO', u'METRO', u'METRO SUR', u'MIX', 56745569, u'A410PBDPI', u'ASIGNADO', u'MORENO CRUZ JOSE ARMANDO', 8523039, u'SL_SL_02 INST', 56745569, u'SL_ INST', u'TELMEX', u'EDIFICIO', u'SANTA LUCIA', u'', u'RESIDENCIAL', u'RESIDENCIAL', 0, u'', 0, u'1 Play', 7, u'11 a 25 d\xedas', u'4 a 10 d\xedas', u'NO', u'ALTAS VOZ', u'22-Jan-17', u'En Tiempo', u'TELMEX', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41559671, u'TV', 5555955143, u'CORRALES AYALA RAFAEL', u'KC', u'1/6/2017', 12, 1, u'OV_', u'OV_0004', u'', u'WMX', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'1/17/2017', u'1L', u'R6', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 0, u'OLIVAR DE LOS PADRES', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONTENEDOR', u'SAN JERONIMO', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'1 Play Inf', 6, u'11 a 25 d\xedas', 1, u'NO', u'TV', u'', u'', u'FUERA', u'', u'', u'-', ''], [41561840, u'A9', 5552771052, u'VILLEGAS CAMPOS ROCIO', u'PS', 42741, 12, 4, u'TY_', u'TY_0167', u'', u'LO', u'MIXCOAC', u'VAL', u'TYB', u'TYB', 42749, u'1L', u'TC', u'MIXCOAC', u'C-', u'D+', 0, 0, 0, 0, u'LOMAS DE BECERRA GRANADA', u'METRO', u'METRO SUR', u'MIX', 56723358, u'A91LPXT', u'PENDIENTE', u'', u'.', u'TY_TY_01 INST', 56723358, u'TY_ INST', u'', u'EDIFICIO', u'TACUBAYA', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'', 0, u'2 Play Res', 4, u'11 a 25 d\xedas', u'4 a 10 d\xedas', u'NO', u'ALTAS INF', u'', u'', u'NO ASIGNADO', u'', u'', u'JUDA CONSTRUCCIONES SA DE CV', ''], [41562751, u'D2', 5555209610, u'GRUPO ICA', u'XO', 42741, 12, 1, u'TY_', u'TY_0244', u'', u'AC3', u'MIXCOAC', u'VAL', u'TYB', u'TYB', 42752, u'2L', u'N', u'MIXCOAC', u'CM', u'C+', 1, 0, 0, 1, u'ESCANDON', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'MIXCOAC', u'MIXCOAC', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 1, u'', 0, u'Cambio Domicilio', 2, u'11 a 25 d\xedas', 1, u'NO', u'CD INF', u'', u'', u'FUERA', u'', u'', u'-', ''], [41562356, u'D2', 5552761672, u'GRUPO ICA SA DECV', u'XO', 42741, 12, 1, u'TY_', u'TY_0244', u'', u'LO', u'MIXCOAC', u'VAL', u'TYB', u'TYB', 42752, 20, u'N', u'MIXCOAC', u'CM', u'C+', 1, 0, 0, 1, u'ESCANDON', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'MIXCOAC', u'MIXCOAC', u'NO RESIDENCIAL', u'COMERCIAL', 1, u'', 0, u'Cambio Domicilio', 2, u'11 a 25 d\xedas', 1, u'NO', u'CD VOZ', u'', u'', u'FUERA', u'', u'', u'-', ''], [41568827, u'D2', 5555503874, u'SANCHEZ COS MARIA ROSA', u'PS', u'1/7/2017', 11, 10, u'SA_', u'SA_0023', u'', u'WFC', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/8/2017', u'1L', u'R1', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 1, u'SAN ANGEL INN', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'CORREDOR INSURGENTES', u'CORREDOR INSURGENTES', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'Cambio Domicilio', 2, u'11 a 25 d\xedas', u'4 a 10 d\xedas', u'NO', u'CD INF', u'15-Jan-17', u'En Tiempo', u'ASISTENCIA', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41571060, u'TV', 5556529292, u'ELIZALDE DI MARTINO CARINA MAR', u'V2', u'1/7/2017', 11, 1, u'PD_', u'PD_0055', u'', u'PC', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/17/2017', u'1L', u'R6', u'MIXCOAC', u'C-', u'C', 0, 0, 0, 0, u'BARRIO SAN FRANCISCO', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONCENTRADOR', u'PEDREGAL', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'1 Play Inf', 6, u'11 a 25 d\xedas', 1, u'NO', u'TV', u'26-Jan-17', u'En Tiempo', u'FUERA', u'CARLOS AGUILAR OCHIQUI', u'UNINET', u'-', ''], [41569116, u'TV', 5555247703, u'HERNANDEZ VELAZQUEZ JESUS ALBE', u'PS', u'1/7/2017', 11, 11, u'GI_', u'GI_0096', u'', u'TKE', u'MIXCOAC', u'MIC', u'MIC', u'CAS', u'1/7/2017', u'1L', u'R5', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 1, u'FLORIDA', u'METRO', u'METRO SUR', u'MIX', 56730107, u'TV1LPBGPI', u'ASIGNADO', u'FILIAL_ITCR_DOMNGO G JOSE_MI', 2610227, u'MI_GI_02 INST', 56730107, u'MI_ INST', u'ITCR', u'EDIFICIO', u'CORREDOR INSURGENTES', u'CORREDOR INSURGENTES', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'1 Play Inf', 6, u'11 a 25 d\xedas', u'11 a 25 d\xedas', u'NO', u'TV', u'12-Jan-17', u'Fuera de Tiempo', u'ITCR', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41567904, u'A4', 5517134191, u'GONZALEZ JIMENEZ ERIKA', u'PS', u'1/7/2017', 11, 11, u'', u'', u'', u'WTM', u'MIX', u'MIC', u'SLI', u'CAS', u'1/7/2017', 10, u'R6', u'MIXCOAC', u'', u'', 0, 0, 0, 0, u'', u'METRO', u'METRO SUR', u'MIX', 56730070, u'A410PBDPI', u'ASIGNADO', u'MORENO CRUZ JOSE ARMANDO', 8523039, u'SL_RX_01 INST', 56730070, u'SL_ INST', u'TELMEX', u'NO IDENTIFICADO', u'', u'', u'RESIDENCIAL', u'RESIDENCIAL', 0, u'', 0, u'1 Play', 7, u'11 a 25 d\xedas', u'11 a 25 d\xedas', u'NO', u'ALTAS VOZ', u'16-Jan-17', u'En Tiempo', u'TELMEX', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41611369, u'A9', 5555688087, u'ADOLFO GUTIERREZ MARROQUIN', u'PO', u'1/9/2017', 9, 1, u'PD_', u'PD_0054', u'', u'TMC', u'MIXCOAC', u'LOR', u'MIC', u'CAS', 42752, u'2L', u'R6', u'MIXCOAC', u'', u'C+', 1, 0, 0, 0, u'', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONCENTRADOR', u'PEDREGAL', u'', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 0, u'', 0, u'2 Play Com', 3, u'8 a 10 d\xedas', 1, u'NO', u'ALTAS INF', u'14-Jan-17', u'Fuera de Tiempo', u'FUERA', u'ANDRES HDZ', u'CCR', u'-', ''], [41606954, u'A0', 5567230990, u'BALCARCEL DOMINGUEZ JORGE RAMO', u'E9', u'1/9/2017', 9, 1, u'PD_', u'PD_0113', u'', u'WTG', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/17/2017', u'2L', u'', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 0, u'JARDINES DEL PEDREGAL', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONCENTRADOR', u'PEDREGAL', u'', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 1, u'AXTEL            ', 1, u'Portabilidad', 1, u'8 a 10 d\xedas', 1, u'NO', u'ALTAS INF', u'22-Jan-17', u'En Tiempo', u'FUERA', u'CENTRAL', u'CENTRAL', u'-', ''], [41603595, u'A9', 5555503360, u'PPP INNOVATION CORPORATE SA DE', u'PO', u'1/9/2017', 9, 1, u'SA_', u'SA_0033', u'', u'LO', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/17/2017', u'2L', u'R5', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 1, u'SAN ANGEL INN', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'CORREDOR INSURGENTES', u'CORREDOR INSURGENTES', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 1, u'', 0, u'2 Play Com', 3, u'8 a 10 d\xedas', 1, u'NO', u'ALTAS INF', u'22-Jan-17', u'En Tiempo', u'FUERA', u'ANDRES HDZ', u'CCR', u'-', ''], [41600241, u'A9', 5555502941, u'GUERRERO MUZQUIZ NAVARRO DULCE', u'E3', u'1/9/2017', 9, 1, u'SA_', u'SA_0023', u'', u'WFC', u'MIXCOAC', u'LOR', u'MIC', u'CAS', 42752, u'1L', u'CP', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 1, u'SAN ANGEL INN', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'CORREDOR INSURGENTES', u'CORREDOR INSURGENTES', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'2 Play Res', 4, u'8 a 10 d\xedas', 1, u'NO', u'ALTAS INF', u'22-Jan-17', u'En Tiempo', u'FUERA', u'CENTRAL', u'CENTRAL', u'-', ''], [41599837, u'A0', 5521244227, u'HERNANDEZ GONZALEZ MARIA DEL R', u'PS', u'1/9/2017', 9, 9, u'GI_', u'GI_0101', u'', u'UN', u'MIXCOAC', u'MIC', u'MIC', u'CAS', u'1/9/2017', 10, u'', u'MIXCOAC', u'C-', u'A/B', 1, 0, 0, 0, u'PUEBLO AXOTLA', u'METRO', u'METRO SUR', u'MIX', 56742138, u'A010PBG', u'ASIGNADO', u'FILIAL_ITCR_DOMNGO G JOSE_MI', 2610227, u'MI_GI_02 INST', 56742138, u'MI_ INST', u'ITCR', u'EDIFICIO', u'SAN JOSE INSURGENTES', u'', u'RESIDENCIAL', u'RESIDENCIAL', 1, u'', 0, u'1 Play', 7, u'8 a 10 d\xedas', u'4 a 10 d\xedas', u'NO', u'ALTAS VOZ', u'21-Jan-17', u'En Tiempo', u'ITCR', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41594194, u'A0', 5515184181, u'JACUINDE CORTES RAFAEL', u'PS', u'1/9/2017', 9, 1, u'BN_', u'BN_0001', u'', u'MI', u'MIXCOAC', u'MIC', u'MIC', u'TYB', u'1/17/2017', 10, u'', u'MIXCOAC', u'C-', u'D+', 0, 0, 0, 0, u'BARRIO NORTE', u'METRO', u'METRO SUR', u'MIX', 56832349, u'A010PBD', u'ASIGNADO', u'CIMAQSA_BOLSA NUEVA COPE MI', 2220100, u'MI_MI_04 INST', 56832349, u'MI_ INST', u'CIMAQSA', u'BANQUETERO', u'SANTA LUCIA', u'', u'RESIDENCIAL', u'RESIDENCIAL', 0, u'', 0, u'1 Play', 7, u'8 a 10 d\xedas', 1, u'NO', u'ALTAS VOZ', u'22-Jan-17', u'En Tiempo', u'CIMAQSA', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41606961, u'D3', 5556682213, u'ALVAREZ RONQUILLO ELIZABETH', u'S2', u'1/9/2017', 9, 2, u'PD_', u'PD_0031', u'', u'WVH', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/16/2017', u'1L', u'R4', u'MIXCOAC', u'A+', u'A/B', 1, 0, 1, 0, u'FUENTES DEL PEDREGAL', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONCENTRADOR', u'PEDREGAL', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'Cambio Domicilio', 2, u'8 a 10 d\xedas', 2, u'NO', u'CD INF', u'', u'', u'FUERA', u'VICTOR MANOATH ESQUIVEL', u'SISTEMAS COMERCIALES', u'-', ''], [41605467, u'D2', 5555503609, u'OPERADORA DE FAST FOOD CHINO S', u'PS', u'1/9/2017', 9, 1, u'GI_', u'GI_0192', u'', u'AC4', u'MIXCOAC', u'MIC', u'MIC', u'CAS', u'1/17/2017', u'2L', u'CE', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 0, u'GUADALUPE INN', u'METRO', u'METRO SUR', u'MIX', 56752449, u'D22LPADPI', u'PENDIENTE', u'', u'.', u'MI_GI_01 INST', 56752449, u'MI_CTLS', u'', u'EDIFICIO', u'CORREDOR INSURGENTES', u'CORREDOR INSURGENTES', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 1, u'', 0, u'Cambio Domicilio', 2, u'8 a 10 d\xedas', 1, u'SI', u'CD INF', u'', u'', u'NO ASIGNADO', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41601007, u'D2', 5591552074, u'GOMEZ GALAZ RODRIGO DE JESUS', u'PS', u'1/9/2017', 9, 5, u'PD_', u'PD_0042', u'', u'PC', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/13/2017', u'1L', u'R5', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 0, u'JARDINES DEL PEDREGAL', u'METRO', u'METRO SUR', u'MIX', 56761130, u'D21LP4DPI', u'ASIGNADO', u'FILIAL_PC_ MIXCOAC MIXCOAC', 2610423, u'MI_PD_04 INST', 56761130, u'MI_ INST', u'PC', u'CONCENTRADOR', u'PEDREGAL', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'Cambio Domicilio', 2, u'8 a 10 d\xedas', u'4 a 10 d\xedas', u'NO', u'CD INF', u'01-Jan-00', u'Sin Programa', u'PC', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41598455, u'D2', 5555687095, u'ARMAS AGUILAR ANA LETICIA', u'ER', u'1/9/2017', 9, 1, u'PD_', u'PD_0027', u'', u'API', u'MIXCOAC', u'LOR', u'MIC', u'CAS', 42752, u'1L', u'R2', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 0, u'JARDINES DEL PEDREGAL', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONCENTRADOR', u'PEDREGAL', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'Cambio Domicilio', 2, u'8 a 10 d\xedas', 1, u'NO', u'CD INF', u'01-Jan-00', u'Sin Programa', u'FUERA', u'CENTRAL', u'CENTRAL', u'-', ''], [41592143, u'D2', 5556899961, u'HERNANDEZ LOPEZ ROSA MARIA', u'ER', u'1/9/2017', 9, 1, u'GI_', u'GI_0075', u'', u'LO', u'MIXCOAC', u'MIC', u'MIC', u'CAS', 42752, 10, u'R6', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 0, u'GUADALUPE INN', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'EDIFICIO', u'CORREDOR INSURGENTES', u'CORREDOR INSURGENTES', u'RESIDENCIAL', u'RESIDENCIAL', 1, u'', 0, u'Cambio Domicilio', 2, u'8 a 10 d\xedas', 1, u'NO', u'CD VOZ', u'27-Jan-17', u'En Tiempo', u'FUERA', u'CENTRAL', u'CENTRAL', u'-', ''], [41608367, u'TV', 5559083029, u'MIGUEL GALVAN MARIA MAGDALENA', u'PS', u'1/9/2017', 9, 6, u'PD_', u'PD_0022', u'', u'LO', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/12/2017', u'1L', u'R5', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 0, u'JARDINES DEL PEDREGAL', u'METRO', u'METRO SUR', u'MIX', 56748222, u'TV1LPBGPE', u'ASIGNADO', u'AZ_FILIAL_FO_UNE ALFONSO ARENAS', 2220660, u'AZ_PO_02_MIXTO', 56748222, u'AZ_MIXTO', u'UNE', u'CONCENTRADOR', u'PEDREGAL', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 1, u'', 0, u'1 Play Inf', 6, u'8 a 10 d\xedas', u'4 a 10 d\xedas', u'NO', u'TV', u'26-Jan-17', u'En Tiempo', u'UNE', u'PLANTA', u'OPERACI\xd3N', u'-', ''], [41605993, u'TI', 5556528171, u'SERVS GASTRONOMICOS MONT ALCE', u'PS', u'1/9/2017', 9, 9, u'PD_', u'PD_0006', u'', u'WTG', u'MIXCOAC', u'LOR', u'MIC', u'CAS', u'1/9/2017', u'2L', u'C-', u'MIXCOAC', u'A+', u'A/B', 1, 0, 0, 0, u'JARDINES DEL PEDREGAL', u'METRO', u'METRO SUR', u'MIX', 56746401, u'TI2LPBF', u'ASIGNADO', u'FILIAL CIMAQSA_ GARCIA NIETO FCO_MI', 2220112, u'MI_PD_03 INST', 56746401, u'MI_ INST', u'CIMAQSA', u'CONCENTRADOR', u'PEDREGAL', u'', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 1, u'', 0, u'TI', 8, u'8 a 10 d\xedas', u'4 a 10 d\xedas', u'NO', u'TI', u'19-Jan-17', u'En Tiempo', u'CIMAQSA', u'PLANTA', u'OPERACI\xd3N', u'-', u'FO'], [41605194, u'A0', 5527930281, u'ALFARO APANCO MARIA GUADALUPE', u'C4', u'1/9/2017', 9, 1, u'TU_', u'TU_0009', u'', u'WFC', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'1/17/2017', u'1L', u'R6', u'MIXCOAC', u'C-', u'D+', 0, 0, 1, 0, u'EL OCOTAL', u'METRO', u'METRO SUR', u'MIX', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'CONCENTRADOR', u'SAN JERONIMO', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'TELMEX           ', 1, u'Portabilidad', 1, u'8 a 10 d\xedas', 1, u'NO', u'ALTAS INF', u'22-Jan-17', u'En Tiempo', u'FUERA', u'TIENDAS', u'COMERCIAL', u'MARNA IMAGEN CREATIVA SA DE CV', ''], [41603950, u'A9', 5517185859, u'X NAJERA MARTHA', u'PS', u'1/9/2017', 9, 8, u'BB_', u'BB_0003', u'', u'WFC', u'MIXCOAC', u'LOR', u'SLI', u'CAS', u'1/10/2017', u'1L', u'', u'MIXCOAC', u'C-', u'C+', 1, 0, 0, 0, u'LOMAS DE SAN BERNABE', u'METRO', u'METRO SUR', u'MIX', 56745974, u'A91LP4D', u'ASIGNADO', u'ITCR_BOLSA NUEVA, COPE SL', 2220120, u'SL_BB_01 INST', 56745974, u'SL_ INST', u'ITCR', u'CONTENEDOR', u'SAN JERONIMO', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'', 0, u'2 Play Res', 4, u'8 a 10 d\xedas', u'4 a 10 d\xedas', u'NO', u'ALTAS INF', u'08-Jan-17', u'Fuera de Tiempo', u'ITCR', u'PLANTA', u'OPERACI\xd3N', u'JUDA CONSTRUCCIONES SA DE CV', ''], [41603070, u'A9', 5550359256, u'RONQUILLO CERVANTES ALEJANDRO', u'PS', u'1/9/2017', 9, 7, u'EY_', u'EY_0002', u'', u'MI', u'MIXCOAC', u'MIC', u'SLI', u'CAS', u'1/11/2017', u'1L', u'', u'MIXCOAC', u'C-', u'C+', 1, 0, 0, 1, u'PRESIDENTES', u'METRO', u'METRO SUR', u'MIX', 56778524, u'A91LPBG', u'ASIGNADO', u'FILIAL_UNE_ SL', 2610222, u'SL_EY_01 INST', 56778524, u'SL_ INST', u'UNE', u'CONTENEDOR', u'SANTA LUCIA', u'', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'', 0, u'2 Play Res', 4, u'8 a 10 d\xedas', u'4 a 10 d\xedas', u'NO', u'ALTAS INF', u'08-Jan-17', u'Fuera de Tiempo', u'UNE', u'PLANTA', u'OPERACI\xd3N', u'JUDA CONSTRUCCIONES SA DE CV', ''], [41601634, u'A9', 5510560687, u'SSID HI SA DE CV', u'PS', u'1/9/2017', 9, 8, u'AI_', u'AI_0020', u'', u'ACP', u'MIXCOAC', u'MIC', u'SLI', u'CAS', u'1/10/2017', u'2L', u'R6', u'MIXCOAC', u'C-', u'C', 0, 0, 0, 0, u'SAN CLEMENTE', u'METRO', u'METRO SUR', u'MIX', 56744760, u'A92LP4S', u'ASIGNADO', u'ITCR_BOLSA NUEVA, COPE SL', 2220120, u'SL_AI_03 INST', 56744760, u'SL_ INST', u'ITCR', u'CONCENTRADOR', u'SAN JERONIMO', u'', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 0, u'', 0, u'2 Play Com', 3, u'8 a 10 d\xedas', u'4 a 10 d\xedas', u'NO', u'ALTAS INF', u'18-Jan-17', u'En Tiempo', u'ITCR', u'PLANTA', u'OPERACI\xd3N', u'-', '']]
#     pos_field_id = get_pos_field_id_dict(header, 10540, cope=cope)
#     pre_os_field_id = get_pos_field_id_dict(header, 11149, cope=cope)
#     create_record(pos_field_id, pre_os_field_id, records, header)
#



#upload_test()
upload_bolsa()
