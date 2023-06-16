# coding: utf-8
#!/usr/bin/python

#Python Imports
import time
from pydantic import BaseModel, validator, StrictBool, AnyUrl
from typing import (
    Deque, Optional, Union, List
)

from jinja2 import Environment, FileSystemLoader

#LinkaForm Imports
from ..lkf_object import LKFBaseObject
from ..utils import Cache
from .base_models import UserData



class LKFException(BaseException):
    print('es un error del tipo lkf')
    def __init__(self, message, res=None):
        self.message = message + 'tset'

    def LKFException(self, msg):
        return BaseException(msg)

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
        self.module_data = {} 
        #Inicializa la variable module_data para saber que modulos estan instalados
        self.get_installed_modules()

    def serach_module_item(self, item_info):
        search_by = {
            'module':item_info['module'],
            'form_name':item_info['item_name'],
        }
        res = self.search(**item_info)
        if res and type(res) == list and len(res) > 0:
            return res[0]
        return False

    def install_script(self, module, script_path, image=None, script_properties=None):
        lkf_api = self.lkf_api
        user = self.get_user_data()
        script_name = script_path.split('/')[-1]
        script_name = script_name.split('.')[0]
        print('script_name=', script_name)
        item_info = {
                # 'created_by' : user,
                'module': module,
                # 'name': 'como lo ponomes',
                'item_type': 'script',
                'item_name':script_name,
            }
        item = self.serach_module_item(item_info)
        script_version = lkf_api.get_md5hash(script_path)
        if item:
            item_id = item['item_id']
            script_item_version = item['item_version']
            if script_version == script_item_version:
                item_info.update(item)
                print('The script is up to date')
                pass
            else:
                #update form
                res = lkf_api.post_upload_script(script_path, script_id=item_id, image=image)
                if res.get('status_code') == 200:
                    updated_at = int(time.time())
                    item.update({
                        'updated_by':int(time.time()),
                        'item_version':script_version,
                        'updated_at':updated_at
                        })
                    update_query = {'_id':item['_id']}
                    item_info.update(item)
                    self.update(update_query, item)
                elif res.get('status_code') == 404:
                    item = None
                    raise LKFException('Not found.....')
                elif res.get('status_code') == 400:
                    raise LKFException('Ya existe un script con este Nombre')
                else:
                    raise LKFException('Error updating catalog model')
        else:
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
                    'item_type': 'script',
                    'item_name':script_name,
                    'item_full_name':script_path,
                    'item_version':script_version,
                }
                self.create(item_info)
                self.load_module_data( module, 'script', script_name, script_name, script_id)
                self.load_item_data('script', script_name, script_name, script_id)
            elif res.get('status_code') == 400:
                raise LKFException('Ya existe un script con este Nombre')
            else:
                raise LKFException('Error creating script')
        if script_properties:
            self.set_script_properties(item_info['item_id'], script_properties)
        return item_info

    def set_script_properties(self, script_id, properties):
        res = self.lkf_api.update_script(script_id, properties)

    def install_catalog(self, module, catalog_name, catalog_model):
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
        if item:
            #Creating New FormExist, lest update it!!!

            item_id = item['item_id']
            catalog_item_revision = item['item_version']
            catalog_version = catalog_model['updated_at']
            if catalog_item_revision != catalog_version:
                print('the form is at its latest state, no need to update')
                pass
            else:
                catalog_model.update({'catalog_id':item_id})
                #update form
                res = lkf_api.update_catalog_model(item_id, catalog_model)
                if res.get('status_code') == 202:
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
                    raise LKFException('Not found.....')
                else:
                    raise LKFException('Error updating catalog model')

        else:
            #Creating New Catalog
            if catalog_model.get('catalog_id'):
                catalog_model.pop('catalog_id')
            if catalog_model.get('_rev'):
                catalog_model.pop('_rev')
            res = lkf_api.create_catalog(catalog_model)
            catalog_full_name = catalog_model['name']
            if res.get('status_code') == 201:
                item_obj_id = res['json']['_id']
                catalog_id = res['json']['catalog_id']
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
                    'item_version':catalog_model['updated_at']
                }
                self.create(item_info)
                self.load_module_data( module, 'catalog', catalog_name, catalog_full_name, catalog_id)
                self.load_item_data('catalog', catalog_name, catalog_full_name, catalog_id, item_obj_id)
            else:
                raise LKFException('Error creating catalog model')
        return item_info

    def install_forms(self, module, form_name, form_model):
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
            if current_form_version == form_version:
                print('the form is at its latest state, no need to update')
                item['status'] = 'unchanged'
                item_info.update(item)
                pass
            else:
                form_model.update({'form_id':item_id})
                #update form
                res = lkf_api.create_form(form_model)
                if res.get('status_code') == 201:
                    updated_at = res['json']['updated_at']['$date']
                    print('form veriosn', form_model['updated_at'])
                    item.update({
                        'updated_by':self.get_user_data(),
                        'item_version':form_model['updated_at'],
                        'updated_at':updated_at,
                        'status':'update'
                        })
                    item_info.update(item)
                    update_query = {'_id':item['_id']}
                    self.update(update_query, item)
        else:
            print('createing new form')
            #Creating New Form
            if form_model.get('form_id'):
                form_model.pop('form_id')
            res = lkf_api.create_form(form_model)
            import simplejson
            form_full_name = form_model['name']
            if res.get('status_code') == 201:
                form_id = res['json']['form_id']
                item_info = {
                    'created_by' : self.get_user_data(),
                    'updated_by' : self.get_user_data(),
                    'created_at':int(time.time()),
                    'updated_at':int(time.time()),
                    'module': module,
                    'item_id': form_id,
                    'item_type': 'form',
                    'item_name':form_name,
                    'item_full_name':form_full_name,
                    'item_version':form_model['updated_at'],
                    'status':'create'
                }
                self.create(item_info)
                self.load_module_data( module, 'form', form_name, form_full_name, form_id)
                self.load_item_data('form', form_name, form_full_name, form_id)
            else:
                return res
        return item_info

    def fetch_installed_modules(self, item=None):
        cr, data = self.get_cr_data()
        if item:
            return cr.find({'item_type': item}, {'module':1, 'item_type':1, 'item_name':1, 'item_id':1})
        return cr.find({}, {'module':1, 'item_type':1, 'item_name':1, 'item_id':1})

    def load_item_data(self, item_type, item_name, item_full_name, item_id, item_obj_id=None):
        self.module_data[item_type] = self.module_data.get(item_type,{})
        self.module_data[item_type][item_name] = self.module_data[item_type].get(item_name,{'id':None,'name':'', 'obj_id':None})
        self.module_data[item_type][item_name]['id'] = item_id
        self.module_data[item_type][item_name]['name'] = item_full_name      
        self.module_data[item_type][item_name]['obj_id'] = item_obj_id      
        return True

    def load_module_data(self, module, item_type, item_name, item_full_name, item_id):
        if module:
            self.module_data[module] = self.module_data.get(module,{})
            if item_type:
                self.module_data[module][item_type] = self.module_data[module].get(item_type,{})
                if item_name:
                    self.module_data[module][item_type][item_name] = self.module_data[module][item_type].get(item_name,{})
                    self.module_data[module][item_type][item_name]['id'] = item_id
                    self.module_data[module][item_type][item_name]['name'] = item_full_name
        return True

    def get_installed_modules(self):
        for x in self.fetch_installed_modules():
            module = x.get('module') 
            item_type = x.get('item_type','') 
            item_name = x.get('item_name','') 
            item_full_name = x.get('item_full_name',item_name) 
            item_id = x.get('item_id') 
            if module:
                self.load_module_data(module, item_type, item_name, item_full_name, item_id)
            if item_type:
                self.load_item_data(item_type, item_name, item_full_name, item_id)
        return True

    def read_template_file(self, file_path, file_name, file_data=None):
        # Create a Jinja2 environment
        env = Environment(loader=FileSystemLoader(f'{file_path}'))
        # Load the template
        template = env.get_template(file_name)
        # Load and parse the JSON data
        # Render the template with JSON data
        # print('module_data=', self.module_data)
        output = template.render(self.module_data)
        # Print or use the rendered output
        json_file = self.lkf_api.xml_to_json(output)
        return json_file

