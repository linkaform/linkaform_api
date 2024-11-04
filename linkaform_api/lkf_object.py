# coding: utf-8
#!/usr/bin/python

#python libs
from bson import ObjectId
from hashlib import sha1, md5
import subprocess, jwt, simplejson, sys

# from pymongo import MongoClient

# from . import settings 
from .models.base_models import UserData
from .mongo_util import connect_mongodb

# from  import UserData
#Flask Models
# from flask_pymongo import PyMongo

##### LKF Object

class LKFBase:


    def search_modules(self, path):
        #cmd = ['ls', '-d', '/srv/scripts/addons/modules/*/']
        cmd = ['ls', '-d', '{}/*/'.format(path)]
        cmd = ['find', path , '-maxdepth', '1', '-type', 'd']
        process = subprocess.Popen(args=cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        output, error = process.communicate()
        res = []
        output = output.split(b'\n')
        for x in output:
            x = x.decode('utf-8')
            x = x.replace(path,'').strip('/')
            if x.find('.') == 0 or x.find('_') ==0:
                continue
            if x:
                res.append(x)
        return res


class LKFBaseObject(LKFBase):
    

    def __init__(self, *, id: str, created_by: UserData, settings: dict,  object: str = None ):
        self.id = id
        self.created_by = created_by
        self.object = object
        self.cr_con = {}
        self.settings = settings
        self.config = settings.config

    def LKFException(self, msg, dict_error={}):
        title_default = "Something needs to be checked!!!"
        type_default  = "warning"
        icon_default = "fa-circle-exclamation"
        msg_dict = {}

        if '"msg":' in msg:
            raise Exception(msg)

        if isinstance(msg, str):
            msg = {'msg':msg}

        msg_dict['title'] = msg.get('title', title_default)
        msg_dict['msg'] = msg.get('msg', "Something went wrong")
        msg_dict['icon'] = msg.get('icon', icon_default)
        msg_dict['type'] = msg.get('type', type_default)

        error_format = {
            "status":400,
            "msg":msg_dict
        }

        if dict_error:
            error_format.update(dict_error)

        raise Exception(simplejson.dumps(error_format))

    def HttpResponse(self, data, indent=False, **kwargs):
        if kwargs.get('test'):
            return True
        if indent:
            sys.stdout.write(simplejson.dumps(data, indent=indent))
        else:
            sys.stdout.write(simplejson.dumps(data))

    # resource_id: Optional[int]
    # username: Optional[str]
    # email: Optional[str]
    # group_id: Optional[int]
    # resource_kind: Optional[str]
    # user_type: Optional[list] #Literal['follower', 'onwer', 'supervisor', 'admin']]
    # phone: Optional[List[UserPhone]]
    # properties: Optional[dict]
    # user_icon: Optional[AnyUrl]
    # user_url: Optional[AnyUrl]
    # user_tag: Optional[List[str]]
    # timezone: Optional[str]

    def decode_jwt(self):
        token = self.settings.config['JWT_KEY']
        import sys
        version = sys.version
        privKeyFile = open('/etc/ssl/certs/lkf_jwt_key.pub','r')
        pub_key = privKeyFile.read()
        jwt_data = jwt.decode(token, pub_key, algorithms='RS256')
        return jwt_data

    def get_user_data(self):
        u = self.config.get('USER')
        user = {
            'email': u.get('user',{}).get('email'),
            'username': u.get('user',{}).get('username'),
            'account_id': u.get('user',{}).get('parent_info',{}).get('id'),
            'name': u.get('user',{}).get('first_name',{}),
            'user_id': u.get('user',{}).get('id')
            }
        return user

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
        self.config['MONGODB_HOST'],
        dbname,
        )
        return uri

    def __conect_db(self):
        if hasattr(self, 'config'):
            config = self.config
        elif hasattr(self, 'settings'):
            config = self.settings.config
        account_id = config.get('ACCOUNT_ID', config.get('USER',{}).get('user',{}).get('parent_info',{}).get('id'))
        dbname = 'infosync_answers_client_{}'.format(account_id)
        self.settings.config['MONGO_CR'] = self.settings.config.get('MONGO_CR', {})
        if not self.settings.config['MONGO_CR'].get(dbname):
            self.settings.config['MONGO_URI'] = self.get_mongo_uri(account_id)

            # mongo = MongoClient(self.config)
            mongo = connect_mongodb(dbname, uri=self.config['MONGO_URI'])
            self.settings.config['MONGO_CR'][dbname] = mongo
        return self.settings.config['MONGO_CR'][dbname]

    def get_db_cr(self, _object=None, db_name=False, collection=False):
        if self.name:
            collection = self.name
        else:
            collection = _object.__class__.__name__
        # mongo = PyMongo(settings)
        mongo =  self.__conect_db()
        conn = eval('mongo.{}'.format(collection))
            #conn = self.lkf_obj
        #TODO Create database indexes
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
            elif type(data) == dict:
                data = _object
            else:
                data = _object.dict(exclude_none=True)
        elif collection:
            cr = self.get_db_cr(collection=collection)
        else:
            cr = self.get_db_cr(_object)
            # data = data.dict()
        return cr, data

    def create(self, _object, is_json=True, collection=False):
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

    def update(self, query, data, upsert=True):
        cr, cr_data = self.get_cr_data()
        data = {"$set":data}
        res = cr.update_many(query, data, upsert=upsert)
        return res

    def search(self, query):
        cols = _one = None
        cr, data = self.get_cr_data()
        if '_one' in list(query.keys()):
            _one = query.pop('_one')
        if '_columns' in list(query.keys()):
            cols = query.pop('_columns')
        if cols:
            res = cr.find(query, cols)
        else:
            res = cr.find(query)
        res = [ x for x in res]
        if _one:
            if res:
                return res[0]
            else:
                return {}
        return res

    def serach_module_item(self, item_info):
        res = self.search(item_info)
        if res and type(res) == list and len(res) > 0:
            return res[0]
        return False

    def delete(self, _object=None, query=False, is_json=False ):
        cr, data = self.get_cr_data(_object, is_json=False)
        if not query:
            query = {'_id':data['id']}
        #print('lkf delte', query)
        res = cr.delete_many(query)
        # print(stop)
        return res
