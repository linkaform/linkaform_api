# -*- coding: utf-8 -*-
import sys, simplejson

from linkaform_api import settings, network, utils, lkf_models


class LKF_Base():

    def __init__(self, settings, sys_argv=None):
        config = settings.config
        self.lkf_base = {}
        self._set_connections(settings)
        self.current_record = {}
        settings = self.update_settings(settings)
        if sys_argv:
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

    def download_pdf(self, file_url, is_txt=False):
        oc_name = 'oc_{}.pdf'.format(str(bson.ObjectId()))
        if is_txt:
            oc_name = 'file_{}.txt'.format(str(bson.ObjectId()))
        wget.download(file_url, '/tmp/{}'.format(oc_name))
        return oc_name

    def get_related_records(self, query):
        records = self.cr.aggregate(query)
        return [r for r in records ]

    def get_record(self, sys_argv):
        try:
            record_to_long = eval(sys_argv[3])
        except:
            record_to_long = False
        current_record = simplejson.loads(sys_argv[1])
        print('current_record=========', current_record)
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

    def read_current_record_from_txt(self, file_url):
        name_downloded = self.download_pdf( file_url, is_txt=True )
        f = open( "/tmp/{}".format( name_downloded ) )
        return simplejson.loads( f.read() )

