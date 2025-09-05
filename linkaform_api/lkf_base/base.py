# -*- coding: utf-8 -*-
import sys, simplejson, arrow, time, pyexcel, wget
from datetime import datetime, date
from bson import ObjectId
import importlib
from datetime import datetime
from pytz import timezone

from ..lkf_object import LKFBaseObject

from linkaform_api import settings, network, utils, lkf_models, upload_file


class LKF_Base(LKFBaseObject):

    def __init__(self, settings, sys_argv=None, use_api=False, **kwargs):
        # print('--------------------LKF_Base----------------------------', LKF_Base.__mro__)
        self.config = settings.config
        self.account_id = self.config.get('ACCOUNT_ID')
        self.master = True
        self.sys_argv = sys_argv
        self.use_api = use_api
        self.lkf_base = {}
        self.open_status = 'open'
        self.close_status = 'close'
        self.open_status = 'new'
        self.status_id = '0000000000000000000aaaaa'
        # print('settings', dir(settings.lkf_api))
        self.settings = settings
        self.settings = self.update_settings(settings, use_api=use_api)
        self.f = kwargs.get('f', {})
        self.GET_CONFIG = {}
        self.kwargs = kwargs
        self.kwargs['MODULES'] = self.kwargs.get('MODULES',[])
        print('=================')
        if sys_argv:
            self.current_record =  simplejson.loads( sys_argv[1] )
            self.argv = sys_argv
            self.data = simplejson.loads( sys_argv[2] )
            if not use_api:
                try:
                    self.config['JWT_KEY'] = self.data.get("jwt",'').split(' ')[1] if self.data.get("jwt",'') else None
                    self.config['USER_JWT_KEY'] = self.data.get("jwt",'').split(' ')[1] if self.data.get("jwt",'') else None
                except Exception as e:
                    self.LKFException("Error al obtener autentificacion, favor de validar tu JWT", e)
                self.settings.config.update(self.config)
            if self.config.get('JWT_KEY'):
                self.user = self.decode_jwt()
            self.current_record = self.get_current_record(sys_argv)
            self.folio = self.current_record.get('folio',{})
            self.form_id = self.current_record.get('form_id',{})
            self.record_user_id = self.current_record.get('user_id')
            if self.current_record.get('_id') or self.current_record.get('record_id'):
                if self.current_record.get('record_id'):
                    self.record_id = self.current_record['record_id']
                elif type(self.current_record['_id']) == dict:
                    self.record_id = self.current_record['_id'].get('$oid') \
                        if self.current_record['_id'].get('$oid') else self.current_record['_id']
                else:
                    self.record_id = self.current_record['_id']
            else:
                self.record_id = None
            if not self.record_id:
                conneciont_id = self.current_record.get('connection_record_id')
                if type(conneciont_id) == dict:
                    conneciont_id = conneciont_id.get('$oid')
                self.record_id = conneciont_id
            # self._set_connections(settings)
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

        self.upfile = upload_file.LoadFile(settings, **{'Cache':self})
        #self.lkf_api = self.upfile.lkf_api
        # TODO USAR el lkf_api que esta en LoadFile para evitar buqule
        self.lkf_api = utils.Cache(settings)
        if hasattr(self.lkf_api, 'network'):
            self.net = self.lkf_api.network
        else:
            self.net = network.Network(settings)
        self.cr = self.net.get_collections()
        self.cr_wkf = self.net.get_collections('workflow_log')
        self.cr_version = self.net.get_collections('answer_version')
        self.lkm = lkf_models.LKFModules(settings, lkf_api=self.lkf_api)
        return True

    def _labels_list(self, data=[], ids_label_dct={}, from_self=False):
        res = []
        for d in data:
            if type(d) == list:
                res.append(self._labels_list(d, ids_label_dct=ids_label_dct, from_self=True))
            else:
                res.append(self._labels(d, ids_label_dct=ids_label_dct, from_self=True))
        return res

    def _labels(self, data={}, ids_label_dct={}, from_self=False):
        if not ids_label_dct:
            ids_label_dct = self.f
        if not data and not from_self:
            data = {}
            if hasattr(self, 'answers'):
                data = self.answers
        _f = {v:k for k, v in ids_label_dct.items()}
        res = {}
        if type(data) in (str, int, float):
            return data
        for key, value in data.items():
            label = _f.get(key,key)
            if type(value) == dict:
                res.update(self._labels(data=value, ids_label_dct=ids_label_dct, from_self=True))
            elif type(value) == list:
                list_res = []
                for l in value:
                    if type(l) == list:
                        list_res.append(self._labels_list(data=l, ids_label_dct=ids_label_dct, from_self=True))
                    else:
                        if l:
                            list_res.append(self._labels(data=l, ids_label_dct=ids_label_dct, from_self=True))
                res.update({label:list_res})
            else:
                res[label] = value
        return res

    def _lables_to_ids(self, data={}):
        if not data:
            data=self.answers
        res = {}
        if type(data) in (str, int, float):
            return data
        for key, value in data.items():
            label = self.f.get(key,key)
            if type(value) == dict:
                res.update(self._labels(data=value))
            elif type(value) == list:
                list_res = []
                for l in value:
                    if isinstance(l, list):
                        list_res = l
                    else:
                        list_res.append(self._lables_to_ids(l))
                res.update({label:list_res})
            else:
                res[label] = value
        return res

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
        if isinstance(res, list) and len(res) > 0:
            if kwargs.get('keep_cache'):
                return res
            self.cache_drop(values)
            return res
        if res and res.get('_id'):
            if kwargs.get('keep_cache'):
                return res
            self.cache_drop({'_id':res['_id']})
        return res

    def cache_read(self, values, **kwargs):
        if 'keep_cache' in list(kwargs.keys()):
            #muy raro porque el kwargs.get('keep_cache') no detectaba la llave
            kwargs.pop('keep_cache')
        if kwargs.keys():
            values.update(kwargs)
        res = self.search(values)
        return res

    def cache_set(self, values, **kwargs):
        created_at = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
        if values.get('_id'):
            t_id = values.pop('_id')
            res = self.search({'_id':t_id, '_one':True}).get('cache',{})
            res.update(values)
            values = res
        else:
            t_id = ObjectId()
        return self.create({
            '_id':t_id, 
            'timestamp':int(time.time()), 
            'created_at': created_at, 
            'cache':values, 
            'kwargs':kwargs})

    def cache_update(self, values):
        self.create({'test':1,'status':'drop'})

    def check_keys_and_missing(self, key_list, dictionary):
        """
        Verifica si todos los elementos de key_list existen como claves en dictionary
        y devuelve los elementos que faltan.

        :param key_list: Lista de strings a verificar.
        :param dictionary: Diccionario en el cual se realizará la verificación.
        :return: Una lista que contiene los elementos faltantes.
        """
        missing_keys = [key for key in key_list if key not in dictionary]
        return missing_keys

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
        if not date_str:
            return None
        date_obj = self.date_from_str(date_str)
        return date_obj.timestamp()

    def date_2_str(self, value):
        res=None
        try:
            res = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                res = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                res = datetime.strptime(value, '%Y-%m-%d')
        return res
        
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
        oc_name = 'oc_{}.pdf'.format(str(ObjectId()))
        if is_txt:
            oc_name = 'file_{}.txt'.format(str(ObjectId()))
        wget.download(file_url, '/tmp/{}'.format(oc_name))
        return oc_name

    def download_file(self, file_url, is_txt=False):
        file_name = 'file_{}.pdf'.format(str(ObjectId()))
        if is_txt:
            file_name = 'file_{}.txt'.format(str(ObjectId()))
        wget.download(file_url, '/tmp/{}'.format(file_name))
        return file_name

    def format_cr(self, cr_result, get_one=False, labels={}, **kwargs):
        res = []
        for x in cr_result:
            if x.get('_id'):
                if type(x['_id']) == dict:
                    x.update({k:v for k,v in x.pop('_id').items()})
                else:
                    x['_id'] = str(x.get('_id',""))
            if x.get('created_at'):
                x['created_at'] = self.get_date_str(x['created_at'])
            if x.get('updated_at'):
                x['updated_at'] = self.get_date_str(x['updated_at'])
            if kwargs.get('labels_off') and kwargs['labels_off']:
                # Se hizo asi para garantizar compatiblidad con proces
                # Que manden llamar funcion.
                res.append(x)
            else:
                res.append(self._labels(x))
        if get_one and res:
            res = res[0]
        elif get_one and not res:
            res = {}
        return res

    def format_cr_result(self, cr_result, get_one=False):
        return self.format_cr(cr_result, get_one=get_one)

    def format_select(self, value):
        if value:
            value = value.replace('_', ' ')
            value = value.title()
        return value

    def get_answer(self, key):
        """
        Return the value of a given objectId with recursive search.
        Ex. get_answer('664f81a23e59756b3c62ff5a.663bd36eb19b7fb7d9e97ccb')
        """
        keys = key.split('.')
        d = self.answers
        for k in keys:
            d = d.get(k)
            if d is None:
                return None
        return d

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

    def get_current_record(self, sys_argv):
        try:
            record_to_long = eval(sys_argv[3])
        except:
            record_to_long = False
        current_record = simplejson.loads(sys_argv[1])
        self.answers = current_record.get('answers',{})
        if not current_record.get('answers') and current_record.get('answers_url'):
            current_record = self.read_current_record_from_txt( current_record['answers_url'] )
            self.answers = current_record.get('answers',{})
        elif record_to_long:
            current_record = self.get_record_from_db( current_record.get('form_id'), current_record.get('folio') )
            self.answers = current_record.get('answers',{})
        return current_record

    def get_prev_version(self, versions, select_columns=[]):
        last_version = versions[-1]['uri']
        id_last_version = last_version.split('/')[-2]
        select_columns = self.get_selected_columns(select_columns)
        record_last_version = self.cr_version.find_one({ '_id': ObjectId( id_last_version ), 'form_id': self.form_id }, select_columns)
        if not record_last_version:
            return {}
        return record_last_version

    def get_key_id(self, key_id=None):
        if not key_id:
            key_id = self.status_id
        return key_id

    def getNum(self, data, key):
        res = data.get(key)
        if not res:
            res = 0
        return res

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

    def get_record_by_folio(self, folio, form_id, select_columns={}, limit=None):
        select_columns = self.get_selected_columns(select_columns)
        query = {
            'folio': folio,
            'deleted_at': {'$exists': False}
        }
        if form_id:
            query.update({'form_id':form_id})
        record_found = self.cr.find(query, select_columns)
        try:
            return record_found.next()
        except:
            return {}

    def get_record_by_folios(self, folios, form_id, select_columns={}, limit=None):
        select_columns = self.get_selected_columns(select_columns)
        query = {
            'folio': {"$in": folios},
            'deleted_at': {'$exists': False}
        }
        if form_id:
            query.update({'form_id':form_id})
        record_found = self.cr.find(query, select_columns)
        try:
            return [r for r in record_found]
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

    def get_record_by_ids(self, _ids,  select_columns=[]):
        select_columns = self.get_selected_columns(select_columns)
        _ids = [ObjectId(x) for x in _ids]
        query = {
            '_id': {"$in":ObjectId(_ids)},
            'deleted_at': {'$exists': False}
        }
        record_found = self.cr.find(query, select_columns)
        try:

            return [r for r in record_found]
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

    def get_selected_columns(self, select_columns):
        if select_columns:
            select_columns = {key:1 for key in select_columns}
        else:
            select_columns = {'folio':1,'user_id':1,'form_id':1,'answers':1,'_id':1,'connection_id':1,'created_at':1,'other_versions':1,'timezone':1}
        return select_columns

    def get_today_format(self):
        today = datetime.now()
        today = today.astimezone(timezone('America/Monterrey'))
        str_today = datetime.strftime(today, '%Y-%m-%d')
        today = datetime.strptime( '{} 00:00:00'.format( str_today ), '%Y-%m-%d %H:%M:%S')
        return today

    def get_value(self, get_value=None):
        if not get_value:
            get_value = self.close_status
        return get_value

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

    def list_to_str(self, list_to_proccess, separator=', ', show_empty=False):
        str_return = ''
        if show_empty:
            str_return += separator.join([a for a in list_to_proccess])
        else:
            str_return += separator.join([a for a in list_to_proccess if a])
        return str_return

    def make_header_dict(self, header):
        ### Return the directory with
        ### the column name : column number
        header_dict = {}
        for position in range(len(header)):
            header_dict[ str( header[ position ] ).lower().replace(' ' ,'_') ] = position
        return header_dict

    def match_query_by_type(self, data):
        if type(data) == list:
            return {'$in':data}
        else:
            return data

    def object_id(self):
        #Asegura que no exista el object_id en la base de datos
        cant = 1
        idx = 0
        while cant > 0:
            new_id = ObjectId()
            res = self.cr.find({"_id":new_id})
            cant = res.count()
        return str(new_id)
        
    def project_format(self, field_dict, **kwargs):
        """
        Return a project format for a field_name:ObjectId dictorionary 
        """
        project = {
                '_id': 1,
                'folio': "$folio",
                'created_at': "$created_at",
                'updated_at': "$updated_at",
        }

        for x in list(field_dict.keys()):
            if type(field_dict[x]) == str:
                project.update({x: f"$answers.{field_dict[x]}"})
            elif type(field_dict[x]) == dict:
                project.update({x: {list(field_dict[x].keys())[0]: f"$answers.{list(field_dict[x].values())[0]}"}})
        return project

    def read_current_record_from_txt(self, file_url):
        name_downloded = self.download_pdf( file_url, is_txt=True )
        f = open( "/tmp/{}".format( name_downloded ) )
        return simplejson.loads( f.read() )

    def read_file(self, file_url):
        sheet = pyexcel.get_sheet(url = file_url)
        all_records = sheet.array
        header = all_records.pop(0)
        return header, all_records

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

    def share_item(self, share_to, item_share, perm, can_delete=False, filter_name=None):
        data_to_share = {
            "owner": share_to,
            "file_shared": item_share,
            "perm": perm,
            "can_delete_records": can_delete
        }
        if filter_name:
            data_to_share["filter_name"] = filter_name
        res_shared = self.lkf_api.share_catalog(data_to_share)
        return res_shared

    def update_settings(self, settings, use_api=False):
        lkf_api = utils.Cache(settings)
        APIKEY = settings.config.get('APIKEY', settings.config.get('API_KEY', ))
        if not settings.config.get("SESSION"):
            user = lkf_api.get_jwt(api_key=APIKEY, get_user=True)
            try:
                if use_api:
                    settings.config["JWT_KEY"] = user.get('jwt')
                settings.config["APIKEY_JWT_KEY"] = user.get('jwt')
                account_id = user['user']['parent_info']['id']
                settings.config["USER_ID"] = user['user']['id']
                settings.config["ACCOUNT_ID"] = account_id
                settings.config["USER"] = user['user']
                settings.config["MONGODB_USER"] = 'account_{}'.format(account_id)
                self.user = user['user']
                settings.config["SESSION"] = True
            except Exception as e:
                self.LKFException('Error al cargar sus settings favor de revisar settings', e)
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

    def wf_create_relation(self, resp_create_record):
        if resp_create_record.get('status_code') == 201:
            # print('... creando workflow')
            record_created_id = resp_create_record.get('json', {}).get('id')
            record_created_folio = resp_create_record.get('json', {}).get('folio')
            self.wf_set_relation(record_created_id, record_created_folio, resp_create_record.get('data',''))

    def today_str(self, tz_name='America/Monterrey', date_format='date'):
        today = datetime.now()
        today = today.astimezone(timezone(tz_name))
        if date_format == 'datetime':
            str_today = datetime.strftime(today, '%Y-%m-%d %H:%M:%S')
        else:
            str_today = datetime.strftime(today, '%Y-%m-%d')
        return str_today

    def wf_set_relation(self, record_id_child, folio_child, data_response):
        name_script = self.data.get('name', '')
        child = {
            'created_at': datetime.utcnow(),
            'folio': self.current_record['folio'],
            'form_id': self.current_record['form_id'],
            'name': f"Script {name_script}",
            # 'record_id': ObjectId(record_id_father),
            # 'record_request_id': ObjectId(record_id_father),
            'record_id': ObjectId(self.record_id),
            'record_request_id': ObjectId(self.record_id),
            'record_response_content': data_response,
            'record_response_code': 201,
            'record_success': True,
            'record_status': 'created',
            "workflow_rule" : 2,
            "workflow_rule_name" : "Create Record",
            "workflow_sucess" : True,
            'workflow_record_folio': folio_child,
            'workflow_record_id': ObjectId(record_id_child),
            'workflow_response_content': data_response
        }
        res_cr = self.cr_wkf.insert_one(child)
        # print('res_cr', res_cr)

#####

class LKF_Report(LKF_Base):


    def __init__(self, settings, sys_argv=None, use_api=False, **kwargs):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
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
        res = {"json":{}}
        for x in self.json:
            res["json"][x] = self.json[x]
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
