# -*- coding: utf-8 -*-
import sys, simplejson
from datetime import datetime, date
from bson import ObjectId

from ..lkf_object import LKFBaseObject

from linkaform_api import settings, network, utils, lkf_models


class LKF_Base(LKFBaseObject):

    def __init__(self, settings, sys_argv=None, use_api=False):
        config = settings.config
        self.lkf_base = {}
        self._set_connections(settings)
        self.current_record = {}
        self.close_status = 'close'
        self.open_status = 'open'
        self.open_status = 'new'
        self.status_id = '0000000000000000000aaaaa'
        settings = self.update_settings(settings)
        if sys_argv:
            self.argv = sys_argv
            self.data = simplejson.loads( sys_argv[2] )
            if not use_api:
                config['JWT_KEY'] = self.data["jwt"].split(' ')[1]
                config['USER_JWT_KEY'] = self.data["jwt"].split(' ')[1]
                settings.config.update(config)
            self.current_record = self.get_current_record(sys_argv)
            self._set_connections(settings)

    def _set_connections(self, settings):
        self.lkf_api = utils.Cache(settings)
        self.net = network.Network(settings)
        self.cr = self.net.get_collections()
        self.lkm = lkf_models.LKFModules(settings)
        return True

    def do_records_close(self, form, folio, status_id=None):
        res = self.is_record_close(form, folio)
        if not res:
            res = self.record_close(form, folio, 
                        status_id= self.get_key_id(status_id),
                        value=self.get_value() 
                        )
        return res

    def do_records_open(self, form, folio,status_id=None):
        return self.set_record(form, folio, 
                    status_id=self.get_key_id(), 
                    value=self.get_value() 
                )

    def cache_drop(self, query):
        return self.delete(query=query)

    def cache_get(self, values, **kwargs):
        res = self.cache_read(values, **kwargs)
        if res and res.get('_id'):
            if kwargs.get('keep_cache'):
                return res
            self.cache_drop({'_id':res['_id']})
        return res

    def cache_read(self, values, **kwargs):
        res = self.search(values)
        return res

    def cache_set(self, values):
        if values.get('_id'):
            t_id = values.pop('_id')
            res = self.search({'_id':t_id, '_one':True}).get('cache',{})
            res.update(values)
            values = res
        else:
            t_id = ObjectId()
        return self.create({'_id':t_id, 'cache':values})

    def cache_update(self, values):
        self.create({'test':1,'status':'drop'})

    def console_run(self):
        print(f"python { self.argv[0].split('/')[-1]} '{ self.argv[1]}' '{ self.argv[2]}'")

    def date_from_str(self, value):
        def get_value(value, date_format):
            try:
                return datetime.strptime(value, date_format)
            except:
                raise('Not a valid date')
        if len(value) == 10:
            #Date
            value = get_value(value, '%Y-%m-%d')
        elif len(value) == 19 or len(value) == 18:
            value = get_value(value, '%Y-%m-%d %H:%M:%S')
        elif len(value) == 16:
            value = get_value(value, '%Y-%m-%d %H:%M')
        elif len(value) == 8:
            value = get_value(value, '%Y-%m-%d %H:%M')
        else:
            raise('Not a valid length of a date')
        return value

    def date_to_week(self, date_from):
        year_week = ""
        if date_from:
            week_from = datetime.strptime(date_from, '%Y-%m-%d')
            year_week = week_from.strftime('%Y%W')
        return year_week

    def date_2_epoch(self, date_str):
        date_obj = self.date_from_str(date_str)
        return date_obj.timestamp()

    def date_operation(self, date_value, operator, qty, unit, date_format=None):
        if type(date_value) == str:
            epoch = self.date_2_epoch(date_value)
        else:
            epoch = date_obj.timestamp()
        if unit in ('second', 'seconds'):
            seconds = qty 
        if unit in ('minutes', 'minutes'):
            seconds = qty * 60
        if unit in ('hour', 'hours'):
            seconds = qty * 60 * 60
        if unit in ('day', 'days'):
            seconds = qty * 60 * 60 * 24
        if unit in ('week', 'weeks'):
            seconds = qty * 60 * 60 * 24 + 7
        if operator == '+' or operator == 'add':
            epoch += seconds
        if operator == '-' or operator == 'subtract':
            epoch -= seconds
        if date_format:
            return datetime.fromtimestamp(epoch).strftime(date_format)
        else:
            return datetime.fromtimestamp(epoch)

    def download_pdf(self, file_url, is_txt=False):
        oc_name = 'oc_{}.pdf'.format(str(bson.ObjectId()))
        if is_txt:
            oc_name = 'file_{}.txt'.format(str(bson.ObjectId()))
        wget.download(file_url, '/tmp/{}'.format(oc_name))
        return oc_name

    def download_file(self, file_url, is_txt=False):
        file_name = 'file_{}.pdf'.format(str(bson.ObjectId()))
        if is_txt:
            file_name = 'file_{}.txt'.format(str(bson.ObjectId()))
        wget.download(file_url, '/tmp/{}'.format(file_name))
        return file_name

    def get_answer_value(self, key_id=None, value=None):
        if not key_id:
            key_id = self.get_key_id()
        if not value:
            value = self.get_value()
        if key_id.find('.'):
            #TODO hacer busqeuda dentro de grupos
            key=key_id
        return {f'answers.{self.get_key_id(key)}':self.get_value(value)}

    def get_date_str(self, value):
        if value:
            if isinstance(value, datetime):
                return value.strftime('%Y-%m-%d')
            elif isinstance(value, date):
                return value.strftime('%Y-%m-%d')
            return str(value)
        else:
            return value

    def get_related_records(self, query):
        records = self.cr.aggregate(query)
        return [r for r in records ]

    def get_current_record(self, sys_argv):
        try:
            record_to_long = eval(sys_argv[3])
        except:
            record_to_long = False
        current_record = simplejson.loads(sys_argv[1])
        if not current_record.get('answers') and current_record.get('answers_url'):
            current_record = self.read_current_record_from_txt( current_record['answers_url'] )
        if record_to_long:
            current_record = self.get_record_from_db( current_record.get('folio'), current_record.get('folio') )
        return current_record

    def get_key_id(self, key_id=None):
        if not key_id:
            key_id = self.status_id
        return key_id

    def get_records(self, form_id=None, folio=None, query_answers={}, select_columns=[]):
        if select_columns:
            select_columns = {key:1 for key in select_columns}
        else:
            select_columns = {'folio':1,'user_id':1,'form_id':1,'answers':1,'_id':1,'connection_id':1,'created_at':1,'other_versions':1,'timezone':1}
        match_query = {'deleted_at': {'$exists': False}}
    
        if form_id:
            match_query.update(self.get_query_by('form_id', form_id))
        if folio:
            match_query.update(self.get_query_by('folio', folio))
        if query_answers:
            match_query.update(query_answers)
        return self.cr.find(match_query, select_columns)

    def get_record_from_db(self, form_id=None, folio=None, query_answers={}, select_columns=[]):
        if select_columns:
            select_columns = {key:1 for key in select_columns}
        else:
            select_columns = {'folio':1,'user_id':1,'form_id':1,'answers':1,'_id':1,'connection_id':1,'created_at':1,'other_versions':1,'timezone':1}
        match_query = {'deleted_at': {'$exists': False}}
    
        if form_id:
            match_query.update(self.get_query_by('form_id', form_id))
        if folio:
            match_query.update(self.get_query_by('folio', folio))
        if query_answers:
            match_query.update(query_answers)

        record_found = self.cr.find(match_query, select_columns)
        return record_found.next()

    def get_record_by_id(self, _id):
        query = {
            '_id': ObjectId(_id),
            'deleted_at': {'$exists': False}
        }
        select_columns = {'folio':1,'user_id':1,'form_id':1,'answers':1,'_id':1,'connection_id':1,'created_at':1,'other_versions':1,'timezone':1}
        record_found = self.cr.find(query, select_columns)
        try:
            return record_found.next()
        except:
            return {}

    def get_record_verion_by_id(self, _id):
        version_cr = self.net.get_collections('answer_version')
        if not _id:
            return []
        query = {
            '_id': ObjectId(_id),
            'deleted_at': {'$exists': False}
        }
        select_columns = {'folio':1,'user_id':1,'form_id':1,'answers':1,'_id':1,'connection_id':1,'created_at':1,'other_versions':1,'timezone':1}
        record_found = version_cr.find(query)
        return record_found.next()

    def get_record_last_version(self, record):
        latest_versions = record.get('other_versions',[])
        if latest_versions:
            latest_versions = latest_versions[-1]
            version_id_path = latest_versions.get('uri','').strip('/')
            version_id = version_id_path.split('/')[-1]
            return self.get_record_verion_by_id(version_id)
        else:
            return {}

    def get_query_by(self, key, value):
        update = {key: value}
        if type(value) == list:
            update = {key: {'$in': value}}
        return update

    def get_value(self, get_value=None):
        if not get_value:
            get_value = self.close_status
        return get_value

    def get_date_query(self, date_from=None, date_to=None, date_field=None, date_field_id=None, field_type=None):
        res = {}
        if not date_field:
            date_field = 'created_at'
        if date_field_id:
            date_field = 'answers.{}'.format(date_field_id)

            if field_type == 'int':
                date_from = int(date_from)
                date_to = int(date_to)
            else:
                date_from = self.get_date_str(date_from)
                date_to = self.get_date_str(date_to)
        if date_from and date_to:
            res.update({
            date_field: {
            '$gte':date_from,
            '$lte':date_to,
            }
            })
        elif date_from and not date_to:
            res.update({
            date_field: {
            '$gte':date_from
            }
            })

        elif not date_from and date_to:
            res.update({
            date_field: {
            '$lte':date_to
            }
            })
        return res

    def is_record_close(self, form, folio, status_id=None ):
        match_query = {'deleted_at': {'$exists': False}}
        match_query.update(self.get_query_by('form_id', form))
        match_query.update(self.get_query_by('folio', folio))
        match_query.update(self.get_query_by(f'answers.{self.get_key_id()}',self.get_value()))
        res = self.cr.find_one(match_query)
        if res:
            return res
        else:
            return False

    def read_current_record_from_txt(self, file_url):
        name_downloded = self.download_pdf( file_url, is_txt=True )
        f = open( "/tmp/{}".format( name_downloded ) )
        return simplejson.loads( f.read() )

    def record_close(self, form, folio, status_id=None, value=None ):
        if not status_id:
            status_id = self.get_key_id()
        if value: 
            value = {'$set':self.get_answer_value(value)}
        else:
            value = {'$set':self.get_answer_value(status_id)}
        return self.set_record(form, folio, status_id=status_id, value=value )

    def set_record(self, form, folio, status_id=None, value=None ):
        match_query = {'deleted_at': {'$exists': False}}
        match_query.update(self.get_query_by('form_id', form))
        match_query.update(self.get_query_by('folio', folio))
        update_db = self.cr.update_many(match_query, value)
        return update_db.raw_result

    def update_settings(self, settings):
        lkf_api = utils.Cache(settings)
        APIKEY = settings.config.get('APIKEY', settings.config.get('API_KEY', ))
        user = lkf_api.get_jwt(api_key=APIKEY, get_user=True)
        settings.config["JWT_KEY"] = user.get('jwt')
        settings.config["APIKEY_JWT_KEY"] = user.get('jwt')
        account_id = user['user']['parent_info']['id']
        settings.config["USER_ID"] = user['user']['id']
        settings.config["ACCOUNT_ID"] = account_id
        settings.config["USER"] = user['user']
        settings.config["MONGODB_USER"] = 'account_{}'.format(account_id)
        return settings

    def unlist(self, arg):
        if type(arg) == list and len(arg) > 0:
            return unlist(arg[0])
        return arg

    def valid_date(self, value):
        if len(value) == 10:
            #Date
            try:
                value = datetime.strptime(value, '%Y-%m-%d')
            except:
                raise('Not a valid date')
        elif len(value) == 19:
            #DateTime
            try:
                value = datetime.strptime(value, '%Y-%m-%d %H:%M%S')
            except:
                raise('Not a valid date')

        elif len(value) == 8:
            #Time
            try:
                value = datetime.strptime(value, '%Y-%m-%d %H:%M%S')
            except:
                raise('Not a valid date')
        else:
            raise('Not a valid length of a date')
        return value


#####

class LKF_Report(LKF_Base):


    def __init__(self, settings, sys_argv=None, use_api=False):
        print('INIT LKF_Report....')
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        self.json = {
            # "firstElement":{
            #     "data": [],
            # },
            # "secondElement":{
            #     "data": [],
            # },
            # "firstFilter":[],
            # "secondFilter":[]
        } 

    def report_print(self):
        res = {'json':{}}
        for x in self.json:
            res['json'][x] = self.json[x]
        return res

