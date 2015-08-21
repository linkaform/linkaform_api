#coding: utf-8
from pymongo import MongoClient
from pymongo.collection import Collection
import json, re


# Create your views here.

def get_user_connection(user_id):
    connection = {}
    connection['client'] = MongoClient()

    user_db_name = "infosync_answers_client_{0}".format(user_id) 

    if not user_db_name:
        return None
    connection['db'] = connection['client'][user_db_name]   

    return connection

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
    meta = ["browser", "created_at", "updated_at", "end_date", "ip", "platform", "start_date"]
    for key in meta:
        new_answer[key] = record.get(key)

    # Añadir valores de filtros (si todos fueron contestados)
    #if all(tmp_filters.values()):
    #new_answer.update(tmp_filters)
    for key in tmp_filters:
        if key in ['Manzana','Lote']:
            value = int(tmp_filters[key])
            new_answer[key.lower()] = '%02d'%value
        else:
            new_answer[key.lower()] = tmp_filters[key]
    #new_answer["field_value"] = get_answer(record["answers"], fields[field_id])
    return new_answer


def etl():
    # Repetir para cada modelo en la tabla de reportes
    #item = Item.objects.get(id=524)
    #items_to_search  = [516,517,549,554,2119]
    items_to_search = [2119,]
    types = open("tipos.json", "r")
    types_dictionary = json.loads(types.read())
    for item in items_to_search:
        # Modelo para pruebas
        etl_model = FakeETLModel(
        **{
            'name': 'Reporte', 'item_id':  item, 'user_id': 94,
            'filters': ['FRACCIONAMIENTO','Fraccionamiento', 'Manzana', 'Lote', 'Concepto'],
	    'group_filters': ['Dictamen Tecnico',]
            }
        )

        user_conn = get_user_connection(etl_model.user_id)
        # Form answer collection
        form_answer = user_conn['db']['form_answer']

        # Obtener coleccion de reportes si existe, crear si aún no existe
        if 'report_answer_g' in user_conn['db'].collection_names():
            report_answer = user_conn['db']['report_answer_g']
        else:
            report_answer = Collection(user_conn['db'], "report_answer_g", create=True)

        # Plantilla del reporte
        report = { "form_id": etl_model.item_id, "answers": [] }
        # Recorrer todos los registros de la forma
        for record in form_answer.find({"form_id": etl_model.item_id}):
	    print 'record =============='
            # Diccionario para obtener campos dado su id
            fields = {}
            # Diccionario para obtener campos dado su label (para filtros)
            filter_fields = {}
            for page in record["voucher"]["form_pages"]:
                for field in page["page_fields"]:
                    field["page"] = page["page_name"]
                    fields[field["field_id"]["id"]] = field
                    if field['label'] in etl_model.filters + etl_model.group_filters:
                        filter_fields[field["label"]] = field   
            tmp_filters = {}
            for filter_id in etl_model.filters:
                try:
                    tmp_filters[filter_id] = get_answer(record["answers"], fields[filter_fields[filter_id]["field_id"]["id"]])
                except KeyError:
                    pass
            group_tmp_filters = {}
            # Recorrer cada respuesta
            for field_id in record["answers"]:
                field_type = fields[field_id]["field_type"]
                if field_type == 'group':
		    group_fields = get_answer(record["answers"], fields[field_id])
		    for group_items in group_fields:
			group_filters = {}
			#agrega los filtros que pertencen a un grupo
                        for filter_id in etl_model.group_filters:
			    print 'agreaga filtro de grupo'
			    try:
				print 'llave', filter_id
				filter_key = re.sub(' ','_',filter_id.lower())
                            	group_filters.update({filter_key:get_answer(group_items, fields[filter_fields[filter_id]["field_id"]["id"]])})
				print 'answer', new_answer
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
                    report["answers"].append(new_answer)

        # Editar reporte si existe, crear si no es así
        if report_answer.find({"form_id": etl_model.item_id}).count() > 0:
            report_answer.update({"form_id": etl_model.item_id}, report)
        else:
            report_answer.insert(report)
etl()

