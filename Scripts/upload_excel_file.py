#####
# Made by Jose Patricio VM
#####
# Script para generar pacos a partir de ordenes de Servicio de PCI Industrial
#
#
#####
import wget
import pyexcel
import datetime, time, re
from sys import argv


from linkaform_api import settings
from linkaform_api import network, utils

mongo_hosts = 'db2.linkaform.com:27017,db3.linkaform.com:27017,db4.linkaform.com:27017'
#mongo_hosts = "127.0.0.1"
mongo_replicaSet = 'linkaform_replica'
MONGO_READPREFERENCE='primary'

MAX_POOL_SIZE = 50
WAIT_QUEUE_TIMEOUT = 1000
MONGODB_URI = 'mongodb://%s/?replicaSet=%s&readPreference=%s'%(mongo_hosts, mongo_replicaSet, MONGO_READPREFERENCE)

lkf_api = utils.Cache()


config = {
    'USERNAME' : 'ricardo.teja@servipro.com.mx',
    #'USERNAME' : 'josepato@infosync.mx',
    'PASS' : '123456',
    'COLLECTION' : 'form_answer',
    #'HOST' : 'db3.linkaform.com',
    'MONGODB_URI':MONGODB_URI,
    #'MONGODB_PASSWORD': mongodb_password_here
    'PORT' : 27017,
    'USER_ID' : 769,
    'KEYS_POSITION' : {},
    'IS_USING_APIKEY' : False,
    'AUTHORIZATION_EMAIL_VALUE' : 'ricardo.teja@servipro.com.mx',
    'AUTHORIZATION_TOKEN_VALUE' : 'f8696545c6bd91b0b53aec83d3129be5d1d699fb',
}


settings.config = config
cr = network.get_collections()

#Nombre del campo en la la Forma: Nombre en el Archvio
equivalcens_map = {'Clase de Servicio':'CLASE_SERV',
                    'Fecha Contratada':'F_CONTRATA',
                    'Estatus':'ESTATUS de Orden',
                    'Metros Bajante':'MTS. BAJANTE (PARALELO)',
                    'Tipo de Tarea':'tipo',
                    'Tipo de Tarea': 'TIPO TAREA',
                    'Dilacion':'Dilacion',
                    'Expediente':'EXP. TEC.',
                    'Expediente':'EXPEDIENTE'}


def read_file(file_url='', file_name=''):
    #sheet = pyexcel.get_sheet(file_name="bolsa.xlsx")
    if file_name:
        sheet = pyexcel.get_sheet(file_name = file_name)
    if file_url:
        sheet = pyexcel.get_sheet(url = file_url)
    records = sheet.array
    header = records.pop(0)
    return header, records


def download_file(url):
    fileb = wget.download(url)
    return fileb


def convert_to_epoch(strisodate):
    if type(strisodate) == datetime.date or type(strisodate) == datetime.datetime:
        return time.mktime(strisodate.timetuple())
    strisodate2 = re.sub(' ','',strisodate)
    strisodate2 = strisodate2.split(' ')[0]
    try:
        date_object = datetime.strptime(strisodate2, '%Y-%m-%d')
    except ValueError:
        date_object = datetime.strptime(strisodate2[:8],  '%d/%m/%y')
    return int(date_object.strftime("%s"))


def convert_to_sting_date(strisodate):
    if type(strisodate) == datetime.date:
        return strisodate
    strisodate2 = re.sub(' ','',strisodate)
    strisodate2 = strisodate2.split(' ')[0]
    try:
        date_object = datetime.strptime(strisodate2, '%Y-%m-%d')
    except ValueError:
        try:
            date_object = datetime.strptime(strisodate2[:10],  '%d/%m/%Y')
        except ValueError:
            date_object = datetime.strptime(strisodate2[:8],  '%d/%m/%y')
    return date_object.strftime('%Y-%m-%d')


def get_element_dict(field):
    res = {'field_id':field['field_id'], 'field_type':field['field_type'], 'label':field['label'], 'options':field['options']}
    if field.has_key('group') and field['group']:
        res['group_id'] = field['group']['group_id']
    return res


def make_header_dict(header):
    header_dict = {}
    for position in range(len(header)):
        content = header[position].encode('utf-8')
        header_dict[str(content).lower().replace(' ' ,'')] = position
    return header_dict


def get_pos_field_id_dict(header, form_id):
    #form_id=10378 el id de bolsa
    #pos_field_id ={3: {'field_type': 'text', 'field_id': '584648c8b43fdd7d44ae63d1'}, 9: {'field_type': 'text', 'field_id': '58464a29b43fdd773c240163'}, 51: {'field_type': 'integer', 'field_id': '584648c8b43fdd7d44ae63d0'}}
    #return pos_field_id
    pos_field_id = {}
    #print 'form_id', form_id
    form_fields = lkf_api.get_form_id_fields(form_id)
    #print 'form_fields=', form_fields
    if not form_fields:
        raise ValueError('No data form FORM')
    header_dict = make_header_dict(header)
    if len(form_fields) > 0:
        fields = form_fields[0]['fields']
        fields_json = {}
        if 'folio' in header_dict.keys():
            pos_field_id[header_dict['folio']] = {'field_type':'folio'}
        for field in fields:
            label = field['label'].lower().replace(' ' ,'')
            label_underscore = field['label'].lower().replace(' ' ,'_')
            if label in header_dict.keys():
                pos_field_id[header_dict[label]] = get_element_dict(field)
            elif label_underscore in header_dict.keys():
                pos_field_id[header_dict[label_underscore]] = get_element_dict(field)
            elif field['label'] in equivalcens_map.keys():
                header_lable = equivalcens_map[field['label']]
                header_lable = header_lable.lower().replace(' ' ,'')
                if header_lable in header_dict.keys():
                    pos_field_id[header_dict[header_lable]] = get_element_dict(field)
    return pos_field_id


def addMultipleChoice(answer, element):
    return True


def set_custom_values(pos_field_id, record):
    custom_answer = {}
    #set status de la orden
    #custom_answer['f1054000a030000000000002'] = 'por_asignar'
    return custom_answer


def update_metadata_from_record(header, record):
    res = {}
    if 'created_at' in header.keys():
        pos = header['created_at']
        if record[pos]:
            #res['created_at'] = convert_to_sting_date(record[pos])
            res['created_at'] = convert_to_epoch(record[pos])
    if 'form_id' in header.keys():
        pos = header['form_id']
        if record[pos]:
            res['form_id'] = record[pos]
    return res


def get_nongroup_fields(pos_field_id):
    res = []
    for pos, element in pos_field_id.iteritems():
        if element.has_key('group_id') and element['group_id']:
            continue
        else:
            res.append(pos)
    return res

def check_record_is_group_iterration(non_group_fields, record):
    for pos in non_group_fields:
        if record[pos]:
            return False
    return True

def create_record(pos_field_id, form_id, records, header):
    records_to_upload = []
    metadata = lkf_api.get_metadata(form_id=form_id, user_id=settings.config['USER_ID'] )
    header_dict = make_header_dict(header)
    non_group_fields = get_nongroup_fields(pos_field_id)
    for record in records:
        is_group_iteration = check_record_is_group_iterration(non_group_fields, record)
        metadata.update(update_metadata_from_record(header_dict, record))
        cont = False
        answer = {}
        this_record = {}
        count = 0
        this_record.update(metadata)
        group_iteration = {}
        for pos, element in pos_field_id.iteritems():
            count +=1
            print 'count', count
            if element['field_type'] == 'folio':
                this_record['folio'] = str(record[pos])
            else:
                element_answer = lkf_api.make_infosync_json(record[pos], element)
                if element.has_key('group_id') and element['group_id'] and element_answer:
                    if not answer.has_key(element['group_id']):
                        answer[element['group_id']] = []
                    #answer.update(element_answer)
                    if not group_iteration.has_key(element['group_id']):
                        group_iteration[element['group_id']] = {}
                    group_iteration[element['group_id']].update(element_answer)
                else:
                    answer.update(element_answer)
        #answer[element['group_id']].append(group_iteration)
        answer.update(set_custom_values(pos_field_id, record ))
        if is_group_iteration:
            last_rec = records_to_upload[-1]
            #print 'last_rec',last_rec

            for group_id  in group_iteration.keys():
                last_rec['answers'][group_id].append(group_iteration[group_id])
            records_to_upload[-1] = last_rec
        else:
            for group_id  in group_iteration.keys():
                answer[group_id].append(group_iteration[group_id])
            this_record["answers"] = answer
            records_to_upload.append(this_record)
    #for rec in  records_to_upload:
    #    network.post_forms_answers(rec)
    network.post_forms_answers_list(records_to_upload)
    return True


def upload_file(file_url='', file_name='', form_id=None):
    if not form_id:
        raise ValueError('Must specify form id')
    if not file_url and not file_name:
        raise ValueError('Must specify either one, file_url or file_name')
    if file_url:
        header, records = read_file(file_url=file_url)
    elif file_name:
        header, records = read_file(file_name=file_name)
    pos_field_id = get_pos_field_id_dict(header, form_id)
    create_record(pos_field_id, form_id, records, header)


def print_help():
    print '---------------- HELP --------------------------'
    print 'more arguments needed'
    print 'the script should be run like this'
    print 'python upload_excel_file.py "**file_name:/tmp/personal.xlsx"  *1234'
    print '** file_name: para un archivo local'
    print '** file_url: para un archivo remoto'
    print '* donde 1234 es el id de la forma'


if __name__ == "__main__":
    print 'args= ', argv
    if len(argv) > 2:
        file_type = argv[1].split(':')[0]
        if file_type == 'help' or 'file_type' == '--help':
            print_help()
        file_url = False
        file_name = False
        if file_type == 'file_url':
            file_url =  argv[1].split(':')[1]
        if file_type == 'file_name':
            file_name =  argv[1].split(':')[1]
        form_id = argv[2]
        upload_file(file_url, file_name, form_id)
    else:
        print_help()
