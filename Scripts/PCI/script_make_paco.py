#####
# Made by Jose Patricio VM
#####
# Script para generar pacos a partir de ordenes de Servicio de PCI Industrial
#
#
#####

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


config = {
    #'USERNAME' : 'atencionalcliente@iesa.cc',
    #'PASS' : 'iesa2014',
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



def get_orders_liquidadas():
    return [{'folio':'390569-1259', 'answers':{'f1054000a030000000000002':'liquidada'}},
            {'folio':'41007103','answers':{'f1054000a030000000000002':'liquidada'}}]
    query = query_order4paco()
    query = {'form_id': {'$in': [10540]}, 'deleted_at' : {'$exists':False}, 'answers.f1054000a030000000000002': 'liquidada'}
    select_columns = {'folio':1, 'answers.f1054000a030000000000002':1}
    #orders_records = cr.aggregate(query)
    orders_records = cr.find(query, select_columns)
    print 'query', query
    print 'order find', orders_records.count()
    return orders_records

def make_array(orders):
    res = [['Folio', 'Estatus']]
    print 'orders', orders
    for order in orders:
        row = [order['folio'], order['answers']['f1054000a030000000000002']]
        res.append(row)
    return res


def make_excel_file(orders):
    rows = make_array(orders)
    file_name = "/tmp/output.csv"
    pyexcel.save_as(array=rows,
        dest_file_name=file_name)
    return file_name

def upload_orders_liquidadas():
    orders = get_orders_liquidadas()
    get_file = make_excel_file(orders)
    csv_file = open(get_file,'rb')
    # Mientras no usemos B2 no es necesario el id del campo
    upload_data ={'form_id': 10798}#, 'field_id':'586080c1b43fdd552a98e6c6'}
    csv_file = {'File': csv_file} # El back lo espera como File no como file
    # Back retorna un diccionario con las llaves: status_code y data.
    # data es un diccionario con la llave file que es la ruta que tiene el archivo
    upload_url = lkf_api.post_upload_file(data=upload_data, up_file=csv_file)
    print 'the url', upload_url
    print stop

upload_orders_liquidadas()
