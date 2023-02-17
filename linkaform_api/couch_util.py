# -*- coding: utf-8 -*-
#####
#
import sys, simplejson, math ,time, requests
from couchdb import Server

class Couch_utils(object):

    def __init__(self, settings={}):
        if settings.config['COUCH_ENV'] == 'prod':
            couch_pord_url = "{}://{}:{}@{}:{}".format(
                settings.config['COUCH_PROTOCOL'],
                settings.config['COUCH_USER'],
                settings.config['COUCH_PASSWORD'],
                settings.config['COUCH_HOST'],
                settings.config['COUCH_PORT'])
            self.cdb = Server(couch_pord_url)
            self.cdb_dest = Server(couch_dev_url)
            self.url_prod = "{}://{}:{}/".format(
                settings.config['COUCH_PROTOCOL'],
                settings.config['COUCH_HOST'],
                settings.config['COUCH_PORT']
                )
            self.host = "{}://{}:{}@{}".format(
            settings.config['COUCH_PROTOCOL'],
                settings.config['COUCH_USER'],
                settings.config['COUCH_PASSWORD'],
                settings.config['COUCH_HOST'],
                )
        elif settings.config['COUCH_ENV'] == 'dev':
            couch_dev_url = "{}://{}:{}@{}:{}".format(
                settings.config['COUCH_DEV_PROTOCOL'],
                settings.config['COUCH_DEV_USER'],
                settings.config['COUCH_DEV_PASSWORD'],
                settings.config['COUCH_DEV_HOST'],
                settings.config['COUCH_DEV_PORT'])
            self.cdb = Server(couch_dev_url)
            self.cdb_dest = Server(couch_dev_url)
            self.url_test = "{}://{}:{}/".format(
                settings.config['COUCH_DEV_PROTOCOL'],
                settings.config['COUCH_DEV_HOST'],
                settings.config['COUCH_DEV_PORT']
                )
            self.host = "{}://{}:{}@{}".format(
                settings.config['COUCH_DEV_PROTOCOL'],
                settings.config['COUCH_DEV_USER'],
                settings.config['COUCH_DEV_PASSWORD'],
                settings.config['COUCH_DEV_HOST'],
                )
        self.max_replications = 20
        self.cr = None

    def set_db(self, dbname):
      self.cr = self.cdb[dbname]
      return self.cr

    def get_replicator(self, org_dbname, dest_dbname):
      replicator = {

        "user_ctx": {
          "name": "admin",
          "roles": [
            "_admin",
            "_reader",
            "_writer"
          ]
        },
        "source": {
          "headers": {
            "Authorization": "Basic YWRtaW46bGlua2Fmb3JtMjAxOHNlcnZlci4="
          },
          "url": org_dbname
        },
        "target": {
          "headers": {
            "Authorization": "Basic bGlua2Fmb3JtOjIwMThsaW5rYWZvcm10ZXN0Kg=="
          },
          "url": dest_dbname
        },
        "create_target": True,
        "continuous": False,
        "owner": "admin",
        }
      return replicator

    def delete_records(self, cr, cr_inbox, verbose=False):
        total =len(cr_inbox)
        if verbose:
            print('total', total)
        blocks = int(math.ceil(total/50.0))
        block_size = 50
        for i in range(blocks):
          before = block_size * i
          after = block_size * (i+1)
          if verbose:
            print('before', before, "after", after)
          cr.purge(cr_inbox[before:after])
        #cr.compact()
        return True

    def count_running_replications(self):
        db = '_replicator'
        cr_prod = self.cdb[db]
        mango_running = {
        "selector": {
          "continuous": False,
          "$or":[
            {"_replication_state": "running"},
            {"_replication_state": {"$exists":False}}
          ]
          },
        "limit":10000
        }
        running = cr_prod.find(mango_running)
        return len(running)

    def delete_completed_replications(self):
      db = '_replicator'
      cr_prod = self.cdb[db]
      mango_completed = {
        "selector": {
          "continuous": False,
          "_replication_state": "completed",
          },
        "limit":10000
      }
      completed = cr_prod.find(mango_completed)
      self.delete_records(cr_prod, completed)

    def delete_database(self, dbname):
      try:
        del self.cdb[dbname]
        return True
      except:
        return 'not found'

    def delete_database_dest(self, dbname):
      try:
        del self.cdb_dest[dbname]
        return True
      except:
        return 'not found'

    def delete_records(self, cr, records):
        print( 'deleteing {} records'.format(len(records)))
        for i in records:
            cr.delete(i)

    def replicate_user_inbox(self ,dbname_id):
      db_type = 'user'
      rep_id, rep_rev = db_replication(dbname_id, db_type)
      return rep_id, rep_rev

    def replicate_catalog_records(self ,dbname_id, account_id):
      db_type = 'catalog_records'
      rep_id, rep_rev = db_replication(dbname_id, db_type)
      print('replcation done')
      catalog_model = get_catalog_model(dbname_id, account_id)
      print('catalog model')
      set_catalog_model(catalog_model, account_id)
      print('setting catalog model done')
      return True

    def get_catalog_model(self, catalog_id, account_id):
      query = {
        "selector": {
        "catalog_id":{
            "$eq": int(catalog_id)
            },
        },
      }
      dbname = "client_{}_catalog_model".format(account_id)
      try:
        catalog_model = self.cdb[dbname]
      except:
        return {}
      if catalog_model:
        doc = catalog_model.find(query)
        print( doc)
        if len(doc) > 0:
          return doc[0]
      return {}

    def delete_catalog_model(self, catalog_id, account_id):
      doc = self.get_catalog_model(catalog_id, account_id)
      dbname = "client_{}_catalog_model".format(account_id)
      catalog_model = self.cdb[dbname]
      print( 'doc', doc.get('_id'))
      if  doc.get('_id'):
        catalog_model.purge([doc])
      #user_inbox.purge(records_to_delete[before:after])
      #user_inbox.compact()

    def set_catalog_model(self, doc, account_id):
      dbname = "client_{}_catalog_model".format(account_id)
      try:
        client_db = self.cdb[dbname]
      except:
        client_db = self.cdb.create(dbname)
      doc.pop('_rev')
      print(doc)
      return client_db.update([doc])

    def get_catalog_name(self, cur, catalog_id):
        query = "select name from items_item where id = {}".format(catalog_id)
        cur.execute(query)
        item_name = cur.fetchone()
        return item_name

    def db_replication(self, dbname_id, db_type):
      db = '_replicator'
      cr_prod = self.cdb[db]
      security = cr_prod.security
      if db_type == 'catalog_records':
        dbname = "catalog_records_{}".format(dbname_id)

      elif db_type == 'user':
        dbname = "user_inbox_{}".format(dbname_id)

      elif db_type == 'account':
        dbname = "account_properties_{}".format(dbname_id)

      elif db_type == 'models':
        dbname = "client_{}_catalog_model".format(dbname_id)

      elif db_type in  ('groups', 'imagenes'):
        dbname = db_type
      else:
        dbname = db_type

      org_dbname = self.url_prod + dbname
      dest_dbname = self.url_test + dbname
      while  self.count_running_replications() > self.max_replications:
        print('... waiting for replicatoins running :', self.count_running_replications())
        time.sleep(4)
      self.delete_database_dest(dbname)
      time.sleep(1)
      rep_id, rep_rev = cr_prod.save(self.get_replicator(org_dbname,dest_dbname))
      cr_dest = self.cdb_dest[db]
      cr_dest.security = security
      return rep_id, rep_rev

    def purge(self, rec_id):
      self.cr.purge(rec_id)

    def delete(self, rec_id):
      self.cr.delete(rec_id)

    def set_index(self, db_name, fields, name, partitioned=False):
        url = "{}/{}/_index".format(self.host, db_name)
        headers = {'Content-type': 'application/json'}
        params ={
                "index": {
                    "fields": fields,
                        },
                "name" : name,
                "type" : "json"
                #"partial_filter_selector": {}
                #https://docs.couchdb.org/en/stable/api/database/find.html#api-db-find-index
                }
        if partitioned:
            params.update({"partitioned":True})
        print('url', url)
        r = requests.post(url, json=params, headers=headers)
        res = r.json()
        res['status_code'] = r.status_code
        return res
