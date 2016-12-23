#####
# Made by Jose Patricio VM
#####
# Script para generar pacos a partir de ordenes de Servicio de PCI Industrial
#
#
#####
import wget
import pyexcel

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
    'USERNAME' : 'jgemayel@pcindustrial.com.mx',
    'PASS' : '123456',
    'COLLECTION' : 'form_answer',
    #'HOST' : 'db3.linkaform.com',
    'MONGODB_URI':MONGODB_URI,
    #'MONGODB_PASSWORD': mongodb_password_here
    'PORT' : 27017,
    'USER_ID' : '1259',
    'KEYS_POSITION' : {},
    'IS_USING_APIKEY' : True,
    'AUTHORIZATION_EMAIL_VALUE' : 'jgemayel@pcindustrial.com.mx',
    'AUTHORIZATION_TOKEN_VALUE' : '74e5455a43b175acc93b3cc72be0ea74c2212ca5',
}

settings.config = config
cr = network.get_collections()

def query_get_files():
    query = {'form_id': {'$in': [10741]}, 'deleted_at' : {'$exists':False}, 'answers.f1074100a010000000000005': 'por_cargar'}
    select_columns = {'answers.f1074100a010000000000001':1}
    return query, select_columns



def get_files2upload():
    query, select_columns = query_get_files()
    orders_records = cr.find(query, select_columns)
    print 'order find', orders_records.count()
    return orders_records


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


def get_form_ids_json(header, form_id=10741):
    form_fields = lkf_api.get_form_id_fields(form_id)
    print 'form_fields', form_fields
    print stop

print 'starting get form ids'
header= [u'FOLIO', u'TIPO', u'TELEFONO', u'NOMBRE', u'ETAPA', u'F_CONTRATA', u'DILACION', u'DILETAPA', u'Central', u'DISTRITO', u'CANAL', u'OF_C', u'AREA', u'OFICINA', u'CT', u'CM', u'F_UE', u'CLASE_SERV', u'SEGMENTO', u'area_ct', u'segpred', u'nse_amai', u'abc', u'elite', u'sky', u'warzone', u'colonia', u'DIVISION', u'SUBDIRECCION', u'SIGLAS', u'Fol_Pisaplex', u'TTarea', u'Degustacion', u'NombreTecnico', u'Expediente', u'Zona', u'IdTarea', u'GrupoAsignacion', u'RedPri', u'RedSec', u'DispositivoCoordenada', u'Empresa', u'Tipo_Sitio', u'Poligono-Zona', u'Prioritaria', u'resynores', u'AgrupaR27', u'FTTH', u'VieneDe', u'Portabilidad', u'Etiqueta', u'Prioridad', u'AgrupaDil', u'AgrupaDilEtapa', u'Pendiente_Puente', u'PRODUCTO', u'CTL', u'EMPRESA*', u'FECHA ASIGNADA', u'DIL2', u'ESTADO', u'SITIO', u'ETIQUETA2', u'RANGO', u'PRIORIDAD2', u'ATIENDE', u'FACTIBILIDAD', u'COLONIA2']
get_form_ids_json(header, 10741)


def upload_bolsa():
    files = get_files2upload()
    if files:
        for file_url in files:
            print 'file_url', file_url
            if file_url.has_key('answers') and file_url['answers'].has_key('f1074100a010000000000001'):
                if file_url['answers']['f1074100a010000000000001'].has_key('file_url'):
                    url = file_url['answers']['f1074100a010000000000001']['file_url']
                    print 'URL', url
                    if url.find('https') == -1:
                        url = 'https://api.linkaform.com/media/' + url
                    print 'url', url
                    #header, records = read_file(url)
                    header= [u'FOLIO', u'TIPO', u'TELEFONO', u'NOMBRE', u'ETAPA', u'F_CONTRATA', u'DILACION', u'DILETAPA', u'Central', u'DISTRITO', u'CANAL', u'OF_C', u'AREA', u'OFICINA', u'CT', u'CM', u'F_UE', u'CLASE_SERV', u'SEGMENTO', u'area_ct', u'segpred', u'nse_amai', u'abc', u'elite', u'sky', u'warzone', u'colonia', u'DIVISION', u'SUBDIRECCION', u'SIGLAS', u'Fol_Pisaplex', u'TTarea', u'Degustacion', u'NombreTecnico', u'Expediente', u'Zona', u'IdTarea', u'GrupoAsignacion', u'RedPri', u'RedSec', u'DispositivoCoordenada', u'Empresa', u'Tipo_Sitio', u'Poligono-Zona', u'Prioritaria', u'resynores', u'AgrupaR27', u'FTTH', u'VieneDe', u'Portabilidad', u'Etiqueta', u'Prioridad', u'AgrupaDil', u'AgrupaDilEtapa', u'Pendiente_Puente', u'PRODUCTO', u'CTL', u'EMPRESA*', u'FECHA ASIGNADA', u'DIL2', u'ESTADO', u'SITIO', u'ETIQUETA2', u'RANGO', u'PRIORIDAD2', u'ATIENDE', u'FACTIBILIDAD', u'COLONIA2']

                    #print 'header=', header
                    form_ids = get_form_ids_json(header)
                    print stop

                else:
                    print 'no file found'
            else:
                print 'no recored found'
        print stop

def create_paco():
    orders = get_orders_ready4paco()

upload_bolsa()
