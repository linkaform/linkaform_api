# coding: utf-8
#!/usr/bin/python

#Python Imports
import time, simplejson
from bson import ObjectId
from pydantic import BaseModel, validator, StrictBool, AnyUrl
from typing import (
    Deque, Optional, Union, List
)

from jinja2 import Environment, FileSystemLoader, exceptions, select_autoescape
from datetime import datetime

#LinkaForm Imports
from ..lkf_object import LKFBaseObject
from ..utils import Cache
from .base_models import UserData



# class self.LKFException(BaseException):
#     def __init__(self, message, res=None):
#         self.message = message + 'tset'

#     def self.LKFException(self, msg):
#         return BaseException(msg)

class LKFModulesModel(BaseModel, LKFBaseObject):
    created_by: UserData
    updated_by: UserData
    module: str
    created_at: int
    updated_at: int
    form_type: Optional[str]
    form_id: Optional[int]
    form_name: Optional[str]
    form_version: Optional[int]

    catalog_name: Optional[str]
    catalog_type: Optional[str]
    catalog_id: Optional[int]
    
    script_type: Optional[str]
    script_id: Optional[int]
    script_name: Optional[str]
    
    report_type: Optional[str]
    report_id: Optional[int]
    report_name: Optional[str]

    @validator('form_type')
    def formtype_valid(cls, v):
        return self.itemtype_valid(v)    

    @validator('catalog_type')
    def catalogtype_valid(cls, v):
        return self.itemtype_valid(v)

    @validator('script_type')
    def scripttype_valid(cls, v):
        return self.itemtype_valid(v)

    @validator('report_type')
    def reporttype_valid(cls, v):
        return self.itemtype_valid(v)

    def itemtype_valid(cls, v):
        type_options = [
            'form', 'catalog', 'report', 'script', 
            'form_foleder', 'catalog_foleder', 'report_foleder', 'script_foleder']
        if v and v not in type_options:
            raise InvalidAPIUsage('item_type: Item Type {}, is not a valid options'.format(v, type_options))
        return v

class LKFModules(LKFBaseObject):

    def __init__(self, settings):
        self.settings = settings
        self.config = settings.config
        self.name =  __class__.__name__
        self.lkf_api = Cache(settings)
        self.module_data = {'form':{},'catalog':{},'script':{}} 
        #Inicializa la variable module_data para saber que modulos estan instalados
        self.get_installed_modules()

    def bad_request(self, form_model):
        form_pages = form_model.get('form_pages')
        for page in form_pages:
            fields = page.get('page_fields')
            for field in fields:
                print('field id', field.get('field_id'))

    def catalog_id(self, catalog_name, info=None):
        return self.item_id(catalog_name, 'catalog', info=info)

    def create_catalog_filters(self, catalog_id, catalog_filters, method='create'):
        res = []
        exiting_filters = self.lkf_api.get_catalog_filters(catalog_id)
        for filter_name, filter_to_search in catalog_filters.items():
            filter_selected=None
            if method == 'update':
                filter_selected = f'filters/{filter_name}'
            res.append(self.lkf_api.create_filter(catalog_id, filter_name, filter_to_search, filter_selected=filter_selected))
        return res

    def create_folder(self, module, folder_type, folder_name, **kwargs):
        folder_path = ''
        parent_id = None
        for f_name in folder_name.split('/'):
            folder_info = {
                'module': module,
                'item_type': folder_type + '_folder',
                'item_name':f_name,
            }
            folder = self.serach_module_item(folder_info)
            if folder:
                item_id = folder['item_id']
                item_name = folder['item_name']
                status_code = 200
                if parent_id:
                    self.update_parent_id(parent_id, folder, **kwargs)
                parent_id = folder['item_id']
            else:
                res = self.lkf_api.create_folder(folder_type, f_name)
                status_code = res.get('status_code')
                if status_code == 201:
                    item_id = res.get('json',{}).get('id')
                    item_name = res.get('json',{}).get('name')
                    item_info = {
                        'created_by' : self.get_user_data(),
                        'updated_by' : self.get_user_data(),
                        'created_at':int(time.time()),
                        'updated_at':int(time.time()),
                        'module': module,
                        'item_id': item_id,
                        'item_type': folder_type + '_folder',
                        'item_full_name': item_name,
                        'item_name': item_name,
                        'load_data': False,
                        'load_demo': False,
                        'local_path': folder_name,
                        'parent_id':parent_id
                    }
                    self.create(item_info)
                    if parent_id:
                        self.lkf_api.move_item(parent_id, [item_id,])
                    parent_id = item_id
            if folder_path:
                folder_path += '/'
            folder_path += item_name
        return {'status_code':status_code, 'item_name':item_name, 'item_id': item_id}

    def fetch_installed_modules(self, item=None):
        cr, data = self.get_cr_data(collection='LKFModules')
        if item:
            return cr.find({'item_type': item}, {'module':1, 'item_type':1, 'item_name':1, 'item_id':1,'item_obj_id':1})
        else:
            return cr.find({}, {'module':1, 'item_type':1, 'item_name':1, 'item_id':1,'item_obj_id':1})

        return cr.find({}, {'module':1, 'item_type':1, 'item_name':1, 'item_id':1,'item_obj_id':1})

    def form_id(self, form_name, info=None):
        return self.item_id(form_name, 'form', info=info)

    def get_module_items(self, module_name):
        cr, data = self.get_cr_data(collection='LKFModules')
        return cr.find({'module': module_name}, {'module':1, 'item_type':1, 'item_name':1, 'item_id':1}).sort([('item_type',1)])

    def get_item_name_obj_id(self, item_obj_id, item_type):
        cr, data = self.get_cr_data(collection='LKFModules')
        return cr.find({'item_obj_id': item_obj_id, 'item_type':item_type}, {'item_name':1,'item_full_name':1})

    def get_installed_modules(self):
        for x in self.fetch_installed_modules():
            module = x.get('module') 
            item_type = x.get('item_type','') 
            item_name = x.get('item_name','') 
            item_full_name = x.get('item_full_name',item_name) 
            item_id = x.get('item_id') 
            item_obj_id = x.get('item_obj_id') 
            if module:
                self.load_module_data(module, item_type, item_name, item_full_name, item_id, item_obj_id)
            if item_type:
                self.load_item_data(item_type, item_name, item_full_name, item_id, item_obj_id)
        return True

    def load_item_data(self, item_type, item_name, item_full_name, item_id, item_obj_id=None):
        self.module_data[item_type] = self.module_data.get(item_type,{})
        self.module_data[item_type][item_name] = self.module_data[item_type].get(item_name,{'id':None,'name':'', 'obj_id':None})
        self.module_data[item_type][item_name]['id'] = item_id
        self.module_data[item_type][item_name]['name'] = item_full_name      
        self.module_data[item_type][item_name]['obj_id'] = item_obj_id      
        return True

    def load_module_data(self, module, item_type, item_name, item_full_name, item_id, item_obj_id=None):
        if module:
            self.module_data[module] = self.module_data.get(module,{})
            if item_type:
                self.module_data[module][item_type] = self.module_data[module].get(item_type,{})
                if item_name:
                    self.module_data[module][item_type][item_name] = self.module_data[module][item_type].get(item_name,{})
                    self.module_data[module][item_type][item_name]['id'] = item_id
                    self.module_data[module][item_type][item_name]['name'] = item_full_name
                    self.module_data[module][item_type][item_name]['item_obj_id'] = item_obj_id
        return True

    def install_catalog(self, module, catalog_name, catalog_model, local_path="", **kwargs):
        """
        Installs catalog on LKFModule database

        Args: 
            module (str): name of the module
            catalog_name (str): name of the catalog
            catalog_model (str): JSON model of the catalog 
        """
        parent_id = None
        if local_path:
            folder = self.create_folder(module, 'catalog', local_path)
            parent_id = folder.get('item_id')
        catalog_filters = []
        lkf_api = self.lkf_api
        user = self.get_user_data()
        item_info = {
                # 'created_by' : user,
                'module': module,
                # 'name': 'como lo ponomes',
                'item_type': 'catalog',
                'item_name':catalog_name,
            }
        item = self.serach_module_item(item_info)
        if catalog_model.get('filters'):
            catalog_filters = catalog_model.pop('filters')
        if item:
            #Creating New FormExist, lest update it!!!
            self.update_parent_id(parent_id, item, **kwargs)
            item_id = int(item['item_id'])
            item_info.update({
                '_id': item['_id'],
                'item_id': item_id, 
                'load_data':item.get('load_data'), 
                'load_demo':item.get('load_demo') ,
                'parent_id':parent_id})
            catalog_item_revision = item['item_version']
            catalog_version = catalog_model['updated_at']
            catalog_item_revision =  datetime.strptime(catalog_item_revision[:19], "%Y-%m-%dT%H:%M:%S")
            catalog_version =  datetime.strptime(catalog_version[:19], "%Y-%m-%dT%H:%M:%S")
            if False: #catalog_version >= catalog_item_revision and catalog_name:
                print(f'the catalog is at its latest state {catalog_version}, {catalog_item_revision}vs no need to update')
                pass
            else:
                self.update_parent_id(parent_id, item, **kwargs)
                catalog_model.update({'catalog_id':item_id})
                #update form
                # import simplejson
                cm = simplejson.dumps(catalog_model, indent=4)
                res = lkf_api.update_catalog_model(item_id, catalog_model)
                if res.get('status_code') == 202:
                    if catalog_filters:
                        self.create_catalog_filters(item_id, catalog_filters, method='update')
                    updated_at = res['json']['updated_at']
                    item.update({
                        'updated_by':self.get_user_data(),
                        'item_version':catalog_model['updated_at'],
                        'updated_at':updated_at
                        }) 
                    update_query = {'_id':item['_id']}
                    item_info.update(item)
                    self.update(update_query, item)

                elif res.get('status_code') == 404:
                    item = None
                    raise self.LKFException('While updating item_id: {} with name {}, was not found on the database for an update.....'.format(item_id, catalog_name))
                else:
                    raise self.LKFException(f'Error updating catalog model {catalog_name}, item_id: {item_id}, response: {res}, check if item exist.')

        else:
            #Creating New Catalog
            if catalog_model.get('catalog_id'):
                catalog_model.pop('catalog_id')
            if catalog_model.get('_rev'):
                catalog_model.pop('_rev')
            catalog_full_name = catalog_model.get('name',catalog_name)
            res = lkf_api.create_catalog(catalog_model)
            if res.get('status_code') == 201:
                item_obj_id = res['json']['_id']
                catalog_id = res['json']['catalog_id']
                if catalog_filters:
                    self.create_catalog_filters(catalog_id, catalog_filters, method='create')
                item_info = {
                    'created_by' : self.get_user_data(),
                    'updated_by' : self.get_user_data(),
                    'created_at':int(time.time()),
                    'updated_at':int(time.time()),
                    'module': module,
                    'item_id': catalog_id,
                    'item_obj_id': item_obj_id,
                    'item_type': 'catalog',
                    'item_name':catalog_name,
                    'item_full_name':catalog_full_name,
                    'load_data': False,
                    'load_demo': False,
                    'item_version':catalog_model['updated_at'],
                    'local_path': local_path,
                }
                self.update_parent_id(parent_id, item_info, **kwargs)
                item_info.update({'parent_id':parent_id})    
                self.create(item_info)
                self.load_module_data( module, 'catalog', catalog_name, catalog_full_name, catalog_id)
                self.load_item_data('catalog', catalog_name, catalog_full_name, catalog_id, item_obj_id)
            else:
                raise self.LKFException('Error creating catalog model', res)
        return item_info

    def install_forms(self, module, form_name, form_model, local_path="", **kwargs):
        parent_id = None
        if local_path:
            folder = self.create_folder(module, 'form', local_path)
            parent_id = folder.get('item_id')
        lkf_api = self.lkf_api
        user = self.get_user_data()
        item_info = {
                # 'created_by' : user,
                'module': module,
                # 'name': 'como lo ponomes',
                'item_type': 'form',
                'item_name':form_name,
            }
        item = self.serach_module_item(item_info)
        if item:
            #Creating New FormExist, lest update it!!!
            item_id = item['item_id']
            current_form_version = item['item_version'],
            form_version = form_model['updated_at'],
            if current_form_version == form_version and False:
                item['status'] = 'unchanged'
                item_info.update(item)
                print('nothgin new')
                pass
            else:
                self.update_parent_id(parent_id, item, **kwargs)
                form_model.update({'form_id':item_id})
                #update form
                res = lkf_api.create_form(form_model)
                if res.get('status_code') == 201:
                    updated_at = res['json']['updated_at']['$date']
                    item.update({
                        'updated_by':self.get_user_data(),
                        'item_version':form_model['updated_at'],
                        'updated_at':updated_at,
                        'status':'update',
                        'parent_id':parent_id
                        })
                    if not item.get('item_obj_id'):
                        item.update({'item_obj_id': str(ObjectId())})
                    item_info.update(item)
                    update_query = {'_id':item['_id']}
                    self.update(update_query, item)
                else:
                    print('Something went wrong, we could not update the form:', res)
        else:
            #Creating New Form
            if form_model.get('form_id'):
                form_model.pop('form_id')
            # print('form_model', form_model)
            res = lkf_api.create_form(form_model)
            form_full_name = form_model['name']
            if res.get('status_code') == 201:
                form_id = res['json']['form_id']
                item_obj_id = str(ObjectId())
                item_info = {
                    'created_by' : self.get_user_data(),
                    'updated_by' : self.get_user_data(),
                    'created_at':int(time.time()),
                    'updated_at':int(time.time()),
                    'module': module,
                    'item_id': form_id,
                    'item_obj_id': item_obj_id,
                    'item_type': 'form',
                    'item_name':form_name,
                    'item_full_name':form_full_name,
                    'item_version':form_model['updated_at'],
                    'status':'create'
                }
                self.update_parent_id(parent_id, item_info, **kwargs)
                item_info.update({'parent_id':parent_id})   
                self.create(item_info)
                self.load_module_data( module, 'form', form_name, form_full_name, form_id)
                self.load_item_data('form', form_name, form_full_name, form_id, item_obj_id)
            else:
                # self.bad_request(form_model)
                return res
        return item_info

    def install_script(self, module, script_path, image=None, script_properties=None, local_path="", **kwargs):
        parent_id = None
        item_type = kwargs.get('item_type', 'script')
        folder_type = kwargs.get('folder_type', 'script')
        if local_path:
            folder = self.create_folder(module, folder_type, local_path)
            parent_id = folder.get('item_id')
        lkf_api = self.lkf_api
        user = self.get_user_data()
        script_name = script_path.split('/')[-1]
        script_name = script_name.split('.')[0]
        item_info = {
                # 'created_by' : user,
                'module': module,
                # 'name': 'como lo ponomes',
                'item_type': item_type,
                'item_name':script_name,
            }
        item = self.serach_module_item(item_info)
        script_version = lkf_api.get_md5hash(script_path)
        if item and script_version:
            item_id = int(item['item_id'])
            script_item_version = item['item_version']
            if script_version == script_item_version:
                item_info.update(item)
                self.update_parent_id(parent_id, item, **kwargs)
                pass
            else:
                #update form
                print('Updating script: ', script_name)
                print('Updating item_id: ', item_id)
                self.update_parent_id(parent_id, item, **kwargs)
                res = lkf_api.post_upload_script(script_path, script_id=int(item_id), image=image)
                if res.get('status_code') == 200:
                    updated_at = int(time.time())
                    item.update({
                        'updated_by':int(time.time()),
                        'item_version':script_version,
                        'updated_at':updated_at,
                        'parent_id':parent_id
                        })
                    update_query = {'_id':item['_id']}
                    item_info.update(item)
                    self.update(update_query, item)
                elif res.get('status_code') == 404:
                    item = None
                    raise self.LKFException('Not found.....',res.get('status_code'))
                elif res.get('status_code') == 400:
                    raise self.LKFException(f'Ya existe un script con este Nombre: {script_name}, item_id:{item_id}')
                else:
                    raise self.LKFException('Error updating catalog model')
        else:
            print('Creating script: ', script_name)
            #Creating New Script
            res = lkf_api.post_upload_script(script_path, image=image)
            if res.get('status_code') == 200:
                script_id = res['json']['id']
                item_info = {
                    'created_by' : self.get_user_data(),
                    'updated_by' : self.get_user_data(),
                    'created_at': int(time.time()),
                    'updated_at':int(time.time()),
                    'module': module,
                    'item_id': script_id,
                    'item_type': item_type,
                    'item_name':script_name,
                    'item_full_name':script_path,
                    'item_version':script_version,
                }
                item_info.update({'parent_id':parent_id})   
                self.create(item_info)
                self.load_module_data( module, item_type, script_name, script_name, script_id)
                self.load_item_data('script', script_name, script_name, script_id)
                self.update_parent_id(parent_id, item_info, **kwargs)
            elif res.get('status_code') == 400:
                raise self.LKFException(f'Ya existe un script con este Nombre: {script_name}')
            else:
                raise self.LKFException('Error creating script')
        if script_properties:
            self.set_script_properties(item_info['item_id'], script_properties)
        return item_info
  
    def install_report(self, module, report_name, report_path, report_model, local_path="", **kwargs):
        parent_id = None
        if local_path:
            folder = self.create_folder(module, 'report', local_path)
            parent_id = folder.get('item_id')
        lkf_api = self.lkf_api
        user = self.get_user_data()
        item_info = {
                # 'created_by' : user,
                'module': module,
                # 'name': 'como lo ponomes',
                'item_type': 'report',
                'item_name':report_name,
            }
        item = self.serach_module_item(item_info)
        if item:
            #Creating New reportExist, last update it!!!
            item_id = item['item_id']
            current_report_version = item['item_version'],
            report_version = report_model.get('updated_at'),
            if current_report_version == report_version and False:
                item['status'] = 'unchanged'
                item_info.update(item)
                self.update_parent_id(parent_id, item, **kwargs)
                print('nothgin new')
                pass
            else:
                self.update_parent_id(parent_id, item, **kwargs)
                report_model.update({'id':item_id})
                #update report
                res = lkf_api.update_report(item_id, report_model)
                if res.get('status_code') == 202:
                    updated_at = None
                    item.update({
                        'updated_by':self.get_user_data(),
                        'item_version':report_model.get('updated_at'),
                        'updated_at':updated_at,
                        'status':'update',
                        'parent_id':parent_id
                        })
                    item_info.update(item)
                    update_query = {'_id':item['_id']}
                    self.update(update_query, item)
                else:
                    print('Something went wrong, we could not update the report:', res)
        else:
            #Creating New report
            res = lkf_api.create_report(report_model )
            report_full_name = report_model['name']
            if res.get('status_code') == 201:
                report_id = res['json']['id']
                item_info = {
                    'created_by' : self.get_user_data(),
                    'updated_by' : self.get_user_data(),
                    'created_at':int(time.time()),
                    'updated_at':int(time.time()),
                    'module': module,
                    'item_id': report_id,
                    'item_type': 'report',
                    'item_name':report_name,
                    'item_full_name':report_full_name,
                    'item_version':report_model.get('updated_at'),
                    'status':'create'
                }
                print('parent_id', parent_id)
                self.update_parent_id(parent_id, item_info, **kwargs)
                self.create(item_info)
                item_info.update({'parent_id':parent_id})   
                self.load_module_data( module, 'report', report_name, report_full_name, report_id)
                self.load_item_data('report', report_name, report_full_name, report_id)
            else:
                # self.bad_request(report_model)
                return res
        return item_info

    def item_id(self, item_name, item_type, info=None):
        res = self.module_data[item_type].get(item_name)
        if info:
            return res.get(info)
        else:
            return res

    def script_id(self, script_name, info=None):
        return self.item_id(script_name, 'script', info=info)

    def set_script_properties(self, script_id, properties):
        res = self.lkf_api.update_script(script_id, properties)

    def update_parent_id(self, parent_id, item_obj, **kwargs):
        force = kwargs.get('force')
        if parent_id != item_obj.get('parent_id') or force:
            item_id = item_obj['item_id']
            move_res = self.lkf_api.move_item(parent_id, [item_id,])
            if item_obj.get('_id'):
                update_query = {'_id':item_obj['_id']}
                if move_res.get('status_code') == 202:
                    item_obj.update({'parent_id':parent_id})
                    self.update(update_query, item_obj)
                elif move_res.get('status_code') == 404:
                    print('no encontro el script....')
                else:
                    self.LKFException('Error moving {}  called {}.'.format(item_obj['item_name'], move_res))
            else:
                if move_res.get('status_code') != 202:
                    self.LKFException('Error moving NEW item {}  called: {}'.format(item_obj['item_name'], move_res ))
        return {'status_code':200}

    def read_template_file(self, file_path, file_name, file_data=None):
        # Create a Jinja2 environment
        # file_path = '/srv/scripts/addons/modules/base/items/forms/Base/_tmp/'
        env = Environment(
                loader=FileSystemLoader(f'{file_path}'), 
                autoescape=select_autoescape(
                            enabled_extensions=('html', 'xml'),
                            default_for_string=True,)
              )
        # Load the template
        template = env.get_template(file_name)
        # Load and parse the JSON data
        # Render the template with JSON data
        try:
            output = template.render(self.module_data)
        except exceptions.UndefinedError as e:
            self.LKFException(f'Falta de instalar un modulo con path: {file_path} y nombre : {file_name} con error:  ' + str(e))
        # Print or use the rendered output
        return output
        json_file = self.lkf_api.xml_to_json(output)
        return json_file

    def remove_module_items(self, item_ids):
        cr, data = self.get_cr_data(collection='LKFModules')
        return cr.remove({'item_id': {'$in': item_ids}})
