#Author JoeDuck

import time
from pymongo import MongoClient
import datetime


#variables
dbname = 'infosync_answers_client_96'
collection_name = 'form_answer'

#port=27020
port=27017
host='localhost'
form_id =2050

def connect_mongodb(dbname, host, port):
	client = MongoClient()
	client = MongoClient(host, port)
	cur_db = client[dbname]
	return cur_db

def get_mongo_collection(cur_db, collection_name ):
	#collection_name = 'form_answer'
	collection = cur_db[collection_name]
	return collection

def get_collection_objects(cur_col, query = None):
	if query:
		objects = cur_col.find(query)
	else:
		objects = cur_col.find()
	try:
		if len(objects) == 0:
			print 'NO RECORDS FOUND'
	except TypeError:
		print 'NO RECORDS FOUND'
	return objects

def get_form_fields(host, port, form_id):
	cur_infosync = connect_mongodb('infosync', host, port)
	cur_is_col = get_mongo_collection(cur_infosync, 'form_data' )
	fields = {}
	fields_cur = cur_is_col.find({'form_id':form_id},{'fields':1})
	for field in fields_cur:
		fields.update(field)
	return fields['fields']

file_path ='/tmp/leads_iesa.csv'


def get_file_to_import(file_path):
    #reads the csv file and imports it
	csv_file = open(file_path, 'r')
	field_ids = csv_file.next()
	field_ids = field_ids.strip('\n')
	field_ids = field_ids.split(',')
	answer = []
	for line in csv_file:
	    #line = line.strip('\n')
	    line = line.split(',')
	    try:
		    line_answer = {
			'phone':line[8],
			'email':line[9],
			'date':line[1],
			'name':line[4],
			'lastname':line[5]
			}
	    except IndexError:
			continue
	    answer.append(line_answer)
	return answer

def get_field_json(form_fields=[]):
	if not form_fields:
		form_fields = get_form_fields(host, port, form_id)
	field_json = {}
	for field in form_fields:
		json ={
		field['field_id'].__str__():{
			'label': field['label'],
			'type': field['field_type'],
			'id':field['field_id'].__str__()}
		}
		print 'udpate',json
		field_json.update(json)
	return field_json

form_fields = get_form_fields(host, port, form_id)
fields_json = get_field_json(form_fields)

cur_db = connect_mongodb(dbname, host, port)
cur_col = get_mongo_collection(cur_db, collection_name )

landing = '5549395d01a4de0439331fd7'
estado = '5575d9a201a4de35862db079'

records = get_collection_objects(cur_col, query = None)

def get_landing_relation():
	landing_names={
		"Franke":["http://www.frankemx.mx","Frankemx.mx",],
		"Subzero-Wolf":["http://www.subzero-wolf.mx","subzero-wolf.mx"],
		"Adwords":["adwords",],
		"smegmx.mx":["http://www.smegmx.mx",],
		"Kindred":["http://www.kindred.mx","KINDred.mx","KINDRED.MX","kindred.mx",],
		"Facebook":["FACEBOOK",],
		"Outlet":["http://iesa.cc/outlet","iesa.cc/outlet"],
		"La Familia Perfecta":["http://www.lafamiliaperfecta.com",],
		"Dexa":["http://www.dexa.mx","http://www.Dexa.mx","DEXA"],
	}
	return landing_names

def update_landing_name(dbname, host, port, collection_name):
	landing_names =  get_landing_relation()
	cur_db = connect_mongodb(dbname, host, port)
	cur_col = get_mongo_collection(cur_db, collection_name )
	for landing_name, values in landing_names.iteritems():
		for wrong_name in values:
				records = cur_col.find({'answers.5549395d01a4de0439331fd7':wrong_name})
				for new_record in records:
					record_id = new_record['_id']
					#new_record.update({'answers.5549395d01a4de0439331fd7':landing_name})
					print 'lannnnding name', landing_name
					cur_col.update({'_id':record_id}, {"$set":{'answers':{'5549395d01a4de0439331fd7':landing_name}}})
	return True

def format_date(date):
 	return datetime.datetime.strptime(date,'%m/%d/%Y')


def update_created_at(dbname, host, port, collection_name):
	cur_db = connect_mongodb(dbname, host, port)
	cur_col = get_mongo_collection(cur_db, collection_name )
	load_file = get_file_to_import(file_path)
	count = 0
	update_records = []
	for old_record in load_file:
		records = cur_col.find({'answers.54de8d8a01a4de283446c394':old_record['phone']})
		try:
			new_date = format_date(old_record['date'])
		except:
			pass
		if records.count() > 0:
			rec_json = records.next()
			record_id = rec_json['_id']
			if rec_json['_id'].__str__() not in update_records:
				count +=1
				update_records.append(rec_json['_id'].__str__())
				print 'records updated ...',record_id, 'date', new_date
				cur_col.update({'_id':record_id}, {"$set":{'created_at':new_date}})
	else:
		records2 = cur_col.find({'answers.54de8d8a01a4de283446c395':old_record['email']})
		if records2.count() > 0:
			rec_json2 = records2.next()
			record_id = rec_json2['_id']
			if rec_json2['_id'].__str__() not in update_records:
				count +=1
				update_records.append(rec_json2['_id'].__str__())
				print 'records updated ...',record_id, 'date', new_date
				cur_col.update({'_id':record_id}, {"$set":{'created_at':new_date}})
			else:
				records3 = cur_col.find({'answers.54de8d8a01a4de283446c390':old_record['name'],'answers.54de8d8a01a4de283446c391':old_record['lastname'] })
				if records3.count() > 0:
					rec_json3 = records3.next()
					record_id = rec_json3['_id'].__str__()
					if rec_json3['_id'].__str__() not in update_records:
						count +=1
						update_records.append(rec_json3['_id'].__str__())
						print 'records updated ...',record_id, 'date', new_date
						cur_col.update({'_id':record_id}, {"$set":{'created_at':new_date}})
		print 'TOTAL',count


#update_landing_name(dbname, host, port, collection_name)


update_created_at(dbname, host, port, collection_name)

# 	for new_record in records:
# 			record_id = new_record['_id']
# 			print 'record_id', record_id
# 			#new_record.update({'answers.5549395d01a4de0439331fd7':landing_name})
# 			print 'lannnnding name', landing_name
# 			cur_col.update({'_id':record_id}, {'answers':{'5549395d01a4de0439331fd7':landing_name}})
# 	return True
#
#
# # db.form_answer.aggregate([
# # {"$match":{
# # "form_id":2050,
# # "answers.5549395d01a4de0439331fd7" :{"$exists":true},
# # }},
# # {"$project":
# # {
# # "year":{"$year" : "$created_at"},
# # "month":{"$month" : "$created_at"},
# # "landing":"$answers.5549395d01a4de0439331fd7"
# # }
# # },
# # {"$group":
# # {"_id":
# # {"year":"$year", "month":"$month","landing":"$landing"},
# # "total" : {"$sum" : 1}}}
# # ])
# #
# # {'type': u'group', 'id': '556490af01a4de4631a7fe3d', 'label': u'Seguimiento'}
# # {'type': u'text', 'id': '54de97a201a4de283446c39a', 'label': u'Direcci\xf3n'}
# # {'type': u'text', 'id': '554a60d901a4de0439332097', 'label': u'C\xf3digo Postal'}
# # {'type': u'date', 'id': '556490f101a4de46326bb268', 'label': u'Fecha de Seguimiento'}
# # {'type': u'email', 'id': '55660efe01a4de3fc850d10b', 'label': u'Correo Origen:'}
# # {'type': u'radio', 'id': '555f47a901a4de47e4a9363d', 'label': u'Rep'}
# # {'type': u'textarea', 'id': '556490f101a4de46326bb269', 'label': u'Comentario'}
# # {'type': u'description', 'id': '555f499301a4de47e4a9363f', 'label': u'Equipos'}
# # {'type': u'text', 'id': '54de97a201a4de283446c399', 'label': u'Compa\xf1\xeda'}
# # {'type': u'textarea', 'id': '54de8d8a01a4de283446c397', 'label': u'Mensaje'}
# # {'type': u'text', 'id': '5549395d01a4de0439331fd7', 'label': u'Contacto'}
# # {'type': u'radio', 'id': '553abe9d01a4de236b938fd9', 'label': u'\xbfCu\xe1l de las siguientes opciones describe mejor su inter\xe9s en comprar un electrodom\xe9stico nuevo?'}
# # {'type': u'text', 'id': '54de8d8a01a4de283446c390', 'label': u'Nombre'}
# # {'type': u'text', 'id': '54de8d8a01a4de283446c391', 'label': u'Apellido'}
# # {'type': u'text', 'id': '54de8d8a01a4de283446c392', 'label': u'Ciudad'}
# # {'type': u'text', 'id': '54de8d8a01a4de283446c394', 'label': u'Tel\xe9fono'}
# # {'type': u'email', 'id': '54de8d8a01a4de283446c395', 'label': u'Correo'}
# # {'type': u'select', 'id': '54de8d8a01a4de283446c396', 'label': u'Asunto'}
# # {'type': u'radio', 'id': '555f6a9f01a4de47e4a9364d', 'label': u'Estatus'}
# # {'type': u'radio', 'id': '555f47a901a4de47e4a9363a', 'label': u'Marca'}
# # {'type': u'text', 'id': '556f42a601a4de5a78839353', 'label': u'Dealer'}
# # {'type': u'select', 'id': '5575d9a201a4de35862db079', 'label': u'Estado'}
# # {'type': u'radio', 'id': '5547da1d01a4de0b614a01f7', 'label': u'\xbfActualmente posee alg\xfan producto?'}
# # {'type': u'radio', 'id': '553abe9d01a4de236b938fda', 'label': u'\xbfEst\xe1 siendo asistido por alguno de los siguientes profesionales para su proyecto de cocina?'}
# # {'type': u'textarea', 'id': '556490f101a4de46326bb26b', 'label': u'Siguiente Acci\xf3n'}
# # {'type': u'date', 'id': '556f42a601a4de5a78839355', 'label': u'Contacto Dealer'}
# # {'type': u'radio', 'id': '5547da1d01a4de0b614a01f8', 'label': u'\xbfQu\xe9 tan pronto piensa adquirir un producto?'}
# # {'type': u'date', 'id': '555f47a901a4de47e4a9363c', 'label': u'Cat\xe1logo y asignaci\xf3n de rep'}
# # {'type': u'date', 'id': '556490f101a4de46326bb26a', 'label': u'Fecha de Siguiente Acci\xf3n'}
# # {'type': u'text', 'id': '556f42a601a4de5a78839354', 'label': u'Vendedor Dealer'}
# #
# #
# #
# # DEXA, http://www.Dexa.mx, http://www.dexa.mx = Dexa
# # FACEBOOK = Facebook
# # Frankemx.mx, http://www.frankemx.mx = Franke
# # KINDRED.MX, KINDred.mx, http://www.kindred.mx, kindred.mx = Kindred
# # Outlet, http://iesa.cc/outlet = iesa.cc/outlet
# # adwords = Adwords
# # http://www.lafamiliaperfecta.com = La Familia Perfecta
# # http://www.smegmx.mx = smegmx.mx
# # http://www.subzero-wolf.mx, subzero-wolf.mx = Subzero-Wolf
