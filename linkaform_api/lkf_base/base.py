# -*- coding: utf-8 -*-
import sys, simplejson
from datetime import datetime, date
from bson import ObjectId

from ..lkf_object import LKFBaseObject

from linkaform_api import settings, network, utils, lkf_models


class LKF_Base(LKFBaseObject):

    def __init__(self, settings, sys_argv=None):
        config = settings.config
        self.lkf_base = {}
        self._set_connections(settings)
        self.current_record = {}
        settings = self.update_settings(settings)
        if sys_argv:
            self.argv = sys_argv
            self.data = simplejson.loads( sys_argv[2] )
            config['JWT_KEY'] = self.data["jwt"].split(' ')[1]
            config['USER_JWT_KEY'] = self.data["jwt"].split(' ')[1]
            settings.config.update(config)
            self.current_record = self.get_record(sys_argv)
            self._set_connections(settings)

    def _set_connections(self, settings):
        self.lkf_api = utils.Cache(settings)
        self.net = network.Network(settings)
        self.cr = self.net.get_collections()
        self.lkm = lkf_models.LKFModules(settings)
        return True

    def cache_drop(self, query):
        return self.delete(query=query)

    def cache_get(self, values, **kwargs):
        print('kwargs>>', kwargs)
        res = self.search(values)
        if res and res.get('_id'):
            if kwargs.get('keep_cache'):
                return res
            self.cache_drop({'_id':res['_id']})
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
        print('drop cache_update....')
        self.create({'test':1,'status':'drop'})

    def console_run(self):
        print(f"python { self.argv[0].split('/')[-1]} '{ self.argv[1]}' '{ self.argv[2]}'")

    def date_to_week(self, date_from):
        year_week = ""
        if date_from:
            week_from = datetime.strptime(date_from, '%Y-%m-%d')
            year_week = week_from.strftime('%Y%W')
        return year_week

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

    def get_record(self, sys_argv):
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

    def get_record_from_db(self, form_id, folio):
        query = {
            'form_id': form_id,
            'folio': folio,
            'deleted_at': {'$exists': False}
        }
        select_columns = {'folio':1,'user_id':1,'form_id':1,'answers':1,'_id':1,'connection_id':1,'created_at':1,'other_versions':1,'timezone':1}
        record_found = self.cr.find(query, select_columns)
        return record_found.next()

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

    def read_current_record_from_txt(self, file_url):
        name_downloded = self.download_pdf( file_url, is_txt=True )
        f = open( "/tmp/{}".format( name_downloded ) )
        return simplejson.loads( f.read() )

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