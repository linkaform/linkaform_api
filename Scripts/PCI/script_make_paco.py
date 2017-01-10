#####
# Made by Jose Patricio VM
#####
# Script para generar pacos a partir de ordenes de Servicio de PCI Industrial
#
#
#####

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
    'AUTHORIZATION_EMAIL_VALUE' : 'jgemayel@pcidustrial.com.mx',
    'AUTHORIZATION_TOKEN_VALUE' : '1a84bab48214997eced5b1baa7b0bb24a4058672',
}

settings.config = config
cr = network.get_collections()
lkf_api = utils.Cache()



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


def query_order_posteadas():
    query = {'form_id': {'$in': [10798]}, 'deleted_at' : {'$exists':False}, 'answers.f1079800a010000000000005': 'generar_archivo_de_carga_masiva'}
    return query


def query_get_folio(folio, form_id):
    query = {'deleted_at' : {'$exists':False}, 'form_id':  form_id,  'folio': {'$in': folio}}
    return query


def get_form_answers_by_folio(folio, form_id):
    query = query_get_folio(folio, form_id)
    select_columns = {'folio':1, 'answers':1 }
    print 'queyr', query
    orders_records = cr.find(query, select_columns)
    return orders_records


def get_orders_liquidadas(date_to):
    #return [{'folio':'390569-1259', 'answers':{'f1054000a030000000000002':'liquidada'}},
    #        {'folio':'41007103','answers':{'f1054000a030000000000002':'liquidada'}}]
    query = query_order4paco()
    print 'date_to', date_to
    query = {'form_id': {'$in': [10540]}, 'deleted_at' : {'$exists':False},
            'answers.f1054000a030000000000002': 'liquidada',
            'created_at':{'$lte':date_to}}
    select_columns = {'folio':1, 'answers.f1054000a030000000000002':1, }
    #orders_records = cr.aggregate(query)
    orders_records = cr.find(query, select_columns)
    print 'query', query
    print 'order find', orders_records.count()
    return orders_records


def get_orders_posteadas():
    query = query_order_posteadas()
    select_columns = {'folio':1, 'answers':1, 'form_id':1 }
    orders_records = cr.find(query, select_columns)
    return orders_records


def make_array(orders):
    res = [['Folio', 'Estatus']]
    print 'orders', orders
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


def make_answer(form_id, file_url, date_to, order_count):
    metadata = lkf_api.get_metadata(form_id = 10798, user_id = settings.config['USER_ID'])
    answers = {}
    date = lkf_api.make_infosync_json(date_to, {'field_type':'date','field_id':'f1079800a010000000000001'})
    if file_url:
        status = {'f1079800a010000000000005':'subir_ordenes_posteadas'}
        comments = {'f1079800a010000000000006':'%s Ordens encontradas como liquidadas'%order_count}
        file_date = time.strftime("%Y_%m_%d")
        date = lkf_api.make_infosync_json(date_to, {'field_type':'date','field_id':'f1079800a010000000000001'})
        file_json = {'f1079800a010000000000002':{'file_name':'Ordenes Liquidadas %s.csv'%file_date,
                                    'file_url':file_url}}
        answers.update(file_json)
    else:
        comments = {'f1079800a010000000000006':'Ninguna orden liquidada encontrada'}
        status = {'f1079800a010000000000005':'subir_ordenes_posteadas'}
    answers.update(date)
    answers.update(comments)
    answers.update(status)
    metadata['answers'] = answers
    print 'metadata',metadata
    return metadata


def upload_orders_liquidadas(date_to=time.strftime("%Y-%m-%d")):
    file_url = False
    print '1date to', date_to
    orders = get_orders_liquidadas(date_to)
    order_count = orders.count()
    if order_count > 0:
        get_file = make_excel_file(make_array(orders))
        print 'csv_file'
        csv_file = open(get_file,'rb')
        print 'uploading'
        # Mientras no usemos B2 no es necesario el id del campo
        upload_data ={'form_id': 10798, 'field_id':'586080c1b43fdd552a98e6c6'}
        csv_file = {'File': csv_file} # El back lo espera como File no como file
        # Back retorna un diccionario con las llaves: status_code y data.
        # data es un diccionario con la llave file que es la ruta que tiene el archivo
        upload_url = lkf_api.post_upload_file(data=upload_data, up_file=csv_file)
        #upload_url = {'status_code': 200, 'data': {'file': 'uploads/1259_jgemayel@pcindustrial.com.mx/b04f64aa25291ed7055dbcd4c49a90c51c59427d.csv'}}
        print 'the url', upload_url
        try:
            file_url = upload_url['data']['file']
        except KeyError:
            #make a post of the error is there was an error
            return upload_url['data']
        metadata = make_answer(10798, file_url, date_to, order_count)
    else:
        metadata = make_answer(10798, file_url, date_to, order_count)
    network.post_forms_answers(metadata)
    return True


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
    return []


def process_other_status(folio):
    ##TODO Ver que se necestia hace en estos casos
    return []


def process_posteada(folio):
    folio = ["40993482",]
    #Orde de servicio form_id
    form_id = 10540
    #params = {'folio__contains': "40993482"}
    #record = lkf_api.get_record_answer(params=params)
    records = get_form_answers_by_folio(folio, form_id)
    archivo = []
    header = ['06','CT CHAIREL','PC','2294896','1021','ptorres@pcindustrial.com.mx']
    archivo.append(header)
    for record in records:
        print 'r=',record
        folio_row = []
        folio_row.append(record['folio'])
        answers = record['answers']
        print 'answers', answers
        folio_row += set_construccion(answers)
        folio_row += set_plusvalia(answers)
        folio_row += set_recontratacion(answers)
        folio_row += set_instalacion_poste(answers)
        folio_row += set_bonificaion(answers)
        folio_row += set_montaje_puente(answers)
        folio_row += set_insalacion_cadena(answers)
        folio_row += set_prueba_transmicion(answers)
        folio_row += set_cableado_interior(answers)
        folio_row += set_prueba_transmicion_datos(answers)
        folio_row += set_ubicacion_cliente(answers)
        folio_row += set_prueba_transmicion_vsdl(answers)
        folio_row += set_libreria(answers)
        archivo.append(folio_row)
    print 'archivo=', archivo
    return archivo


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
            csv_file = {'File': csv_file}
            upload_data ={'form_id': 10798, 'field_id':'f1079800a010000000000004'}
            upload_url = lkf_api.post_upload_file(data=upload_data, up_file=csv_file)
            try:
                file_url = upload_url['data']['file']
            except KeyError:
                #make a post of the error is there was an error
                return upload_url['data']
            record['answers']['f1079800a010000000000004'] = file_url
            record_id = record.pop('_id')
            record.pop('folio')
            #record['answers']['f1079800a010000000000005'] = 'subir_resultado_paco'
            file_date = time.strftime("%Y_%m_%d")
            record['answers']['f1079800a010000000000004'] ={
                    'file_name':'Archivo de Carga Masiva %s.xlsx'%file_date,
                    'file_url':file_url}
            record.update(lkf_api.get_metadata(0, user_id = settings.config['USER_ID']))
            print 'record', record
            lkf_api.patch_record(record, record_id)
            print 'csv_file'
            print 'uploading'
        # Mientras no usemos B2 no es necesario el id del campo
    return True


def isItADate(arg):
    try:
        valid_date = datetime.datetime.strptime(arg, '%Y-%m-%d')#time.strptime(arg, '%Y-%m-%d')
        print 'valid_date', valid_date
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
        upload_orders_liquidadas(valid_date)
    else:
        #upload_orders_liquidadas()
        get_orders_for_paco()
