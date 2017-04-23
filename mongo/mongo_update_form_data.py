#Author JoeDuck

import time
from pymongo import MongoClient
import datetime


#variables
dbname = 'infosync'
collection_name = 'form_data'


def connect_mongodb(dbname, host='localhost', port=27017):
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

def check_date_default_value(records):
	if len(records) == 0:
		print 'NO RECORDS FOUND'
	for rec in records['fields']:
		if rec['field_type'] == 'date':
			if rec['default_value']:
				print rec['field_type']

cur_db = connect_mongodb(dbname, host='localhost', port=27017)
cur_col = get_mongo_collection(cur_db, collection_name )

records = get_collection_objects(cur_col, query = None)







