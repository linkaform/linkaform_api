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

from script_get_ordenes_liquidadas import *

mongo_hosts = 'db2.linkaform.com:27017,db3.linkaform.com:27017,db4.linkaform.com:27017'
#mongo_hosts = "127.0.0.1"
mongo_replicaSet = 'linkaform_replica'
MONGO_READPREFERENCE='primary'

MAX_POOL_SIZE = 50
WAIT_QUEUE_TIMEOUT = 1000
MONGODB_URI = 'mongodb://%s/?replicaSet=%s&readPreference=%s'%(mongo_hosts, mongo_replicaSet, MONGO_READPREFERENCE)


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
    'AUTHORIZATION_EMAIL_VALUE' : 'jgemayel@pcidustrial.com.mx',
    'AUTHORIZATION_TOKEN_VALUE' : '1a84bab48214997eced5b1baa7b0bb24a4058672',
}


settings.config = config
cr = network.get_collections()

#Nombre del campo en la la Forma: Nombre en el Archvio
equivalcens_map = {'Clase de Servicio':'CLASE_SERV',
                    'Fecha Contratada':'F_CONTRATA',
                    'Estatus':'ESTATUS de Orden'}


def read_file(file_url):
    #sheet = pyexcel.get_sheet(file_name="bolsa.xlsx")
    sheet = pyexcel.get_sheet(url = file_url)
    records = sheet.array
    header = records.pop(0)
    return header, records


def download_file(url):
    fileb = wget.download(url)
    print 'fileb', fileb
    return fileb


def get_element_dict(field):
    return {'field_id':field['field_id'], 'field_type':field['field_type'], 'label':field['label']}


def get_pos_field_id_dict(header, form_id=10540):
    #form_id=10378 el id de bolsa
    #pos_field_id ={3: {'field_type': 'text', 'field_id': '584648c8b43fdd7d44ae63d1'}, 9: {'field_type': 'text', 'field_id': '58464a29b43fdd773c240163'}, 51: {'field_type': 'integer', 'field_id': '584648c8b43fdd7d44ae63d0'}}
    #return pos_field_id
    pos_field_id = {}
    form_fields = lkf_api.get_form_id_fields(form_id)
    header_dict = {}
    for position in range(len(header)):
        header_dict[str(header[position]).lower().replace(' ' ,'')] = position
    #print 'form_fields=', form_fields
    if len(form_fields) > 0:
        fields = form_fields[0]['fields']
        #print 'keys', fields
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

#print 'starting get form ids'
#header= [u'FOLIO', u'TIPO', u'TELEFONO', u'NOMBRE', u'ETAPA', u'F_CONTRATA', u'DILACION', u'DILETAPA', u'Central', u'DISTRITO', u'CANAL', u'OF_C', u'AREA', u'OFICINA', u'CT', u'CM', u'F_UE', u'CLASE_SERV', u'SEGMENTO', u'area_ct', u'segpred', u'nse_amai', u'abc', u'elite', u'sky', u'warzone', u'colonia', u'DIVISION', u'SUBDIRECCION', u'SIGLAS', u'Fol_Pisaplex', u'TTarea', u'Degustacion', u'NombreTecnico', u'Expediente', u'Zona', u'IdTarea', u'GrupoAsignacion', u'RedPri', u'RedSec', u'DispositivoCoordenada', u'Empresa', u'Tipo_Sitio', u'Poligono-Zona', u'Prioritaria', u'resynores', u'AgrupaR27', u'FTTH', u'VieneDe', u'Portabilidad', u'Etiqueta', u'Prioridad', u'AgrupaDil', u'AgrupaDilEtapa', u'Pendiente_Puente', u'PRODUCTO', u'CTL', u'EMPRESA*', u'FECHA ASIGNADA', u'DIL2', u'ESTADO', u'SITIO', u'ETIQUETA2', u'RANGO', u'PRIORIDAD2', u'ATIENDE', u'FACTIBILIDAD', u'COLONIA2']
#get_pos_field_id_dict(header, 6015)

def addMultipleChoice(answer, element):
    return True


def set_custom_values(pos_field_id, record):
    custom_answer = {}
    #set status de la orden
    #custom_answer['f1054000a030000000000002'] = 'abierta'
    return custom_answer


def create_record(pos_field_id, records):
    answer = {}
    metadata = lkf_api.get_metadata(form_id=10540, user_id=settings.config['USER_ID'] )
    for record in records:
        count = 0
        for pos, element in pos_field_id.iteritems():
            count +=1
            answer.update(lkf_api.make_infosync_json(record[pos], element))
            if element['field_type'] == 'folio':
                metadata['folio'] = str(record[pos])
        answer.update(set_custom_values(pos_field_id, record ))
        metadata["answers"] = answer
        network.post_forms_answers([metadata,])
        print '=========================================='
    return True


def upload_bolsa():
    files = get_files2upload()
    #files = [{u'_id': ('58575ff4b43fdd35e3169665'), u'answers': {u'f1074100a010000000000001': {u'file_name': u'BASE 16-DICIEMBRES10.xls', u'file_url': u'uploads/1259_jgemayel@pcindustrial.com.mx/e201093c634a2a2ff2068b4df622401a2ac90c83.xls'}}}]
    if files:
        for file_url in files:
            if file_url.has_key('answers') and file_url['answers'].has_key('f1074100a010000000000001'):
                if file_url['answers']['f1074100a010000000000001'].has_key('file_url'):
                    url = file_url['answers']['f1074100a010000000000001']['file_url']
                    #print 'URL', url
                    if url.find('https') == -1:
                        url = 'https://app.linkaform.com/media/' + url
                    header, records = read_file(url)
                    #records = get_rr()
                    pos_field_id = get_pos_field_id_dict(header)
                    print 'pos_field_id=', pos_field_id

                    create_record(pos_field_id, records)
                else:
                    print 'no file found'
            else:
                print 'no recored found'

upload_bolsa()
