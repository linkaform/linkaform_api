#####
# Made by Jose Patricio VM
#####
# Script para generar pacos a partir de ordenes de Servicio de PCI Industrial
#
#
#####

#import os, sys
#sys.path.insert(0, os.path.abspath("../.."))
import pyexcel, time, datetime
from sys import argv

from linkaform_api import settings
from linkaform_api import network, utils

from rules_archivo_carga import *


mongo_hosts = 'db2.linkaform.com:27017,db3.linkaform.com:27017,db4.linkaform.com:27017'
#mongo_hosts = "127.0.0.1"
mongo_replicaSet = 'linkaform_replica'
MONGO_READPREFERENCE='primary'

MAX_POOL_SIZE = 50
WAIT_QUEUE_TIMEOUT = 1000
MONGODB_URI = 'mongodb://%s/?replicaSet=%s&readPreference=%s'%(mongo_hosts, mongo_replicaSet, MONGO_READPREFERENCE)


config = {
    'USERNAME' : 'linkaform@pcindustrial.com.mx',
    #'USERNAME' : 'josepato@infosync.mx',
    'PASS' : '654321',
    'COLLECTION' : 'form_answer',
    #'HOST' : 'db3.linkaform.com',
    'MONGODB_URI':MONGODB_URI,
    #'MONGODB_PASSWORD': mongodb_password_here
    'PORT' : 27017,
    'USER_ID' : 1259,
    'KEYS_POSITION' : {},
    'IS_USING_APIKEY' : True,
    'AUTHORIZATION_EMAIL_VALUE' : 'linkaform@pcindustrial.com.mx',
    'AUTHORIZATION_TOKEN_VALUE' : '32e3414e60a19c261f42ab83a68897cbc78728e6',
}


settings.config = config
cr = network.get_collections()
lkf_api = utils.Cache()


GLOBAL_VARS = {}

def query_order4paco():
    query = [{'form_id': {'$in': [10540]}, 'deleted_at' : {'$exists':False}, 'answers.f1054000a030000000000002': 'liquidada'},
            {"$group": {
            "_id": {
                     'cope': "$answers.f1054000a010000000000002",
                     },
            "folioPisa": "$answers.f1054000a010000000000001",
            "folioPisaPlex": "$answers.f1054000a010000000000006",
            "telefono": "$answers.f1054000a010000000000005",
            "materiales": "$answers.f1054000a020000100000005",
            "folio": "folio"
            }}
            ]
    return query


#Get errors
def query_orders_with_errors():
    query = {'form_id': {'$in': [10798]}, 'deleted_at' : {'$exists':False},
    'answers.f1079800a010000000000005': 'subir_resultado_paco',
    'answers.f1079800a010000000000002':{'$exists':True}, #Folios Liquidados
    'answers.f1079800a010000000000003':{'$exists':True}, #Folios Posteados
    'answers.f1079800a010000000000004':{'$exists':True}, #Archivo de Carga Masiva
    'answers.f1079800a010000000000012':{'$exists':True}, #Errores PACO
    }
    return query


def get_orders_with_errors():
    query = query_orders_with_errors()
    select_columns = {'folio':1, 'answers':1, 'form_id':1 }
    orders_records = cr.find(query, select_columns)
    return orders_records


def get_errores_paco():
    file_url = False
    orders = get_orders_with_errors()
    order_count = orders.count()
    if order_count > 0:
        for record in orders:
            try:
                get_file_url = record['answers']['f1079800a010000000000012']['file_url']
                get_archivo_file = record['answers']['f1079800a010000000000004']['file_url']
            except KeyError:
                raise KeyError('No se encontro archvio con folios posteadas')
            error_rows = read_errors_file(get_file_url)
            archivo_rows = read_archivo_file(get_archivo_file)
            #print 'file_rows=', error_rows
            for error in error_rows:
                error_index = -1
                try:
                    error_index = archivo_rows.index(str(error[0]))
                except ValueError:
                    pass
                if error_index >= 0:
                    print 'ppoooopppooo'
                    archivo_rows.pop(error_index)
            metadata = lkf_api.get_metadata(form_id = 10798, user_id = settings.config['USER_ID'])
            answers = record['answers']
            answers.update({'f1079800a010000000000009':len(error_rows)})
            answers.update({'f1079800a010000000000005':'realizado'})
            metadata['answers'] = answers
            network.patch_forms_answers(metadata, record['_id'])
            make_paco_record(record, archivo_rows)
    return True


def make_paco_record(record, archivo_rows):
    #record es el archivo para generar el paco
    #archivo_rows son los folios autorizados
    metadata = lkf_api.get_metadata(form_id = 10570, user_id = settings.config['USER_ID'])
    answers = {}
    answers['f1057000a0100000000000f1'] = []
    for folio in archivo_rows:
        print 'solio===', folio
        answers['f1057000a0100000000000f1'].append({'f1057000a010b100000000f1':folio})
    answers['f1074100a0100000000000c1'] =record['answers']['f1074100a0100000000000c1']
    answers['f1057000a010000000000005'] = 'autorizado'
    metadata['answers'] = answers
    network.post_forms_answers(metadata)
    return True


def read_errors_file(file_url):
    if file_url.find('http') == -1:
        file_url = 'https://api.linkaform.com/media/' + file_url
    sheet = pyexcel.get_sheet(url=file_url)
    col = 0
    folio_col = error_col = False
    for row in sheet.row[0]:
        if row.lower() == 'folio':
            folio_col = col
        if row.lower() in ['error']:
            error_col = col
        col += 1
    if not error_col or not folio_col:
        raise Exception("No folio or errors found")
    folios = sheet.column[folio_col][1:]
    errores = sheet.column[error_col][1:]
    res = [ (folios[n],errores[n]) for n in range(len(folios))]
    return res


def read_archivo_file(file_url):
    if file_url.find('http') == -1:
        file_url = 'https://api.linkaform.com/media/' + file_url
    sheet = pyexcel.get_sheet(url=file_url)
    col = 0
    folio_col = 0
    folios = sheet.column[folio_col][1:]
    res = [ str(folios[n]) for n in range(len(folios))]
    return res

##### End errors


def query_get_folio(folio, form_id):
    query = {'deleted_at' : {'$exists':False}, 'form_id':  form_id,  'folio': {'$in': folio}}
    return query


def get_form_answers_by_folio(folio, form_id):
    query = query_get_folio(folio, form_id)
    select_columns = {'folio':1, 'answers':1 }
    orders_records = cr.find(query, select_columns)
    return orders_records


def get_orders_liquidadas(cope, date_to):
    #return [{'folio':'390569-1259', 'answers':{'f1054000a030000000000002':'liquidada'}},
    #        {'folio':'41007103','answers':{'f1054000a030000000000002':'liquidada'}}]
    query = query_order4paco()
    query = {'form_id': {'$in': [10540]}, 'deleted_at' : {'$exists':False},
            'answers.f1054000a030000000000002': 'liquidada',
            'answers.f1054000a010000000000002': cope,
            'created_at':{'$lte':date_to}}
    select_columns = {'folio':1, 'answers.f1054000a030000000000002':1, }
    #orders_records = cr.aggregate(query)
    print 'query2=', query
    orders_records = cr.find(query, select_columns)
    return orders_records


def make_array(orders):
    res = [['Folio', 'Estatus']]
    for order in orders:
        row = [order['folio'], order['answers']['f1054000a030000000000002']]
        res.append(row)
    return res


def make_excel_file(rows):
    #rows = make_array(orders)
    date = time.strftime("%Y_%m_%d")
    file_name = "/tmp/output_%s.xlsx"%(date)
    pyexcel.save_as(array=rows,
        dest_file_name=file_name)
    return file_name


def make_answer(form_id, file_url, date_to, order_count, cope):
    metadata = lkf_api.get_metadata(form_id = 10798, user_id = settings.config['USER_ID'])
    answers = {}
    date = lkf_api.make_infosync_json(date_to, {'field_type':'date','field_id':'f1079800a010000000000001'})
    if file_url:
        status = {'f1079800a010000000000005':'subir_ordenes_posteadas'}
        #comments = {'f1079800a010000000000006':'%s Ordens encontradas como liquidadas'%order_count}
        GLOBAL_VARS['comments'] = '%s Ordens encontradas como liquidadas'%order_count
        GLOBAL_VARS['folios_liquidados'] = order_count
        file_date = time.strftime("%Y_%m_%d")

        #date = lkf_api.make_infosync_json(date_to, {'field_type':'date','field_id':'f1079800a010000000000001'})
        file_json = {'f1079800a010000000000002':{'file_name':'Ordenes Liquidadas %s.xlsx'%file_date,
                                    'file_url':file_url}}
        answers.update(file_json)
    else:
        #comments = {'f1079800a010000000000006':'Ninguna orden liquidada encontrada'}
        GLOBAL_VARS['comments'] = 'Ninguna orden liquidada encontrada'
        status = {'f1079800a010000000000005':'subir_ordenes_posteadas'}
        GLOBAL_VARS['folios_liquidados'] = 0
    answers.update(date)
    #answers.update(comments)
    answers.update(get_update_answer_comments(answers))
    answers.update(status)
    answers.update({'f1074100a0100000000000c1':cope})
    metadata['answers'] = answers
    return metadata

## Ordenes Liquidadas
def query_get_files():
    #This should lookup by ID
    query = {'form_id': {'$in': [10798]}, 'deleted_at' : {'$exists':False},
    'answers.f1079800a010000000000005': 'obtener_folios_liquidados',
    'answers.f1079800a010000000000002':{'$exists':False}, #Folios Liquidados
    'answers.f1079800a010000000000003':{'$exists':False}, #Folios Posteados
    'answers.f1079800a010000000000004':{'$exists':False}, #Archivo de Carga Masiva
    'answers.f1079800a010000000000012':{'$exists':False}, #Errores PACO
    }
    #select_columns = {'answers.f1074100a010000000000001':1, 'answers.f1074100a0100000000000c1':1}
    select_columns = {'answers':1 }
    return query, select_columns


def get_ordenes_liquidadas():
    query, select_columns = query_get_files()
    orders_records = cr.find_one(query, select_columns)
    return orders_records


def get_cope_orders():
    order = get_ordenes_liquidadas()
    if order:
        date = order['answers']['f1079800a010000000000001']
        cope = order['answers']['f1074100a0100000000000c1']
        order_id = order['_id']
        upload_orders_liquidadas(order_id, cope ,date)
    return True


def upload_orders_liquidadas(order_id, cope, date_to=time.strftime("%Y-%m-%d")):
    file_url = False
    date2 = datetime.datetime.strptime(date_to, '%Y-%m-%d')
    orders = get_orders_liquidadas(cope, date2)
    order_count = orders.count()
    if order_count > 0:
        get_file = make_excel_file(make_array(orders))
        csv_file = open(get_file,'rb')
        # Mientras no usemos B2 no es necesario el id del campo
        upload_data ={ 'form_id': 10798, 'field_id':'586080c1b43fdd552a98e6c6'}
        csv_file_json = {'File': csv_file} # El back lo espera como File no como file
        # Back retorna un diccionario con las llaves: status_code y data.
        # data es un diccionario con la llave file que es la ruta que tiene el archivo
        upload_url = lkf_api.post_upload_file(data=upload_data, up_file=csv_file_json)
        csv_file.close()
        #upload_url = {'status_code': 200, 'data': {'file': 'uploads/1259_jgemayel@pcindustrial.com.mx/b04f64aa25291ed7055dbcd4c49a90c51c59427d.csv'}}
        print 'the url', upload_url
        try:
            file_url = upload_url['data']['file']
        except KeyError:
            #make a post of the error is there was an error
            return upload_url['data']
        metadata = make_answer(10798, file_url, date_to, order_count, cope)
    else:
        metadata = make_answer(10798, file_url, date_to, order_count, cope)
    #network.post_forms_answers(metadata)
    network.patch_forms_answers(metadata, order_id)
    return True

####

def read_file(file_url):
    if file_url.find('http') == -1:
        file_url = 'https://api.linkaform.com/media/' + file_url
    sheet = pyexcel.get_sheet(url=file_url)
    col = 0
    for row in sheet.row[0]:
        if row.lower() == 'folio':
            folio_col = col
        if row.lower() in ['etapa','estatus','estatus_de_orden']:
            etapa_col = col
        col += 1
        print 'row',row
    folios = sheet.column[folio_col][1:]
    etapas = sheet.column[etapa_col][1:]
    res = [ (folios[n],etapas[n]) for n in range(len(folios))]
    return res


def porcess_objetada(folio):
    ##TODO se necesita ir al folio y marcar la orden con estatus de objetada
    form_id = 10540
    records = get_form_answers_by_folio(folio, form_id)
    for record in records:
        record_id = record.pop('_id')
        comments = ''
        if record.has_key('answers') and record['answers'].has_key('f1054000a030000000000005'):
            comments = record['answers']['f1054000a030000000000005']
            comments += '\n'
        comments += 'Orden objetada por Telmex'
        record['answers']['f1054000a030000000000005'] = comments
        record['answers']['f1054000a030000000000002'] = 'objetada'
        record.update(lkf_api.get_metadata(10540, user_id = settings.config['USER_ID']))
        lkf_api.patch_record(record, record_id)
    return []


def process_other_status(folio):
    ##TODO Ver que se necestia hace en estos casos
    return []


def process_posteada(folio):
    #folio = ["40993482",]
    #Orde de servicio form_id
    form_id = 10540
    #params = {'folio__contains': "40993482"}
    #record = lkf_api.get_record_answer(params=params)
    records = get_form_answers_by_folio(folio, form_id)
    archivo = []
    rechazos = []
    folios_update = []
    header = ['06','CT CHAIREL','PC','2294896','1021','ptorres@pcindustrial.com.mx']
    archivo.append(header)
    for record in records:
        folio_row = []
        folio_row.append(record['folio'])
        answers = record['answers']
        folio_row += set_construccion(answers)
        plusvalia = set_plusvalia(answers)
        if not plusvalia:
            rechazos.append(record)
            continue
        folio_row += plusvalia
        folio_row += set_recontratacion(answers)
        folio_row += set_instalacion_poste(answers)
        folio_row += set_bonificaion(answers)
        montaje = set_montaje_puente(answers)
        if type(montaje) == str:
            record['comments'] = montaje
            rechazos.append(record)
            continue
        folio_row += montaje
        folio_row += set_insalacion_cadena(answers)
        folio_row += set_prueba_transmicion(answers)
        folio_row += set_cableado_interior(answers)
        folio_row += set_prueba_transmicion_datos(answers)
        folio_row += set_ubicacion_cliente(answers)
        folio_row += set_prueba_transmicion_vsdl(answers)
        folio_row += set_libreria(answers)
        archivo.append(folio_row)
        folios_update.append(record['folio'])
    ### TODO actualizar status y rechazos
    update_records_rechazos(rechazos)
    update_records_status(folios_update, 'proceso_de_carga')
    GLOBAL_VARS['comments'] = 'Se cargaron %s folios al archivo de carga.\n '%(len(folios_update))
    GLOBAL_VARS['comments'] += 'Se rechazaron %s folios.'%(len(rechazos))
    GLOBAL_VARS['rechazo_pci'] = len(rechazos)
    GLOBAL_VARS['archivo_carga'] = len(folios_update)
    return archivo


def update_records_rechazos(rechazos):
    for record in rechazos:
        record_id = record.pop('_id')
        comments = ''
        if record.has_key('answers') and record['answers'].has_key('f1054000a030000000000005'):
            comments = record['answers']['f1054000a030000000000005']
            comments += '\n'
        comments += record.pop('comments')
        record['answers']['f1054000a030000000000005'] = comments
        record['answers']['f1054000a030000000000002'] = 'rechazo_pci'
        record.update(lkf_api.get_metadata(10540, user_id = settings.config['USER_ID']))
        lkf_api.patch_record(record, record_id)
    return True


def update_records_status(folios, status):
    #db.form_answer.update({_id:data._id},{$set:{'answers.552fdbf501a4de288f4275ee':parseInt(data.answers['552fdbf501a4de288f4275ee'])}});
    query = {'folio':{'$in':folios}, 'deleted_at':{'$exists':False}}
    cr.find(query)
    update =  {'$set':{'answers.f1054000a030000000000002':status}}
    tt = cr.update(query, update, multi=True)
    return True


def make_archivo_carga(file_rows):
    archivo_rows = []
    folios_posteados = []
    folios_objetaods = []
    folios_otros = []
    for folio in file_rows:
        if folio[1].lower() == 'posteada':
            folios_posteados.append(folio[0])
        elif folio[1].lower() == 'objetada':
            folios_objetaods.append(folio[0])
        else:
            folios_otros.append(folio[0])
    archivo_rows += process_posteada(folios_posteados)
    archivo_rows += porcess_objetada(folios_objetaods)
    archivo_rows += process_other_status(folios_otros)
    file_name = make_excel_file(archivo_rows)
    return file_name


#Ordenes Posteadas
def query_order_posteadas():
    query = {'form_id': {'$in': [10798]}, 'deleted_at' : {'$exists':False},
    #'answers.f1079800a010000000000005': 'generar_archivo_de_carga_masiva',
    'answers.f1079800a010000000000005': 'subir_ordenes_posteadas',
    'answers.f1079800a010000000000002':{'$exists':True}, #Folios Liquidados
    'answers.f1079800a010000000000003':{'$exists':True}, #Folios Posteados
    'answers.f1079800a010000000000004':{'$exists':False}, #Archivo de Carga Masiva
    'answers.f1079800a010000000000012':{'$exists':False}, #Errores PACO
    }
    return query


def get_orders_posteadas():
    query = query_order_posteadas()
    select_columns = {'folio':1, 'answers':1, 'form_id':1 }
    orders_records = cr.find(query, select_columns)
    return orders_records


def get_orders_for_paco():
    file_url = False
    orders = get_orders_posteadas()
    order_count = orders.count()
    if order_count > 0:
        for record in orders:
            try:
                get_file_url = record['answers']['f1079800a010000000000003']['file_url']
            except KeyError:
                raise KeyError('No se encontro archvio con folios posteadas')
            file_rows = read_file(get_file_url)
            archivo_file_name = make_archivo_carga(file_rows)
            csv_file = open(archivo_file_name,'rb')
            csv_file_json = {'File': csv_file}
            upload_data ={'form_id': 10798, 'field_id':'f1079800a010000000000004'}
            upload_url = lkf_api.post_upload_file(data=upload_data, up_file=csv_file_json)
            csv_file.close()
            try:
                file_url = upload_url['data']['file']
            except KeyError:
                #make a post of the error is there was an error
                return upload_url['data']
            record['answers']['f1079800a010000000000004'] = file_url
            record_id = record.pop('_id')
            record.pop('folio')
            record['answers']['f1079800a010000000000005'] = 'subir_resultado_paco'
            file_date = time.strftime("%Y_%m_%d")
            record['answers']['f1079800a010000000000004'] ={
                    'file_name':'Archivo de Carga Masiva %s.xlsx'%file_date,
                    'file_url':file_url}
            #record['answers']['f1079800a010000000000006'] =  get_update_comments(record)
            record['answers'] =  get_update_answer_comments(record)
            record.update(lkf_api.get_metadata(0, user_id = settings.config['USER_ID']))
            lkf_api.patch_record(record, record_id)
            print 'csv_file'
            print 'uploading'
        # Mientras no usemos B2 no es necesario el id del campo
    return True


def get_update_answer_comments(record):
    answers = {}
    if record.has_key('answers'):
        answers = record['answers']
    comments = ''
    if answers.has_key('f1079800a010000000000006'):
        comments = answers['f1079800a010000000000006']
        comments += '\n'
    comments += GLOBAL_VARS['comments']
    answers['f1079800a010000000000006'] = comments
    if GLOBAL_VARS.has_key('folios_liquidados'):
        answers['f1079800a010000000000007'] = GLOBAL_VARS['folios_liquidados']
    if GLOBAL_VARS.has_key('rechazo_pci'):
        answers['f1079800a010000000000008'] = GLOBAL_VARS['rechazo_pci']
    if GLOBAL_VARS.has_key('rechazo_telmex'):
        answers['f1079800a010000000000009'] = GLOBAL_VARS['rechazo_telmex']
    if GLOBAL_VARS.has_key('archivo_carga'):
        answers['f1079800a010000000000010'] = GLOBAL_VARS['archivo_carga']
    return answers


def isItADate(arg):
    try:
        valid_date = datetime.datetime.strptime(arg, '%Y-%m-%d')#time.strptime(arg, '%Y-%m-%d')
    except ValueError:
        error = 'Invalid date or date format, format should look like this Y-M-d.'
        error += ' Insted you send this %s'%arg
        raise ValueError(error)
    return valid_date

if __name__ == "__main__":
    print 'args= ', argv
    if len(argv) > 1:
        valid_date = isItADate(argv[1])
        print 'valid date', valid_date
        #upload_orders_liquidadas(valid_date)
    else:
        #upload_orders_liquidadas()
        get_errores_paco()
        get_orders_for_paco()
        get_cope_orders()
