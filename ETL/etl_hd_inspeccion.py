#coding: utf-8
from pymongo import MongoClient
from pymongo.collection import Collection
import json

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
        self.filters = [filter.decode('utf-8') for filter in self.filters]
        self.user_id = kwargs["user_id"]
        #created_at = kwargs["created_at"]
        #updated_at = kwargs["updated_at"]
        #expiration = kwargs["expiration"]
        #active = True

def etl():
    # Repetir para cada modelo en la tabla de reportes
    #item = Item.objects.get(id=524)
    items_to_search  = [2008]
    tipos = json.loads(open("tipos.json").read())
    for item in items_to_search:
	    # Modelo para pruebas
            print 'item=', item
	    etl_model = FakeETLModel(
		**{
		    'name': 'Reporte', 'item_id':  item, 'user_id': 126,
		    'filters': ['Tienda:']
		    }
	    )

	    user_conn = get_user_connection(etl_model.user_id)
	    # Form answer collection
	    form_answer = user_conn['db']['form_answer']

	    # Obtener coleccion de reportes si existe, crear si aún no existe
	    if 'report_answer' in user_conn['db'].collection_names():
		report_answer = user_conn['db']['report_answer']
	    else:
		report_answer = Collection(user_conn['db'], "report_answer", create=True)

	    # Plantilla del reporte
	    report = { "form_id": etl_model.item_id, "answers": [] }
            # Recorrer todos los registros de la forma
	    for record in form_answer.find({"form_id": etl_model.item_id}):
		# Diccionario para obtener campos dado su id
		fields = {}
		# Diccionario para obtener campos dado su label (para filtros)
		filter_fields = {}
		for page in record["voucher"]["form_pages"]:
		    for field in page["page_fields"]:
			field["page"] = page["page_name"]
			fields[field["field_id"]["id"]] = field
			if field['label'] in etl_model.filters:
			    filter_fields[field["label"]] = field
		
		tmp_filters = {}
		for filter_id in etl_model.filters:
		    tmp_filters[filter_id] = record["answers"].get(filter_fields[filter_id]["field_id"]["id"])
		# Recorrer cada respuesta
		for field_id in record["answers"]:
		    answer = record["answers"][field_id]
		    
		    # METADATA
		    new_answer = {
			"field_id": field_id,
			"page_name": fields[field_id]["page"],
			"field_type": fields[field_id]["field_type"],
			"field_text": fields[field_id]["label"],
                        "help_text": fields[field_id].get("help_text"),
                        "type": tipos.get(field_id)
		    }
                    if tipos.get(field_id): print tipos[field_id]
		    meta = ["browser", "created_at", "updated_at", "end_date", "ip", "platform", "start_date"]
		    for key in meta:
			new_answer[key] = record.get(key)

		    # Añadir valores de filtros (si todos fueron contestados)
		    if all(tmp_filters.values()):
			#new_answer.update(tmp_filters)
			for key in tmp_filters:
			    #print 'key', key
			    new_answer[key.lower()] = tmp_filters[key]

		    # Formatear respuesta dependiendo del tipo
		    # Imagen, Documento, Firma
		    if type(answer) == dict:
			continue
			#ew_answer["file_url"] = answer["file_url"]
			#new_answer["file_name"] = answer["file_name"]
			#report["answers"].append(new_answer)
		    # Opcion multiple
		    elif type(answer) == list:
			options = {}
			for option in fields[field_id]["options"]:
			    	print option
				options[option["value"]] = option["label"]
			for value in answer:
			    if options.get(value):
				new_answer["field_value"] = options[value]
			    else:
				new_answer["field_value"] = value
			    report["answers"].append(new_answer)
		    # Demás tipos de campos 
		    else:
			if fields[field_id]["field_type"] == "radio":
			    options = {}
			    for option in fields[field_id]["options"]:
				options[option["value"]] = option["label"]
			    if options.get(answer):
				new_answer["field_value"] = options[answer]
			    else:
				new_answer["field_value"] = answer
			    report["answers"].append(new_answer)
			else:
			    #print field["field_type"], answer
			    new_answer["field_value"] = answer
			    report["answers"].append(new_answer)
	    # Editar reporte si existe, crear si no es así
	    if report_answer.find({"form_id": etl_model.item_id}).count() > 0:
		report_answer.update({"form_id": etl_model.item_id}, report)
	    else:
		report_answer.insert(report)
etl()

