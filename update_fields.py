
from pymongo import MongoClient

def get_data(fields_type_to_find, value_to_option):
	query = {
	    "form_pages.page_fields.field_type": {"$in": fields_type_to_find},
	    "form_pages.page_fields."+option_to_find: {"$in": value_to_option},
	}
	data = [row for row in collection.find(query)]
	print "total formas a editar ", len(data)
	return data


def get_data_from_query(query={}):
	data = [row for row in collection.find(query)]
	print "total formas a editar ", len(data)
	return data

def replace_values(data):
    for field in data:
        if field['field_type'] in fields_type_to_find and field[option_to_find] in value_to_option:
            field[option_to_find] = value_to_replace
    return data

def update_mongo(data):
	for form in data:
	    for page in form["form_pages"]:
		page["page_fields"] = replace_values(page["page_fields"])
	    if form.has_key('fields'):
		    form["fields"] = replace_values(form["fields"])
	    collection.update({'_id': form['_id']}, form, True)

def data_log(form, field):
	print '-----------------------------------'
	print 'form_id =', form['form_id']
	print 'field_type = ', field['field_type']
	print 'default_value = ', field['default_value']

def print_data(fields_type_to_find, option_to_find, value_to_option=None):
	data = [x for x in collection.find()]
	for form in data:
		if 'fields' in form:
			for field in form['fields']:
				if "field_type" in field and\
					field['field_type'] in fields_type_to_find and\
					option_to_find in field and field[option_to_find]:
						if value_to_option:
			 				if field[option_to_find] in value_to_option:
								data_log(form, field)
						else:
							data_log(form, field)


######
# Remplaza o agrega la variable de metadatos de la forma de confirmation
######

def update_metadata(data, key_to_update, new_info = {}):
	print 'entra a update_metadata'
	for form in data:
		print '======start====='
		print 'has keys', form['form_id']
		if form.has_key(key_to_update):
			if form[key_to_update].keys():
				print 'yes'
				pass
			else:
				print 'no'
				form[key_to_update].update(new_info)
				print 'update info'
		form[key_to_update] = new_info
		print 'new info... updating'
		collection.update({'_id': form['_id']}, form, True)
		print 'inject info to', form['form_id']
		print '-----next----'

def test_confirmation_update(data, key_to_update):
	print 'Forms to test', len(data)
	tested = 0
	faild = 0 
	for form_test in data:
		if form_test.has_key(key_to_update):
			if form_test[key_to_update].keys():
				tested +=1
				continue
		faild +=1
	print 'forms that pass the test', tested
	print 'forms FAILD', faild


### Configuración de Base de datos ####
#######################################
client = MongoClient("mongodb://localhost:27017")
db_name = 'infosync'
collection_name = 'form_data'
db = client[db_name]
collection = db[collection_name]
#######################################


### Configurar datos a buscar #############

# Que tipos de campos estas buscando
fields_type_to_find = ['date', 'datetime', 'time']
#que opcion quieres encontrar
option_to_find = "default_value"
#que valores quieres reemplazar
value_to_option = [[], "opcion_1"]
# por que valor los quieres reemplazar
value_to_replace = ""

# Configurar
fields_type_to_find = ['checkbox']
option_to_find = "default_value"
value_to_option = ["opcion_1", u"desinsectización", "ceremonia_de_entrega_de_medallas"]
value_to_replace = ""



print_data(fields_type_to_find, option_to_find, value_to_option)

data = get_data(fields_type_to_find, value_to_option)

update_mongo(data)



query = {}
data = get_data_from_query(query)
key_to_update = 'confirmation'
new_info = {"button_message": "Mandar respuestas", 
		"message": "¡Su información fue capturada!", 
		"redirect_url": "default"}
test_confirmation_update(data, key_to_update)
update_metadata(data, key_to_update, new_info)
new_data = get_data_from_query(query)

test_confirmation_update(new_data, key_to_update)

data = get_data_from_query(query)

"confirmation": {"button_message": "Mandar respuestas", "message": "¡Su información fue capturada!", "redirect_url": "default"},



