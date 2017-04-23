#coding: utf-8
from pymongo import MongoClient
from pymongo.collection import Collection
from sys import stderr
import json, re

host = 'localhost'
local_port = 27017
testing_port = 27020
production_port = 27019

form_ids  = [4534, 4535, 4536]

orden_servicio_json = {
    # Datos iniciales 
    '55e85d9f23d3fd0ca23d7908':'formato_servicio',
    '55e85d9f23d3fd0ca23d7907':'nombre_cliente',
    '55e85d9f23d3fd0ca23d790a':'fecha_servicio',
    '55e85d9f23d3fd0ca23d790c':'ruta_servicio',
    '55e85d9f23d3fd0ca23d790d':'precio_servicio',

    # Tratamiento 
    '55e85d9f23d3fd0ca23d790f':'producto',
    '55e85d9f23d3fd0ca23d7915':'area',

    # Cebaderos Roedores Exterior 
    '55e85d9f23d3fd0ca23d7919':'tipo_dispositivo_ext',
    '55e85d9f23d3fd0ca23d791a':'numero_dispositivo_ext',
    '55e85d9f23d3fd0ca23d791b':'condicion_dispositivo_ext',
    '55e85d9f23d3fd0ca23d791d':'accion_realizada_ext',
    '55e881dc23d3fd0ca0bdde64':'rata_ext',
    '55e881dc23d3fd0ca0bdde65':'raton_ext',
    '55e881dc23d3fd0ca0bdde66':'cucaracha_alemana_ext',
    '55e881dc23d3fd0ca0bdde67':'cucaracha_americana_ext',
    '55e881dc23d3fd0ca0bdde68':'hormiga_ext',
    '55e881dc23d3fd0ca0bdde69':'mosca_ext',
    '55e8bf7323d3fd685b7ff0cf':'palomilla_ext',
    '55e8bf7323d3fd685b7ff0d0':'gorgojo_ext',
    '55ee015723d3fd65cb47fbe2':'otra_ext',
    '55eef43f23d3fd6d6a65d4da':'descripcion_otra_ext',


    # Trampas Mecanicas Roedor Interior 
    '55e85d9f23d3fd0ca23d7920':'tipo_dispositivo_int',
    '55e85d9f23d3fd0ca23d7921':'numero_dispositivos_int',
    '55e85d9f23d3fd0ca23d7922':'condicion_dispositivo_int',
    '55e85d9f23d3fd0ca23d7924':'accion_realizada_int',
    '55e85d9f23d3fd0ca23d7925':'rata_int',
    '55e8875323d3fd0ca1472827':'raton_int',
    '55e8875323d3fd0ca1472828':'cucaracha_alemana_int',
    '55e8875323d3fd0ca1472829':'cucaracha_americana_int',
    '55e889ea23d3fd0ca0bdde72':'hormiga_int',
    '55e8875323d3fd0ca147282a':'mosca_int',
    '55e8bfe923d3fd685de86e35':'palomilla_int',
    '55e8bfe923d3fd685de86e36':'gorgojo_int',
    '55ee065b23d3fd6d6a65d45d':'otra_int',
    '55eef47523d3fd6d69400649':'descripcion_otra_int',

    # Trampas de Luz UV Voladores 
    '55e85d9f23d3fd0ca23d7927':'tipo_dispositivo_luz',
    '55e85d9f23d3fd0ca23d7928':'numero_dispositivo_luz',
    '55e85d9f23d3fd0ca23d7929':'condicion_dispositivo_luz',
    '55e85d9f23d3fd0ca23d792b':'accion_dispositivo_luz',
    '55e88ab323d3fd0ca23d79d8':'mosca_luz',
    '55e88ab323d3fd0ca23d79d6':'mosca_fruta_luz',
    '55e8cc0223d3fd685de86e53':'mosquita_drenaje_luz',
    '55e88ab323d3fd0ca23d79d9':'mosquito_luz',
    '55e88ab323d3fd0ca23d79da':'gorgojo_luz',
    '55e8c14f23d3fd685de86e37':'palomilla_luz',
    '55e88ab323d3fd0ca23d79db':'termita_luz',
    '55e88ab323d3fd0ca23d79d7':'hormiga_luz',
    '55ee06bf23d3fd6d6a65d460':'otra_luz',
    '55eef4a823d3fd6d6a65d4db':'descripcion_otra_luz',

    # Trampas de Feromonas 
    '55e85d9f23d3fd0ca23d792e':'tipo_dispositivo_fer',
    '55e85d9f23d3fd0ca23d792f':'numero_dispositivo_fer',
    '55e85d9f23d3fd0ca23d7930':'condicion_dispositivo_fer',
    '55e85d9f23d3fd0ca23d7932':'accion_dispositivo_fer',
    '55e88c1123d3fd0ca147282d':'cucaracha_alemana_fer',
    '55e88c1123d3fd0ca1472830':'gorgojo_fer',
    '55e88c1123d3fd0ca147282e':'palomilla_fer',
    '55e88c1123d3fd0ca147282f':'mosca_fer',
    '55e8c2ce23d3fd685de86e38':'otra_fer',
    '55e8c2ce23d3fd685de86e39':'descripcion_otra_fer',

    # Otras Trampas 
    '55e85d9f23d3fd0ca23d7935':'tipo_dispositivo_otra',
    '55e85d9f23d3fd0ca23d7936':'numero_dispositivo_otra',
    '55e85d9f23d3fd0ca23d7937':'condicion_dispositivo_otra',
    '55e85d9f23d3fd0ca23d7939':'accion_dispositivo_otra',
    '55e8c39e23d3fd685cc98b12':'cantidad_plaga_encontrada_otra',
    '55ee084c23d3fd6d6940061f':'descripcion_plaga_encontrada_otra',

    # Acciones Correctivas 
    '55e85d9f23d3fd0ca23d793c':'categoria',
    '55e85d9f23d3fd0ca23d793d':'actividad_pendiente_hacer',
    '55e85d9f23d3fd0ca23d793e':'accion_realizar_parte',
    '55e85d9f23d3fd0ca23d793f':'fecha_compromiso_terminar',
    '55e85d9f23d3fd0ca23d7940':'estatus',
    '55e88f5923d3fd0ca1472836':'fecha_realizado',

    # Comprobante de Servicio 
    '55e85d9f23d3fd0ca23d7941':'nombre_tecnico',
    '55e85d9f23d3fd0ca23d7943':'nombre_cliente'    
}


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


def warning(*objs):
    '''
    To print stuff at stderr
    '''
    output = "warning:%s\n" % objs
    stderr.write(output)


class FakeETLModel(object):
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        #rtype = kwarghs["rtype"]
        self.item_id = kwargs["item_id"]
        self.filters = kwargs["filters"]
        self.user_id = kwargs["user_id"]
	self.group_filters = kwargs["group_filters"]
        #created_at = kwargs["created_at"]
        #updated_at = kwargs["updated_at"]
        #expiration = kwargs["expiration"]
        #active = True

def get_answer(answers, field):
    # Formatear respuesta dependiendo del tipo de campo
    field_id = field["field_id"]["id"]
    answer = answers.get(field_id)
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
    elif field["field_type"] == "radio":
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
    # Demás tipos
    else:
        return answer

def get_new_answer(record, fields, field_id, tmp_filters, types_dictionary):
    #answer = record["answers"][field_id]
    #field = fields[field_id]
    #if fields["field_type"] in ["radio"]: print 'radio'
    # METADATA
    new_answer = {
    "field_id": field_id,
    "page_name": fields[field_id]["page"],
    "field_type": fields[field_id]["field_type"],
    "field_text": fields[field_id]["label"],
    "tipo": types_dictionary.get(field_id, None)
    }
    meta = ["version", "created_at", "updated_at", "end_date", "ip", "platform", "start_date"]
    for key in meta:
        new_answer[key] = record.get(key)

    # Añadir valores de filtros (si todos fueron contestados)
    #if all(tmp_filters.values()):
    #new_answer.update(tmp_filters)
    print 'tmp_filters',tmp_filters
    # for key in tmp_filters:
    #     print 'key', key
    #     if key in ['Manzana','Lote']:
    #         print 'va a tratar de ser int ', tmp_filters[key]
    #         value = int(tmp_filters[key])
    #         new_answer[key.lower()] = '%02d'%value
    #     else:
    #         new_answer[key.lower()] = tmp_filters[key]
    #new_answer["field_value"] = get_answer(record["answers"], fields[field_id])
    return new_answer


def etl():
    
    etl_model = FakeETLModel(
        **{
            'name': 'Reporte', 'item_id':  form_ids, 'user_id': 126,
            'filters': orden_servicio_json.keys(),
	    'group_filters': []
        }
    )

    user_production_conn = get_user_production_connection(etl_model.user_id)
    form_answer = user_production_conn['db']['form_answer']
    
    user_local_conn = get_user_local_connection(etl_model.user_id)        

    if 'report_answer' in user_local_conn['db'].collection_names():
        report_answer = user_local_conn['db']['report_answer']
        report_answer.drop()
    report_answer = Collection(user_local_conn['db'], "report_answer", create=True)
    report = {}
    count = 0

    #print vars(form_answer.find({"form_id": {"$in":etl_model.item_id}}))

    for record in form_answer.find({"form_id": {"$in":etl_model.item_id}}):
        count +=1
        print 'records ', count
        record_answer = {}
        pass_all = False
        fields = {}
        filter_fields = {}
        tmp_filters = {}
        for page in record["voucher"]["form_pages"]:
            for field in page["page_fields"]:
                field["page"] = page["page_name"]
                fields[field["field_id"]["id"]] = field
                if field['label'] in etl_model.filters:
                        filter_fields[field["label"]] = field   
                        tmp_filters = {}
            for filter_id in etl_model.filters:
                try:
                    tmp_filters[filter_id] = get_answer(record["answers"], fields[filter_fields[filter_id]["field_id"]["id"]])
                except KeyError:
                    pass

        # Recorrer cada respuesta
        for field_id in record["answers"]:
            field_type = fields[field_id]["field_type"]
            if field_type == 'group':
		group_fields = get_answer(record["answers"], fields[field_id])
		for group_items in group_fields:
		    group_filters = {}
		    #agrega los filtros que pertencen a un grupo
                    for filter_id in etl_model.group_filters:
			try:
			    filter_key = re.sub(' ','_',filter_id.lower())
                            group_filters.update({filter_key:get_answer(group_items, fields[filter_fields[filter_id]["field_id"]["id"]])})
			except KeyError:
			    pass
		    for group_field in group_items.items():
			new_answer = get_new_answer(record, fields, group_field[0], tmp_filters, types_dictionary)
			new_answer.update(group_filters)
			new_answer["field_value"] = get_answer({group_field[0]:group_field[1]}, fields[group_field[0]])
			report["answers"].append(new_answer)
            else:
		new_answer = get_new_answer(record, fields, field_id, tmp_filters, types_dictionary)
		#print '-------------------------'
		#print 'fields[field_id]',fields[field_id]
                new_answer["field_value"] = get_answer(record["answers"], fields[field_id])
                try:
                    if (new_answer['concepto'] and new_answer['concepto']  == 'Entrega DOS M-Cliente' and new_answer['lote'] == '07' and new_answer['manzana'] == '525' and (new_answer['field_value'] != u'ok' and new_answer['field_value'] != u'OK' and new_answer['field_value'] != None)):
                        if(new_answer['field_value'].find("Pendiente") != -1) or (new_answer['field_value'].find("PENDIENTE") != -1):
                            warning(new_answer)
                except:
                    pass
                report["answers"].append(new_answer)
        # Editar reporte si existe, crear si no es así
        if report_answer.find({"form_id": etl_model.item_id}).count() > 0:
            report_answer.update({"form_id": etl_model.item_id}, report)
        else:
            report_answer.insert(report)
etl()

