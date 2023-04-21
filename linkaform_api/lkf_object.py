print('loading lkf_object ...')

#python libs
from bson import ObjectId
from hashlib import sha1, md5

from app import bob
from .base_models import UserData

# from  import UserData

#Flask Models
from flask_pymongo import PyMongo


#### LKF Object
class LKFBaseObject:


    def get_mongo_uri(self, account_id):
        dbname = 'infosync_answers_client_{}'.format(account_id)
        alias = 'client_{}'.format(account_id)
        mongo_user = 'account_{}'.format(account_id)
        alias = alias.encode('utf-8')
        encode_alias = '{}{}'.format(md5(alias).hexdigest(), '_lkf').encode('utf-8')
        user_pass = sha1(encode_alias).hexdigest()
        authSource = 'admin'
        uri = 'mongodb://{}:{}@{}/{}'.format(
        mongo_user,
        user_pass,
        bob.config['MONGO_HOST'],
        dbname,
        )
        return uri

    def __init__(self, *, id: str, object: str = None, created_by: UserData = None):
        self.id = id
        self.created_by = created_by
        self.object = object
        self.cr_con = {}

    def __conect_db(self):
        if isinstance(self.created_by, dict):
            account_id =self.created_by.get('account_id', self.created_by.get('parent_id'))
        else:
        # if type(self.created_by) is LKFBaseObject:
            if  hasattr(self.created_by, "parent_id"):
                account_id = self.created_by.parent_id
            if  hasattr(self.created_by, "account_id"):
                account_id = self.created_by.account_id
        dbname = 'infosync_answers_client_{}'.format(account_id)
        if not bob.config['MONGO_CR'].get(dbname):
            bob.config['MONGO_URI'] = self.get_mongo_uri(account_id)
            mongo = PyMongo(bob)
            bob.config['MONGO_CR'][dbname] = PyMongo(bob)
        return bob.config['MONGO_CR'][dbname]

    def get_db_cr(self, _object=None, db_name=False, collection=False):
        if not _object:
            collection = self.object
        else:
            g = _object.__class__
            collection = g.__name__
        # mongo = PyMongo(bob)
        mongo =  self.__conect_db()
        d  = mongo.db
        conn = eval('mongo.db.{}'.format(collection))
            #conn = self.lkf_obj
        #TODO Create database indexes
        # print('sellf', self.lkf_obj)
        # print('seleeelf ======', self.lkf_obj['account_{}'.format(self.created_by.account_id)])
        # return self.lkf_obj['account_{}'.format(self.created_by.account_id)]
        return conn

    def _edit_record(self, cr, data):
        try:
        #if True:
            res = {}
            dag_obj = cr.find({"_id":data['_id']})
            #dag_obj = cr.find({"_id"})
            dag_data = dag_obj.next()
            res['_id'] =  dag_data.get("_id")
            res['rec_id'] =  dag_data.get("_id")
            res['move_type'] = 'edit'
            res['status_code'] = 200
            if True:
                #TODO revisar cuando puede ser update y cuando replace
                cr.find_one_and_replace({"_id":data['_id']}, data)
            else:
                cr.find_one_and_update({"_id":data['_id']}, {"$set":data})
        except:# StopIteration:
             res.update(self._insert_record(cr, data))
        return res



    def _insert_record(self, cr, data):
        res = {}
        if type(data) == list:
            res = []
            for x in data:
                if x.get('lkf_obj'):
                    x.pop('lkf_obj')
            dag_obj_list = cr.insert_many(data)
            if dag_obj_list.acknowledged:
                for x in dag_obj_list.inserted_ids:
                    this_r = {}    
                    this_r['_id'] =  x
                    # this_r['rec_id'] =  x.inserted_id
                    this_r['status_code'] = 201
                    this_r['move_type'] = 'insert'
                    res.append(this_r)
        else:
            if data.get('lkf_obj'):
                data.pop('lkf_obj')
            if not data.get('_id'):
                data['_id'] = ObjectId()
            dag_obj = cr.insert_one(data)
            res['_id'] =  dag_obj.inserted_id
            res['rec_id'] =  dag_obj.inserted_id
            res['status_code'] = 201
            res['move_type'] = 'insert'
        return res

    def get_cr_data(self, _object=None, is_json=False, collection=False):
        data = _object
        if not _object and not collection:
            cr = self.get_db_cr()
        elif _object and not is_json:
            cr = self.get_db_cr(_object)
            if type(data) == list:
                data_res = []
                for x in data:
                    data_res.append(x.dict(exclude_none=True) for x in data)
                data = data_res
            else:
                data = _object.dict(exclude_none=True)
        elif collection:
            cr = self.get_db_cr(collection=collection)
        else:
            cr = self.get_db_cr(_object)
            # data = data.dict()
        return cr, data

    def lkf_create(self, _object, is_json=False, collection=False):
        cr, data = self.get_cr_data(_object, is_json=is_json)
        if type(data) == dict:
            res = {}
            # data['_id'] = data.get('_id',data.get('id',None))
            data['_id'] = data.get('_id',data.get('id'))
            if data.get('_id') :
                res.update(self._edit_record(cr, data))
            else:
                res.update(self._insert_record(cr, data))
                    # dag_id = dag_obj.inserted_id
                # print('col', dag_id.values)
                # print('col', dd)
            res['obj'] = data
        elif type(data) == list:
            res = []
            edit_rec = []
            insert_rec = []
            for x in data:
                if x.get('_id') :
                    edit_rec.append(x)
                else:
                    insert_rec.append(x)
            if edit_rec:
                print(todo_update_many)
            if insert_rec:
                res += self._insert_record(cr, insert_rec)

        else:
            print(nada_nada)
        # print('cr', cr)
        # print('data', data)
        return res

    def lkf_update(self, query, data, replace=False):
        cr, cr_data = self.get_cr_data()
        if replace:
            data = data
        else:
            data = {"$set":data}

        res = cr.update_many(query, data)
        return res

    def lkf_search(self, **args):
        cols = _one = None
        cr, data = self.get_cr_data()
        if '_one' in list(args.keys()):
            _one = args.pop('_one')
        if '_columns' in list(args.keys()):
            cols = args.pop('_columns')
        if cols:
            res = cr.find(args, cols)
        else:
            res = cr.find(args)
        res = [ x for x in res]
        if _one:
            if res:
                return res[0]
        return res

    def lkf_delete(self, _object=None, query=False, is_json=False ):
        cr, data = self.get_cr_data(_object, is_json=False)
        if not query:
            query = {'_id':data['id']}
        #print('lkf delte', query)
        res = cr.delete_many(query)
        # print(stop)
        return res
