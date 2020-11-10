# coding: utf-8

import time
from pymongo import MongoClient
import datetime


#variables
dbname = 'infosync'
collection_name = 'form_data'

def close_connection(cur_db):
  cur_db.client.close()
  return True

def connect_mongodb(dbname, host='localhost', port=27017):
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
    if objects.count() == 0:
      print('NO RECORDS FOUND')
  except TypeError:
    print('NO RECORDS FOUND')
  return objects


def update_one(cur_col, this_filter, update, upsert=False, bypass_document_validation=False, collation=None, array_filters=None, session=None):
  response = cur_col.update_one(this_filter, update, upsert, bypass_document_validation, collation, array_filters, session)
  print('response', response)
