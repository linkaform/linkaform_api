#coding: utf-8
from pymongo import MongoClient
from pymongo.collection import Collection

from datetime import datetime
from random import randint
from logistorage import *

from sys import stderr

import json, re, locale, requests, simplejson



host = 'localhost'
local_port = 27017
#testing_port = 27019
production_port = 27017

LOGIN_URL = "https://www.info-sync.com/api/infosync/user_admin/login/"
USERNAME = 'logistorage.infosync@gmail.com'
PASS = '654321'
GET_PARENT_ID_FORMS = "https://www.info-sync.com/api/infosync/item/?parent="

MONTH_DIR = {1:'2015/01',2:'2015/02',3:'2015/03',4:'2015/04',5:'2015/05',6:'2015/06',
7:'2015/07',8:'2015/08',9:'2015/09',10:'2015/10',11:'2015/11',12:'2015/12'}

MONTH_DIR_TEXT = {'ENERO':'2015/01','FERERO':'2015/02','MARZO':'2015/03','ABRIL':'2015/04','MAYO':'2015/05','JUNIO':'2015/06',
'JULIO':'2015/07','AGOSTO':'2015/08','SEPTIEMBRE':'2015/09','OCTUBRE':'2015/10','NOVIEMBRE':'2015/11','DICIEMBRE':'2015/12'}


service_names = {'service':'Servicios', 'space_unit':'Unidad de Espacio',
                'fixed_rent':'Renta Fija', 'office_rent':'Renta Oficina'}
#
# price_fields_ids = [
#     #"5591a8b601a4de7bba8529b5",
#     #"558b248901a4de7bb94f7cfc",
#     "558d6a3c01a4de7bba8528a1",
#     "558b01dd01a4de7bba851397",
#     "558b01dd01a4de7bba851398",
#     "558b01dd01a4de7bba851399",
#     "558b01dd01a4de7bba85139c",
#     "558b01dd01a4de7bba85139d",
#     "558b01dd01a4de7bba85139e",
#     "558b01dd01a4de7bba8513af",
#     "558b01dd01a4de7bba85139f",
#     "559168bd01a4de7bba852996",
#     "558b01dd01a4de7bba8513a0",
#     "558b01dd01a4de7bba8513a1",
#     "558b01dd01a4de7bba8513a2",
#     "558b01dd01a4de7bba8513a3",
#     "558b01dd01a4de7bba8513a4",
#     "558b01dd01a4de7bba8513a5",
#     "558b01dd01a4de7bba8513a6",
#     "558b01dd01a4de7bba8513a7",
#     "558b01dd01a4de7bba8513a8",
#     "558b01dd01a4de7bba8513a9",
#     "558b01dd01a4de7bba85139a",
#     "558b01dd01a4de7bba8513aa",
#     "558b01dd01a4de7bba8513ab",
#     "558b01dd01a4de7bba8513ac",
#     "558b01dd01a4de7bba8513ad",
#     "558b01dd01a4de7bba8513ae",
#     "558db23301a4de7bba8528e5",
#     "5594677423d3fd7d311a4580",
#     "5595a5ae23d3fd7d304980c3",
#     "5594688623d3fd7d311a4583",
#     "5594688623d3fd7d311a4584",
#     "55c5392c23d3fd4817ed01d0"]

#This are all the forms related to service,
#every time logistoage creates a new services form
#we have to add it here

mty = [3749]
mex = [3893]
gdl = [3758]
tij = [3918]
vsa = [3935]
juarez = [4192]

service_folders = mty + mex + gdl + tij + vsa + juarez

#service_forms = get_all_forms(service_folders)

#This are all the forms related to space unit,
#every time logistoage creates a new related to space unit form
#we have to add it here
space_unit_folder= [4339]
#space_forms = get_all_forms(space_unit_folder)

#service_id:price_id
#everytime we add a new price
#we have to add it here , with the service id and the price is related to

#558b01dd01a4de7bba8513a1:65

service_price_json = {
        "5591627901a4de7bb8eb1ad9":"558b01dd01a4de7bba851397",
        "559167ed01a4de7bba852991":"558b01dd01a4de7bba851398",
        "5591627901a4de7bb8eb1ada":"558b01dd01a4de7bba851399",
        "559167ed01a4de7bba852992":"558b01dd01a4de7bba85139a",
#Old record testing        "5591627901a4de7bb8eb1adb":"558b01dd01a4de7bba85139b",
        "5591627901a4de7bb8eb1adb":"558b01dd01a4de7bba85139b",
        "5591627901a4de7bb8eb1adc":"558b01dd01a4de7bba85139c",
        "559167ed01a4de7bba852993":"558b01dd01a4de7bba85139d",
        "559167ed01a4de7bba852994":"558b01dd01a4de7bba85139e",
        "5591627901a4de7bb8eb1add":"558b01dd01a4de7bba85139f",
        "5591627901a4de7bb8eb1ade":"559168bd01a4de7bba852996",
        "55916a6f01a4de7bba852997":"558b01dd01a4de7bba8513a0",
        "5591627901a4de7bb8eb1adf":"558b01dd01a4de7bba8513a1",
        "5591627901a4de7bb8eb1ae0":"558b01dd01a4de7bba8513a2",
        "55916a6f01a4de7bba852998":"558b01dd01a4de7bba8513a3",
        "55916a6f01a4de7bba852999":"558b01dd01a4de7bba8513a4",
        "55916a6f01a4de7bba85299a":"558b01dd01a4de7bba8513a5",
        "55916a6f01a4de7bba85299b":"558b01dd01a4de7bba8513a6",
        "55916a6f01a4de7bba85299c":"558b01dd01a4de7bba8513a7",
        "55916a6f01a4de7bba85299d":"558b01dd01a4de7bba8513a8",
        "55916a6f01a4de7bba85299e":"558b01dd01a4de7bba8513a9",
        "55916a6f01a4de7bba85299f":"558b01dd01a4de7bba8513aa",
        "55916a6f01a4de7bba8529a0":"558b01dd01a4de7bba8513ab",
        "5591627901a4de7bb8eb1ae1":"558b01dd01a4de7bba8513ac",
        "5591627901a4de7bb8eb1ae2":"558b01dd01a4de7bba8513ad",
        "55916a6f01a4de7bba8529a1":"558b01dd01a4de7bba8513ae",
        "55916a6f01a4de7bba8529a2":"558b01dd01a4de7bba8513af",
        "55cb692523d3fd4818dd2195":"55cb786023d3fd4818dd21b7",
        "55cb692523d3fd4818dd2196":"55c5389623d3fd4818dd1dad",
        "55cb692523d3fd4818dd2197":"55cb786023d3fd4818dd21b8",
        "55cb692523d3fd4818dd2198":"55cb786023d3fd4818dd21b9",
        "55cb692523d3fd4818dd2199":"55cb786023d3fd4818dd21ba",
        "55cb692523d3fd4818dd219a":"55cb786023d3fd4818dd21bb",
        "55cb692523d3fd4818dd219b":"55cb786023d3fd4818dd21bc",
        "55cb692523d3fd4818dd219c":"55cb786023d3fd4818dd21bd",
        "55cb692523d3fd4818dd219d":"55cb786023d3fd4818dd21be",
        "55cb692523d3fd4818dd219e":"55cb786023d3fd4818dd21bf",
        "55cb692523d3fd4818dd219f":"55cb786023d3fd4818dd21c0",
        "55cb692523d3fd4818dd21a0":"55cb786023d3fd4818dd21c1",
        "55cb692523d3fd4818dd21a1":"55cb786023d3fd4818dd21c2",
        "55cb692523d3fd4818dd21a2":"55cb786023d3fd4818dd21c3",
        "55cb7f0923d3fd0328736629":"55cb7f5323d3fd032873662a",
        "558d685701a4de7bba85289f":"558db23301a4de7bba8528e5",
        "55a010c323d3fd2994ab74e8":"558db23301a4de7bba8528e5",
        "55a010c323d3fd2994ab74e9":"558db23301a4de7bba8528e5",
        "5595a5ae23d3fd7d304980c3":"5595a5ae23d3fd7d304980c3",
        "5594688623d3fd7d311a4583":"5594688623d3fd7d311a4583",
        "558d6a3c01a4de7bba8528a1":"558d6a3c01a4de7bba8528a1",
        "5594677423d3fd7d311a4580":"5594677423d3fd7d311a4580"
}

#service_id:price_id
#just for extra space
extra_price_json = {
        "558d685701a4de7bba85289f":"55c5392c23d3fd4817ed01d0",
        "55a010c323d3fd2994ab74e8":"55c5392c23d3fd4817ed01d0",
        "55a010c323d3fd2994ab74e9":"55c5392c23d3fd4817ed01d0",
}

#price_id:condition_id <the condition_id in on the list price
extra_price_condition_json = {
        "55c5392c23d3fd4817ed01d0":"5594688623d3fd7d311a4584",
}

#new price_fields_ids ids,
price_fields_ids = service_price_json.values() + extra_price_json.values() + extra_price_condition_json.values()

meta = ["_id", "version","folio", "created_at", "updated_at", "end_date", "start_date"]

other_field = {
    'Cliente':{'id':'5591627901a4de7bb8eb1ad5','required':True},
    'Almacen': {'id':'5591627901a4de7bb8eb1ad4','required':True},
    'Documento':{'id':'55917c1701a4de7bb94f87ef','required':False},
    'Fecha_de_Captura':{'id':'55b7f41623d3fd41daa1c414','old_id':'55b7f3e023d3fd41dbccb376', 'required':False},
    'Mes':{'id':'559174f601a4de7bb94f87ed','required':False},
    'Fecha':{'id':'55b7f3e023d3fd41dbccb376','required':False},
    }

other_field_ids = [x['id'] for x in other_field.values()]

filter_ids = service_price_json.keys() + other_field_ids

file_path = '/var/tmp/logistorage/'


def warning(*objs):
    '''
    To print stuff at stderr
    '''
    output = "warning:%s\n" % objs
    stderr.write(output)

def login(session, username, password):
    r = session.post(LOGIN_URL, data = simplejson.dumps({"password": PASS, "username": USERNAME}))
    return r.status_code == 200

def get_all_forms(folders_id):
    forms_ids = []
    session = requests.Session()
    if login(session, USERNAME, PASS):
        for folder_id in folders_id:
            get_forms = GET_PARENT_ID_FORMS + str(folder_id)
            r = session.get(get_forms, headers={'Content-type': 'application/json'}, verify=False)
            if r.status_code == 200:
                response = simplejson.loads(r.content)
                objects = response['objects']
                for obj in objects:
                    if obj['itype'] == 'form':
                        forms_ids.append(obj['id'])
    return forms_ids

def get_price_id_dict():
    select_fields = {}
    #for price_id in price_fields_ids:
    for price_id in price_fields_ids:
        select_fields.update({"answers.%s"%price_id:1})
    for meta_field in meta:
        select_fields.update({meta_field:1})
    return select_fields

def set_dict_service():
    res = {}
    for service_id in service_price_json.keys():
        qty = int(random.random()*10)
        price =  math.floor(random.random()*10)
        res.update({service_id:{'qty':qty,'unit_price':price, 'total':qty*price}})
    return res

def get_user_local_connection(user_id):
    connection = {}
    connection['client'] = MongoClient(host, local_port)
    user_db_name = "infosync_answers_client_{0}".format(user_id)
    if not user_db_name:
        return None
    connection['db'] = connection['client'][user_db_name]
    return connection

def get_user_production_connection(user_id):
    connection = {}
    connection['client'] = MongoClient(host, production_port)
    user_db_name = "infosync_answers_client_{0}".format(user_id)
    if not user_db_name:
        return None
    connection['db'] = connection['client'][user_db_name]
    return connection

def set_price_client(price_line, price_list, client):
    #checks client key or crates it
    if price_list.has_key(client):
        return price_list
    else:
        price_list[client] = {}
        return price_list

def set_price_warehouse(price_line, price_list, client, warehouse):
    #checks client key or crates it
    if price_list[client].has_key(warehouse):
        return price_list
    else:
        price_list[client][warehouse] = set_structure_service()
        return price_list

def set_structure_service():
    services = {}
    for price_id in price_fields_ids:
        services.update({price_id:[]})
    return  services

def set_price_service(price_line, service_list):
    for service_id in service_list.keys():
        price_detail = {
        'from': price_line['answers'].get('55a53ecb23d3fd7c88b11108', ''),
        'to':price_line['answers'].get('55a53ecb23d3fd7c88b11109', ''),
        'price':price_line['answers'].get(service_id, 0),
        'currency' : price_line['answers'].get('5591a8b601a4de7bba8529b5', 'mx_pesos'),
        #'lable': 'Etiqueta %s'%service_id,
        #'operation':"%s*%s"%(service_id,service_id),
        }
        service_list[service_id].append(price_detail)
    return service_list

def get_service_price():
    all_forms = get_all_forms(service_folders) + get_all_forms(space_unit_folder)
    etl_model = FakeETLModel(
    **{
        'name': 'Reporte', 'item_id':  all_forms[0], 'user_id': 516,
        'filters': filter_ids,
        'group_filters': []
        }
    )
    user_conn = get_user_production_connection(etl_model.user_id)
    form_answer = user_conn['db']['form_answer']
    price_list = {}
    for price_line in form_answer.find({"form_id": 3447}):
        #checks that the primary keys exists
        service_list = {}
        try:
            client = price_line['answers']['558d6a3c01a4de7bba8528a1']
            warehouse = price_line['answers']['558b248901a4de7bb94f7cfc']
        except KeyError:
            pass
        price_list = set_price_client(price_line, price_list ,client)
        price_list = set_price_warehouse(price_line, price_list, client, warehouse)
        price_list[client][warehouse] = set_price_service(price_line, price_list[client][warehouse])
    return price_list

class FakeETLModel(object):
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        #rtype = kwarghs["rtype"]
        self.item_id = kwargs["item_id"]
        self.filters = kwargs["filters"]
        self.user_id = kwargs["user_id"]
        self.group_filters = kwargs["group_filters"]
        self.rent = {}
        #created_at = kwargs["created_at"]
        #updated_at = kwargs["updated_at"]
        #expiration = kwargs["expiration"]
        #active = True

def get_price_from_dates(answer, price_list, created_at):
        offset = '05'
        index_price = -1
        index_prices = 0
        last_from_delta = 1000
        last_to_delta = 1000
        for price in price_list:
            if not price['from'] or not price['to']:
                continue
            to_price = datetime.strptime(price['to']+'T%s'%offset, "%Y-%m-%dT%H")
            to_created_at_delta = to_price - created_at
            if to_created_at_delta.days <= 0 or (index_prices == 0 and to_created_at_delta.days >= 0):
                index_price = index_prices
            last_to_delta = to_created_at_delta.days
            index_prices = index_prices + 1
        try:
            current_price = price_list[index_price]
            unit_price = current_price['price']
            qty = float(answer)
            currency = current_price['currency']
        except:
            unit_price = 0.0
            qty = 0
            currency = 'mx_pesos'
        service_json = {
            'qty':qty,
            'unit_price': unit_price,
            'total': unit_price * qty,
            'currency': currency,
        }
        return service_json

def get_service_answer_json(answer, field, meta_answers):
    price_id = service_price_json[field['field_id']['id']]
    client = re.sub(' ', '_', meta_answers['5591627901a4de7bb8eb1ad5']).lower()
    warehouse = re.sub(' ', '_', meta_answers['5591627901a4de7bb8eb1ad4']).lower()
    created_at = meta_answers['created_at']
    price_list =  PRICE_LIST[client][warehouse][price_id]
    service_json = get_price_from_dates(answer, price_list, created_at)
    if field['field_id']['id'] in extra_price_json.keys():
        price_id = extra_price_json[field['field_id']['id']]
        extra_price_list = PRICE_LIST[client][warehouse][price_id]
        extra_unit_price =  get_price_from_dates(answer, extra_price_list, created_at)['unit_price']
        #unit_price = current_price['price']
        condition_id = extra_price_condition_json[price_id]
        condition_price_list = PRICE_LIST[client][warehouse][condition_id]
        condition_qty = get_price_from_dates(answer, condition_price_list, created_at)['unit_price']
        extra_json = {
        'extra_price':extra_unit_price,
        'condition':{'operator':'>','qty':condition_qty}
        }
        service_json.update(extra_json)
    return service_json

def get_answer(answer, field, meta_answers= {}):
        # Formatear respuesta dependiendo del tipo de campo
        field_id = field["field_id"]["id"]
        # if field_id == '5591627901a4de7bb8eb1ad5':
        #     print 'field',field
        #     print 'answer', answer
        # Imagen, Documento, Firma
        if field["field_type"] in ["geolocation", "signature", "image", "document"]:
            return None
        # Opcion multiple
        elif field["field_type"] in ["checkbox"]:
            options = {}
            for option in field["options"]:
                options[option["value"]] = option["label"]
            for value in answer:
                if options.get(value):
                    return options[value]
                else:
                    return value
        # Radio
        elif field["field_type"] in ("radio","select"):
            options = {}
            #print 'answer', len(answer)
            for option in field["options"]:
                options[option["value"]] = option["label"]
            if options.get(answer):
                return options.get(answer)
            else:
                if answer and len(answer) ==0:
                    return None
                else:
                    return answer
        elif field["field_type"] == "date":
            #TODO get time offset
            date = answer + 'T05'
            return datetime.strptime(date,'%Y-%m-%dT%H')
        elif field_id in service_price_json.keys():
            try:
                return get_service_answer_json(answer, field, meta_answers)
            except KeyError:
                return {
                'qty':float(answer),
                'unit_price': 0.0,
                'total': 0.0,
                'currency':'mx_pesos'
                }
        # Demás tipos
        else:
            return answer

def insert_rent_services(meta_answer):
    rent_json = meta_answer.copy()
    rent_json.pop('folio')
    rent_json.pop('end_date')
    rent_json.pop('start_date')
    rent_json.pop('updated_at')
    rent_json.pop('version')
    client = re.sub(' ', '_', rent_json['5591627901a4de7bb8eb1ad5']).lower()
    warehouse = re.sub(' ', '_', rent_json['5591627901a4de7bb8eb1ad4']).lower()
    created_at = rent_json['created_at']
    rent_id = str(created_at.year) + str(created_at.month) + client + warehouse
    #TODO get real price depending on the date
    fixed_rent_uprice = PRICE_LIST[client][warehouse]['5595a5ae23d3fd7d304980c3'][0]['price']
    fixed_rent_currency = PRICE_LIST[client][warehouse]['5595a5ae23d3fd7d304980c3'][0]['currency']
    office_rent_uprice = PRICE_LIST[client][warehouse]['5594688623d3fd7d311a4583'][0]['price']
    office_rent_currency = PRICE_LIST[client][warehouse]['5594688623d3fd7d311a4583'][0]['currency']
    rent_json.update({
    '_id':rent_id,
    'itype':'rent',
    'fixed_rent':{'unit_price':fixed_rent_uprice,'currency':fixed_rent_currency},
    'office_rent':{'unit_price':office_rent_uprice,'currency':office_rent_currency},
    })
    return rent_json

def invoicing_month(one_record_json):
    month = one_record_json.get('559174f601a4de7bb94f87ed',False)
    if not month:
        locale.setlocale(locale.LC_TIME,'es_MX.utf-8')
        date_format = locale.nl_langinfo(locale.D_FMT)
        month = one_record_json['created_at'].strftime('%B').upper()
    return {'559174f601a4de7bb94f87ed':month}

def get_all_months(db_form_answer):
    proyect = [{"$project":
                    {
                    "year":{"$year" : "$created_at"},
                    "month":{"$month" : "$created_at"},
                    }
                },
                {"$group":
                    {"_id":
                        {"year":"$year", "month":"$month"},
                    }
                }]
    year_month = db_form_answer.aggregate(proyect)['result']
    return year_month

def verify_one_record_per_company(report_answer):#, one_record_json):
    all_client = report_answer.distinct('5591627901a4de7bb8eb1ad5')
    all_warehouse = report_answer.distinct('5591627901a4de7bb8eb1ad4')
    all_types = report_answer.distinct('itype')
    for client_upper in all_client:
        client = re.sub(' ', '_', client_upper ).lower()
        for warehouse_upper in all_warehouse:
            warehouse = re.sub(' ', '_', warehouse_upper).lower()
            for year_month in get_all_months(report_answer):
                year = year_month['_id']['year']
                month = year_month['_id']['month']
                offset = '05'
                date = '%s-%s-01T%s:00:00'%(year, month, offset)
                created_at = datetime.strptime(date,'%Y-%m-%dT%H:%M:%S')
                for itype in all_types:
                    one_record_json = {}
                    one_record_id = str(year) + str(month) + client + warehouse + '_' + itype
                    one_record_json.update({
                        '_id':one_record_id,
                        'itype':itype,
                        'created_at': created_at,
                        '55b7f41623d3fd41daa1c414':created_at,
                        '5591627901a4de7bb8eb1ad5':client_upper,
                        '5591627901a4de7bb8eb1ad4':warehouse_upper })
                    one_record_json.update(invoicing_month(one_record_json))
                    report_answer.update({'_id':one_record_id}, one_record_json, upsert=True)
    return True

#TODO AGREGAR LISTA DE PRECIOS EN PESOS Y DLLS
#VALIDAR FECHA DE LISTA DE PRECIOS
#INSERTAR PRECIO ESPECIAL

def get_meta_answer_with_rules(record):
    created_at = record['created_at']
    res = record['answers'].get(other_field['Fecha_de_Captura']['id'], False)
    #TODO Get the real offset from mongodb
    #do in mongo
    #var now = new Date();
    #now.getTimezoneOffset()
    #this will give you the offset in munuts
    offset = '05'
    if not res:
        res = record['answers'].get(other_field['Fecha_de_Captura']['old_id'], False)
    if not res:
        res = str(created_at.year) + '-' + str(created_at.month) + '-' + str(created_at.day)
    date = res + 'T%s'%offset
    res =  datetime.strptime(date,'%Y-%m-%dT%H')
    return {other_field['Fecha_de_Captura']['id']:res}

def get_record_currency(record_answer):
    currency = False
    if record_answer.has_key('currency') and record_answer['currency']:
        print 'ya tenia -------------------------------------------------------------'
        return record_answer['currency']
    for answer in record_answer.values():
        try:
            currency = answer['currency']
        except:
            continue
        if currency:
            return currency
    print '******************************* no pudo ****fuerza a pesos*******************************'
    print 'record_answer='  ,record_answer
    return 'mx_pesos'

def etl():
    service_forms = get_all_forms(service_folders)
    space_forms = get_all_forms(space_unit_folder)
    all_forms = service_forms + space_forms
    items_to_search  = all_forms
    if True:
        etl_model = FakeETLModel(
        **{
            'name': 'Reporte', 'item_id':  items_to_search[0], 'user_id': 516,
            'filters': filter_ids,
            'group_filters': []
            }
        )
        user_production_conn = get_user_production_connection(etl_model.user_id)
        # Form answer collection
        form_answer = user_production_conn['db']['form_answer']
        user_local_conn = get_user_local_connection(etl_model.user_id)
        # Obtener coleccion de reportes si existe, crear si aún no existe
        if 'report_answer' in user_local_conn['db'].collection_names():
            report_answer = user_local_conn['db']['report_answer']
            report_answer.drop()
        report_answer = Collection(user_local_conn['db'], "report_answer", create=True)
        report = { "form_id": etl_model.item_id }
        count = 0
        all_forms_find = {"form_id": {"$in":all_forms}}
        #alter_find = {'answers.5591627901a4de7bb8eb1ad5':'celer','form_id': {"$in":space_forms}}
        #alter_find =  {"answers.55b7f41623d3fd41daa1c414":{"$gte": 'ISODate("2015-05-01T00:00:00Z")', '$lt':'ISODate("2015-08-01T00:00:00Z")'}}
        ###replace alter_find with all_forms_find
        for record in form_answer.find(all_forms_find):
            count +=1
            print 'records ', count
            record_answer = {}
            pass_all = False
            fields = {}
            filter_fields = {}
            all_fields = record['voucher']['fields']
            #fields = update_fields()
            for field in all_fields:
                field_id = field['field_id']['id']
                if field_id in  record["answers"].keys():
                    if field_id in etl_model.filters:
                        fields.update({field_id:field})
            meta_answers = {}
            ## Metadata
            #meta_answers = set_metadata
            for raw_meta in meta:
                meta_answer = record.get(raw_meta, False)
                if meta_answer:
                    meta_answers.update({raw_meta:meta_answer})
                else:
                    print 'NOT FOUND THE the metadata ', raw_meta
                    print 'meta_answer',meta_answer
                    pass_all = True
                    continue
            ### Metadata form fields
            meta_answers.update(get_meta_answer_with_rules(record))
            for meta_field in other_field.values():
                meta_answer = record["answers"].get(meta_field['id'], False)
                if meta_answer:
                    meta_answers.update({meta_field['id']:get_answer(meta_answer,fields[meta_field['id']])})
                    record["answers"].pop(meta_field['id'])
                else:
                    if meta_field['required']:
                        print 'DID NOT FIND THE FOLLOWING FIND AND WILL SKIP THIS RECORD', meta_field
                        pass_all = True
            if pass_all:
                try:
                    print 'SKIPING ...', record['_id']
                except:
                    pass
                continue
            record_answer.update(meta_answers)
            service_answers = {}
            ### Fileds for services
            for answer_field_id in record["answers"].keys():
                if record['form_id'] in space_forms:
                    service_answers.update({'itype':'space_unit'})
                else:
                    service_answers.update({'itype':'service'})
                if answer_field_id in etl_model.filters:
                    service_answers.update({answer_field_id:get_answer(record["answers"][answer_field_id], fields[answer_field_id], meta_answers)})
            #print 'service_answers',service_answers
            record_answer.update(service_answers)
            #report_answer.replace_one(record_answer, upsert=True)
            #print 'record_answer',record_answer
            currency = get_record_currency(record_answer)
            record_answer.update({'currency':currency})
            report_answer.update({'_id':record_answer['_id']}, record_answer, upsert=True)
            try:
                rent_service = insert_rent_services(meta_answers)
            except KeyError:
                print 'COULD NOT INSERT RENT, NO PRICE LIST FOR...',meta_answers
                continue
            report_answer.update({'_id':rent_service['_id']}, rent_service, upsert=True)
        verify_one_record_per_company(report_answer)
        return True

PRICE_LIST = get_service_price()
etl()

def loop_query_update(cr_report_total, query_result, itype, operation_type='update'):
    count = 0
    for record in query_result:
        count += 1
        try:
            insert_res = {'itype':service_names[itype]}
        except KeyError:
            insert_res = {'itype':itype}
        _id = get_insert_id(record['_id'], itype)
        if _id:
            insert_res.update(get_query_service_total(record))
            has_id = cr_report_total.find({'_id':_id})
            print 'count',count
            #if count == 30:
            #    print stop
            if has_id.count() > 0 and operation_type == 'update':
                insert_res.update(has_id.next())
                has_id.close()
                print 'userting record : ', count
                cr_report_total.update({'_id':_id}, insert_res, upsert=True )
            elif has_id.count() == 0:
                insert_res['_id'] = _id
                has_id.close()
                cr_report_total.insert(insert_res)
                ###TODO READFILE THEN UPDATE IT
    return True

#loop_query_update(cr_report_total, space_unit_res['result'], operation_type='insert')
def get_insert_id (rec, itype):
    #rec_id = rec['_id']
    try:
        try:
            currency = rec['currency'].split('_')[0]
        except:
            #TODO CURRENCY
            currency = 'mx'
        months_index_str = [str(i) for i in range(13)]
        #Checks if the month comes on a numeric format even if its consider a str
        #And it converts it to the given format ad MONTH_DIR
        if type(rec['month']) is int or rec['month'] in months_index_str:
            month = MONTH_DIR[int(rec['month'])]
        else:
            month = MONTH_DIR_TEXT[rec['month']]
        month = month.lower()
        client = re.sub(' ', '_', rec['client']).lower()
        #print 'cliente ', client
        if not client:
            print 'aqui truena'
            print truena_get_insert_id
        warehouse = re.sub(' ', '_', rec['warehouse']).lower()
        if not warehouse:
            print 'aqui warehouse'
            print truena_get_insert_id
        if not itype:
            print 'truena type'
            print truena_get_insert_id
        db_id = currency + month + client + warehouse + itype
        return db_id
    except KeyError:
        print 'fail-fail-fail--fail-fail-fail-fail-fail-fail===='
        return False

def get_query_service_total(record):
    res = {}
    for key, value in record.iteritems():
        if key == '_id':
            res.update(get_query_service_total(record[key]))
        else:
            if value:
                res.update({key:value})
            else:
                res.update({key:0})
        if key == 'month' and type(value) == int:
            res.update({key:MONTH_DIR[value]})
        elif key == 'month' and type(value) in (str, unicode):
            res.update({key:MONTH_DIR_TEXT[value]})
    return res


def insert_services(report_answer, cr_report_total):
    service_query = services.get_query()
    service_res = report_answer.aggregate(service_query)
    loop_query_update(cr_report_total, service_res['result'], itype='service', operation_type='insert')
    return True

def upsert_space_unit(report_answer, cr_report_total):
    space_unit_query =space_unit.get_query()
    space_unit_res = report_answer.aggregate(space_unit_query)
    loop_query_update(cr_report_total, space_unit_res['result'], itype='space_unit',operation_type='insert')
    return True

def upsert_rent_service(report_answer, cr_report_total):
    rent_service_query = rent_fixed.get_query()
    rent_service_res = report_answer.aggregate(rent_service_query)
    loop_query_update(cr_report_total, rent_service_res['result'], itype='fixed_rent',operation_type='insert')
    rent_office_query = rent_office.get_query()
    rent_office_res = report_answer.aggregate(rent_office_query)
    loop_query_update(cr_report_total, rent_office_res['result'], itype='office_rent',operation_type='insert')
    return True

def set_services_total():
    user_id = 516
    user_local_conn = get_user_local_connection(user_id)
    # Obtener coleccion de reportes si existe, crear si aún no existe
    if 'report_answer' in user_local_conn['db'].collection_names():
        report_answer = user_local_conn['db']['report_answer']
    else:
        print 'STOP NO COLLECTION'
        print 'driiiioooopstoooooooooooooooooooooooooooop'
    if 'report_total' in user_local_conn['db'].collection_names():
        cr_report_total = user_local_conn['db']['report_total']
        cr_report_total.drop()
        #space
    cr_report_total = Collection(user_local_conn['db'], "report_total", create=True)
    print 'uuuuuuuuuuuuupsertng space unit'
    upsert_space_unit(report_answer ,cr_report_total)
    print 'uuuuuuupserint rentttt'
    upsert_rent_service(report_answer, cr_report_total)
    print 'iiiiiiiinserting services'
    insert_services(report_answer, cr_report_total)
    return True


set_services_total()
