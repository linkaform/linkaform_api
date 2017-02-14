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
    'USER_ID' : '1259',
    'KEYS_POSITION' : {},
    'IS_USING_APIKEY' : True,
    'AUTHORIZATION_EMAIL_VALUE' : 'jgemayel@pcindustrial.com.mx',
    #'AUTHORIZATION_EMAIL_VALUE' : 'josepato@infosync.mx',
    'AUTHORIZATION_TOKEN_VALUE' : '74e5455a43b175acc93b3cc72be0ea74c2212ca5',
    #'AUTHORIZATION_TOKEN_VALUE' :'76d742df0353da8fd824daae2d158dc146f7eedd'
}

settings.config = config
cr = network.get_collections()

def query_get_files():
    query = {'form_id': {'$in': [10741]}, 'deleted_at' : {'$exists':False}, 'answers.f1074100a010000000000005': 'por_cargar'}
    #select_columns = {'answers.f1074100a010000000000001':1, 'answers.f1074100a0100000000000c1':1}
    select_columns = {'answers':1 }
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
    return fileb


def get_pos_field_id_dict(header, form_id=10540):
    #form_id=10378 el id de bolsa
    #form_id=10540 es el id de la orden light
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
            if label in header_dict.keys():
                pos_field_id[header_dict[label]] = {'field_id':field['field_id'], 'field_type':field['field_type'], 'label':field['label']}
    return pos_field_id

#print 'starting get form ids'
#header= [u'FOLIO', u'TIPO', u'TELEFONO', u'NOMBRE', u'ETAPA', u'F_CONTRATA', u'DILACION', u'DILETAPA', u'Central', u'DISTRITO', u'CANAL', u'OF_C', u'AREA', u'OFICINA', u'CT', u'CM', u'F_UE', u'CLASE_SERV', u'SEGMENTO', u'area_ct', u'segpred', u'nse_amai', u'abc', u'elite', u'sky', u'warzone', u'colonia', u'DIVISION', u'SUBDIRECCION', u'SIGLAS', u'Fol_Pisaplex', u'TTarea', u'Degustacion', u'NombreTecnico', u'Expediente', u'Zona', u'IdTarea', u'GrupoAsignacion', u'RedPri', u'RedSec', u'DispositivoCoordenada', u'Empresa', u'Tipo_Sitio', u'Poligono-Zona', u'Prioritaria', u'resynores', u'AgrupaR27', u'FTTH', u'VieneDe', u'Portabilidad', u'Etiqueta', u'Prioridad', u'AgrupaDil', u'AgrupaDilEtapa', u'Pendiente_Puente', u'PRODUCTO', u'CTL', u'EMPRESA*', u'FECHA ASIGNADA', u'DIL2', u'ESTADO', u'SITIO', u'ETIQUETA2', u'RANGO', u'PRIORIDAD2', u'ATIENDE', u'FACTIBILIDAD', u'COLONIA2']
#get_pos_field_id_dict(header, 6015)

def addMultipleChoice(answer, element):
    return True


def set_custom_values(pos_field_id, record):
    custom_answer = {}
    #set status de la orden
    #custom_answer['58464e3cb43fdd7d44ae63f1'] = 'abierta'
    return custom_answer


def create_record(pos_field_id, records):
    answer = {}
    metadata = lkf_api.get_metadata()
    for record in records:
        count = 0
        for pos, element in pos_field_id.iteritems():
            count +=1
            if element['field_type'] == 'folio':
                metadata['folio'] = str(record[pos])
                continue
            answer.update(set_custom_values(pos_field_id, record ))
            answer.update(lkf_api.make_infosync_json(record[pos], element))
    metadata["answers"] = answer
    print 'metadata3', metadata
    #print stop
    network.post_forms_answers([metadata,])
    return True

# def upload_bolsa():
#     files = get_files2upload()
#     #files = [{u'_id': ('58575ff4b43fdd35e3169665'), u'answers': {u'f1074100a010000000000001': {u'file_name': u'BASE 16-DICIEMBRES10.xls', u'file_url': u'uploads/1259_jgemayel@pcindustrial.com.mx/e201093c634a2a2ff2068b4df622401a2ac90c83.xls'}}}]
#     if files:
#         for file_url in files:
#             if file_url.has_key('answers') and file_url['answers'].has_key('f1074100a010000000000001'):
#                 if file_url['answers']['f1074100a010000000000001'].has_key('file_url'):
#                     url = file_url['answers']['f1074100a010000000000001']['file_url']
#                     #print 'URL', url
#                     if url.find('https') == -1:
#                         url = 'https://app.linkaform.com/media/' + url
#                     header, records = read_file(url)
#                     #records = get_rr()
#                     pos_field_id = get_pos_field_id_dict(header)
#                     create_record(pos_field_id, records)
#                 else:
#                     print 'no file found'
#             else:
#                 print 'no recored found'
#     return True


def create_paco():
    orders = get_orders_ready4paco()


def get_rr():
    return [[41006162, u'A0', 5552940494, u'CUMAFAR SA DE CV', u'PS', datetime.date(2016, 12, 14), 2, 1, u'NA_', u'NA_0011', '', u'ACR', u'SOTELO', u'SO', u'NA', u'NAL', datetime.date(2016, 12, 15), u'20', u'CP', u'SOTELO', u'CM', u'D+', 0, 0, 1, 0, u'ALCE BLANCO', u'METRO', u'METRO SUR', u'SOT', 56447516, u'A020PBDPE', 3, u'PC CASOS ESPECIALES, NAUCALPAN', 2220240, u'NA_19 INST', 56447516, u'NA_INST', u'NA_0125-20', u'NA_0011B4-7', u'31000037064  /  03C072', u'PCI', u'CONCENTRADOR', u'NAUCALPAN', '', u'NO RESIDENCIAL', u'COMERCIAL', 0, u'TELMEX           ', 1, u'Portabilidad', 1, u'0 a 7 d\\xedas', u'1', u'NO', u'ALTAS VOZ', u'NA_', u'PCI', 20161216, u'A 0-7', u'EN PROCESO', u'CONCENTRADOR', u'PORTABILIDAD', u'0-3', 1, u'PLEX', u'FACTIBLE', 42], [41006667, u'A0', 5552940536, u'CUMAFAR SA DE CV', u'PS', datetime.date(2016, 12, 14), 2, 1, u'NA_', u'NA_0011', '', u'ACR', u'SOTELO', u'SO', u'NA', u'NAL', datetime.date(2016, 12, 15), u'20', u'CP', u'SOTELO', u'CM', u'D+', 0, 0, 1, 0, u'ALCE BLANCO', u'METRO', u'METRO SUR', u'SOT', 56447517, u'A020PBDPE', 3, u'PC CASOS ESPECIALES, NAUCALPAN', 2220240, u'NA_19 INST', 56447517, u'NA_INST', u'NA_0125-26', u'NA_0011B4-8', u'31000038379  /  04E107', u'PCI', u'CONCENTRADOR', u'NAUCALPAN', '', u'NO RESIDENCIAL', u'COMERCIAL', 0, u'TELMEX           ', 1, u'Portabilidad', 1, u'0 a 7 d\\xedas', u'1', u'NO', u'ALTAS VOZ', u'NA_', u'PCI', 20161216, u'A 0-7', u'EN PROCESO', u'CONCENTRADOR', u'PORTABILIDAD', u'0-3', 1, u'PLEX', u'FACTIBLE', 42], [41007103, u'A0', 5552940537, u'CUMAFAR SA DE CV', u'PS', datetime.date(2016, 12, 14), 2, 1, u'NA_', u'NA_0011', '', u'ACR', u'SOTELO', u'SO', u'NA', u'NAL', datetime.date(2016, 12, 15), u'20', u'CP', u'SOTELO', u'CM', u'D+', 0, 0, 1, 0, u'ALCE BLANCO', u'METRO', u'METRO SUR', u'SOT', 56447653, u'A020PBDPE', 3, u'PC CASOS ESPECIALES, NAUCALPAN', 2220240, u'NA_19 INST', 56447653, u'NA_INST', u'NA_0177-18', u'NA_0011B4-9', u'31000038506  /  04F106', u'PCI', u'CONCENTRADOR', u'NAUCALPAN', '', u'NO RESIDENCIAL', u'COMERCIAL', 0, u'TELMEX           ', 1, u'Portabilidad', 1, u'0 a 7 d\\xedas', u'1', u'NO', u'ALTAS VOZ', u'NA_', u'PCI', 20161216, u'A 0-7', u'EN PROCESO', u'CONCENTRADOR', u'PORTABILIDAD', u'0-3', 1, u'PLEX', u'FACTIBLE', 42], [41007692, u'A0', 5552940538, u'CUMAFAR SA DE CV', u'PS', datetime.date(2016, 12, 14), 2, 1, u'NA_', u'NA_0011', '', u'ACR', u'SOTELO', u'SO', u'NA', u'NAL', datetime.date(2016, 12, 15), u'20', u'CP', u'SOTELO', u'CM', u'D+', 0, 0, 1, 0, u'ALCE BLANCO', u'METRO', u'METRO SUR', u'SOT', 56447654, u'A020PBDPE', 3, u'PC CASOS ESPECIALES, NAUCALPAN', 2220240, u'NA_19 INST', 56447654, u'NA_INST', u'NA_0177-21', u'NA_0011A4-4', u'31000038910  /  04J126', u'PCI', u'CONCENTRADOR', u'NAUCALPAN', '', u'NO RESIDENCIAL', u'COMERCIAL', 0, u'TELMEX           ', 1, u'Portabilidad', 1, u'0 a 7 d\\xedas', u'1', u'NO', u'ALTAS VOZ', u'NA_', u'PCI', 20161216, u'A 0-7', u'EN PROCESO', u'CONCENTRADOR', u'PORTABILIDAD', u'0-3', 1, u'PLEX', u'FACTIBLE', 42], [41008411, u'A0', 5552943201, u'CUMAFAR SA DE CV', u'PS', datetime.date(2016, 12, 14), 2, 1, u'NA_', u'NA_0011', '', u'ACR', u'SOTELO', u'SO', u'NA', u'NAL', datetime.date(2016, 12, 15), u'20', u'CP', u'SOTELO', u'CM', u'D+', 0, 0, 1, 0, u'ALCE BLANCO', u'METRO', u'METRO SUR', u'SOT', 56447649, u'A020PBDPE', 3, u'PC CASOS ESPECIALES, NAUCALPAN', 2220240, u'NA_19 INST', 56447649, u'NA_INST', u'NA_0177-25', u'NA_0011A4-5', u'31000039080  /  05C040', u'PCI', u'CONCENTRADOR', u'NAUCALPAN', '', u'NO RESIDENCIAL', u'COMERCIAL', 0, u'TELMEX           ', 1, u'Portabilidad', 1, u'0 a 7 d\\xedas', u'1', u'NO', u'ALTAS VOZ', u'NA_', u'PCI', 20161216, u'A 0-7', u'EN PROCESO', u'CONCENTRADOR', u'PORTABILIDAD', u'0-3', 1, u'PLEX', u'FACTIBLE', 42], [41001517, u'A0', 5570213740, u'FLORES JIMENEZJOSE RODOLFO', u'PS', datetime.date(2016, 12, 14), 2, 1, u'LM_', u'LM_0018', '', u'WFC', u'SOTELO', u'SO', u'NA', u'NAL', datetime.date(2016, 12, 15), u'1L', '', u'SOTELO', u'C-', u'D+', 0, 0, 0, 0, u'LA MANCHA 2A SECCION', u'METRO', u'METRO SUR', u'SOT', 56445539, u'A01LP4DPE', 0, u'PC CASOS ESPECIALES, NAUCALPAN', 2220240, u'NA_43 INST', 56445539, u'NA_INST', u'LM_0017-36', u'LM_0018C1-3', u'31000030117  /  04E037', u'PCI', u'CONCENTRADOR', u'NAUCALPAN', '', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'BESTPHONE        ', 1, u'Portabilidad', 1, u'0 a 7 d\\xedas', u'1', u'NO', u'ALTAS INF', u'LM_', u'PCI', 20161216, u'A 0-7', u'EN PROCESO', u'CONCENTRADOR', u'PORTABILIDAD', u'0-3', 1, u'PLEX', u'NO FACTIBLE', 42], [41002088, u'A0', 5570956460, u'LUIS RAMIREZ SEVERO', u'PS', datetime.date(2016, 12, 14), 2, 2, u'HC_', u'HC_0003', '', u'WFC', u'SOTELO', u'SO', u'NA', u'NAL', datetime.date(2016, 12, 14), u'2L', '', u'SOTELO', u'C-', u'D+', 0, 0, 0, 0, u'LOS CUARTOS', u'METRO', u'METRO SUR', u'SOT', 56439538, u'A02LP4DPE', 3, u'PC CASOS ESPECIALES, NAUCALPAN', 2220240, u'NA_33 INST', 56439538, u'NA_INST', u'HC_0084-18', u'HC_0003F5-10', u'22001030180  /  01E179', u'PCI', u'EDIFICIO', u'MOLINITO', u'MOLINITO', u'NO RESIDENCIAL', u'INFINITUM COMERCIAL', 0, u'BESTPHONE        ', 1, u'Portabilidad', 1, u'0 a 7 d\\xedas', u'2', u'NO', u'ALTAS INF', u'HC_', u'PCI', 20161215, u'A 0-7', u'EN PROCESO', u'EDIFICIO', u'PORTABILIDAD', u'0-3', 1, u'CENTRALES', u'FACTIBLE', u'MOLINITO'], [41003389, u'A0', 5553024417, u'CAMACHO ROBLES CAROLINA', u'PS', datetime.date(2016, 12, 14), 2, 2, u'HC_', u'HC_0069', '', u'WFC', u'SOTELO', u'SO', u'NA', u'NAL', datetime.date(2016, 12, 14), u'1L', u'R5', u'SOTELO', u'C-', u'D+', 0, 0, 0, 0, u'LA OLIMPICA', u'METRO', u'METRO SUR', u'SOT', 56439333, u'A01LP4DPE', 0, u'PC CASOS ESPECIALES, NAUCALPAN', 2220240, u'NA_34 INST', 56439333, u'NA_INST', u'HC_0108-44', u'HC_0069D2-3', u'22001030197  /  01E196', u'PCI', u'EDIFICIO', u'MOLINITO', u'MOLINITO', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'TELMEX           ', 1, u'Portabilidad', 1, u'0 a 7 d\\xedas', u'2', u'NO', u'ALTAS INF', u'HC_', u'PCI', 20161215, u'A 0-7', u'EN PROCESO', u'EDIFICIO', u'PORTABILIDAD', u'0-3', 1, u'CENTRALES', u'FACTIBLE', u'MOLINITO'], [40993482, u'A0', 5557756050, u'CARBALLIDO BUENABAD ASIEL GERM', u'PS', datetime.date(2016, 12, 14), 2, 2, u'AE_', u'AE_0144', '', u'EA', u'CUAUTITLAN', u'EAT', u'MRE', u'MRE', datetime.date(2016, 12, 14), u'1L', u'R5', u'CUAUTITLAN', u'C-', u'C', 0, 0, 0, 0, u'CIUDAD AZTECA', u'METRO', u'METRO NORTE', u'CUA', 56431380, u'A01LPBGPE', 0, u'PC_VARELA, TANIA ME_', 2220943, u'ME_10 INST', 56431380, u'ME_ INST', u'AE_0018FO-33', u'AE_0144FOB5-1', u'  /  ', u'PCI', u'EDIFICIO', u'ECATEPEC', '', u'RESIDENCIAL', u'INFINITUM RESIDENCIAL', 0, u'TELMEX           ', 1, u'Portabilidad', 1, u'0 a 7 d\\xedas', u'2', u'NO', u'ALTAS INF', u'AE_', u'PCI', 20161215, u'A 0-7', u'EN PROCESO', u'EDIFICIO', u'PORTABILIDAD', u'0-3', 1, u'CENTRALES', u'FACTIBLE', 42]]


#upload_bolsa()
