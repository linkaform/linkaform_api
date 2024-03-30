# -*- coding: utf-8 -*-
import sys, simplejson, arrow
from datetime import datetime, date
from bson import ObjectId
import importlib
from datetime import datetime
from pytz import timezone

from ..lkf_object import LKFBaseObject

from linkaform_api import settings, network, utils, lkf_models


class LKF_Base(LKFBaseObject):

    def __init__(self, settings, sys_argv=None, use_api=False):
        config = settings.config
        self.lkf_base = {}
        self._set_connections(settings)
        self.current_record =  simplejson.loads( sys_argv[1] )
        self.open_status = 'open'
        self.close_status = 'close'
        self.open_status = 'new'
        self.status_id = '0000000000000000000aaaaa'
        self.settings = self.update_settings(settings, use_api=use_api)
        self.f = {}
        if sys_argv:
            self.argv = sys_argv
            self.data = simplejson.loads( sys_argv[2] )
            if not use_api:
                config['JWT_KEY'] = self.data.get("jwt",'').split(' ')[1]
                config['USER_JWT_KEY'] = self.data.get("jwt",'').split(' ')[1]
                settings.config.update(config)
            self.answers = self.current_record.get('answers',{})
            self.current_record = self.get_current_record(sys_argv)
            self.folio = self.current_record.get('folio',{})
            self.form_id = self.current_record.get('form_id',{})
            self.record_user_id = self.current_record.get('user_id')
            if self.current_record.get('_id'):
                if type(self.current_record['_id']) == dict:
                    self.record_id = self.current_record['_id'].get('$oid') \
                        if self.current_record['_id'].get('$oid') else self.current_record['_id']
                else:
                    self.record_id = self.current_record['_id']
            else:
                self.record_id = None
                self.record_id = None
            self._set_connections(settings)

    # def _do_inherits(self):
    #     print('========================= inherit')
    #     opt = dir(self)
    #     if '_inherit' in opt:
    #         print('inherit3333', self._inherit)
    #         inherits = self._inherit.split(',')
    #         print('inherits22', inherits)
    #         for module in inherits:
    #             print('ya module',module)
    #             forms = importlib.import_module(f'lkf_addons.addons.{module}.{module}_utils')
    #             class_ = getattr(forms, 'Employee')
    #             print('fir', dir(class_))
    #             print('ya class_=====================>>>>',class_)
    #             print('ya forms=====================>>>>',self.settings)
    #             print('ya forms',forms.Employee(self.settings))
    #             print('ya forms=====================>>>>',self)
    #             return forms.Employee(self.settings)
    #     return self

    def _set_connections(self, settings):
        self.lkf_api = utils.Cache(settings)
        self.net = network.Network(settings)
        self.cr = self.net.get_collections()
        self.lkm = lkf_models.LKFModules(settings)
        return True

    def do_records_close(self, form, folio, status_id=None):
        res = self.is_record_close(form, folio, status_id=status_id)
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

    def cache_set(self, values, **kwargs):
        if values.get('_id'):
            t_id = values.pop('_id')
            res = self.search({'_id':t_id, '_one':True}).get('cache',{})
            res.update(values)
            values = res
        else:
            t_id = ObjectId()
        return self.create({'_id':t_id, 'cache':values, 'kwargs':kwargs})

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

    def get_record_form_fields(self, form_id=None):
        if not form_id:
            form_id = self.form_id
        fields_inventory_flow = self.lkf_api.get_form_id_fields( form_id )
        if not fields_inventory_flow:
            return {}
        else:
            fields = fields_inventory_flow[0]['fields']

            # Obtengo solo los índices que necesito de cada campo
            info_fields = [{k:n[k] for k in ('label','field_type','field_id','groups_fields','group','options','catalog_fields','catalog') if k in n} for n in fields]

            fields_to_new_record = {}
            for field in info_fields:
                if field['field_type'] == 'catalog':
                    fields_to_new_record[ field['field_id'] ] = field['field_type']
                if not field.get('catalog'):
                    fields_to_new_record[ field['field_id'] ] = field['field_type']
            #print('fields_to_new_record = ',fields_to_new_record)
        return fields_to_new_record

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
            current_record = self.get_record_from_db( current_record.get('form_id'), current_record.get('folio') )
        return current_record

    def get_key_id(self, key_id=None):
        if not key_id:
            key_id = self.status_id
        return key_id

    def get_query_by(self, key, value):
        update = {key: value}
        if type(value) == list:
            update = {key: {'$in': value}}
        return update

    def get_records(self, form_id=None, folio=None, query_answers={}, select_columns=[]):
        select_columns = self.get_selected_columns(select_columns)
        match_query = {'deleted_at': {'$exists': False}}
    
        if form_id:
            match_query.update(self.get_query_by('form_id', form_id))
        if folio:
            match_query.update(self.get_query_by('folio', folio))
        if query_answers:
            match_query.update(query_answers)
        return self.cr.find(match_query, select_columns)

    def get_record_from_db(self, form_id=None, folio=None, query_answers={}, select_columns=[]):
        select_columns = self.get_selected_columns(select_columns)
        match_query = {'deleted_at': {'$exists': False}}
    
        if form_id:
            match_query.update(self.get_query_by('form_id', form_id))
        if folio:
            match_query.update(self.get_query_by('folio', folio))
        if query_answers:
            match_query.update(query_answers)

        record_found = self.cr.find(match_query, select_columns)
        try:
            return record_found.next()
        except:
            return {}

    def get_record_by_folio(self, folio, form_id, select_columns=[]):
        select_columns = self.get_selected_columns(select_columns)
        query = {
            'folio': folio,
            'deleted_at': {'$exists': False}
        }
        if form_id:
            query.update({'form_id':form_id})
        print('query', query)
        print('query', self.cr)
        record_found = self.cr.find(query, select_columns)
        try:
            return record_found.next()
        except:
            return {}

    def get_record_by_id(self, _id,  select_columns=[]):
        select_columns = self.get_selected_columns(select_columns)
        query = {
            '_id': ObjectId(_id),
            'deleted_at': {'$exists': False}
        }
        record_found = self.cr.find(query, select_columns)
        try:
            return record_found.next()
        except:
            return {}

    def get_record_verion_by_id(self, _id, select_columns=[]):
        select_columns = self.get_selected_columns(select_columns)
        version_cr = self.net.get_collections('answer_version')
        if not _id:
            return []
        query = {
            '_id': ObjectId(_id),
            'deleted_at': {'$exists': False}
        }
        record_found = version_cr.find(query)
        try:
            return record_found.next()
        except:
            return {}

    def get_record_last_version(self, record):
        latest_versions = record.get('other_versions',[])
        if latest_versions:
            latest_versions = latest_versions[-1]
            version_id_path = latest_versions.get('uri','').strip('/')
            version_id = version_id_path.split('/')[-1]
            return self.get_record_verion_by_id(version_id)
        else:
            return {}

    def get_selected_columns(self, select_columns):
        if select_columns:
            select_columns = {key:1 for key in select_columns}
        else:
            select_columns = {'folio':1,'user_id':1,'form_id':1,'answers':1,'_id':1,'connection_id':1,'created_at':1,'other_versions':1,'timezone':1}
        return select_columns

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
        match_query.update(self.get_query_by(f'answers.{self.get_key_id(key_id=status_id)}',self.get_value()))
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
            value = {'$set':self.get_answer_value(key_id=status_id, value=value)}
        else:
            value = {'$set':self.get_answer_value(key_id=status_id)}
        return self.set_record(form, folio, status_id=status_id, value=value )

    def set_record(self, form, folio, status_id=None, value=None ):
        match_query = {'deleted_at': {'$exists': False}}
        match_query.update(self.get_query_by('form_id', form))
        match_query.update(self.get_query_by('folio', folio))
        update_db = self.cr.update_many(match_query, value)
        return update_db.raw_result

    def search_4_key(self, data, search_key):
        if data.get(search_key):
            return data[search_key]
        res = None
        for key, value in data.items():
            if type(data[key]) == dict:
               res = self.search_4_key(data[key], search_key)
            if type(data[key]) == list:
               for x in data[key]:
                  if type(x) == dict:
                     res = self.search_4_key(x, search_key)
            if key == search_key:
               return value
            if res:
                break
        return res

    def update_settings(self, settings, use_api=False):
        lkf_api = utils.Cache(settings)
        APIKEY = settings.config.get('APIKEY', settings.config.get('API_KEY', ))
        user = lkf_api.get_jwt(api_key=APIKEY, get_user=True)
        if use_api:
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
            return self.unlist(arg[0])
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

    def get_today_format(self):
        today = datetime.now()
        today = today.astimezone(timezone('America/Monterrey'))
        str_today = datetime.strftime(today, '%Y-%m-%d')
        today = datetime.strptime( '{} 00:00:00'.format( str_today ), '%Y-%m-%d %H:%M:%S')
        return today
#####

class LKF_Report(LKF_Base):


    def __init__(self, settings, sys_argv=None, use_api=False):
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

    def get_period_dates(self, period):
        now = arrow.utcnow()
        start_date = None
        end_date = None
        if period == 'today':
            start_date = now.floor('day')
            end_date = now.shift(days=+1).floor('day')
        elif period == 'yesterday':
            now = now.shift(days=-1)
            start_date = now.floor('day')
            end_date = now.shift(days=+1).floor('day')
        elif period == 'this_week':
            start_date = now.floor('week')
            end_date = now.ceil('week').shift(days=+1).floor('day')
        elif period == 'last_week':
            start_date = now.shift(weeks=-1)
            start_date = start_date.floor('week')
            end_date = start_date.ceil('week').shift(days=+1).floor('day')
        elif period == 'last_fifteen_days':
            start_date = now.shift(weeks=-2)
            start_date = start_date.floor('day')
            end_date = now.shift(days=+1).floor('day')
        elif period == 'this_month':
            start_date = now.floor('month')
            end_date = now.ceil('month').shift(days=+1).floor('day')
        elif period == 'last_month':
            start_date = now.floor('month')
            end_date = start_date.shift(days=-1)
            start_date = end_date.floor('month').shift(days=+1).floor('day')
        elif period == 'this_year':
            start_date = now.replace(day=1, month=1, year=now.year).floor('day')
            end_date = now.shift(days=+1).floor('day')
        elif period == 'last_year':
            start_date = now.replace(day=1, month=1, year=now.year-1).floor('day')
            end_date = now.replace(day=31, month=12, year=now.year-1).ceil('day').shift(days=+1).floor('day')

        return start_date, end_date