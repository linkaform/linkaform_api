# coding: utf-8
#!/usr/bin/python

import time
from pydantic import BaseModel, validator, StrictBool, AnyUrl
from typing import (
    Deque, Optional, Union, List
)

from ..lkf_object import LKFBaseObject
from ..utils import Cache
from .base_models import UserData

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

    def serach_module_item(self, item_info):
        search_by = {
            'module':item_info['module'],
            'form_name':item_info['form_name'],
        }
        res = self.search(**item_info)
        if res and type(res) == list and len(res) > 0:
            return res[0]
        return False

    def install_forms(self, module, form_name, form_model):
        lkf_api = self.lkf_api
        user = self.get_user_data()
        item_info = {
                # 'created_by' : user,
                'module': module,
                # 'name': 'como lo ponomes',
                'form_type': 'form',
                'form_name':form_name,
            }
        item = self.serach_module_item(item_info)
        if item:
            #Creating New FormExist, lest update it!!!
            form_id = item['form_id']
            current_form_version = item['form_version'],
            form_version = form_model['updated_at'],
            if current_form_version == form_version:
                print('the form is at its latest state, no need to update')
                pass
            else:
                form_model.update({'form_id':form_id})
                #update form
                res = lkf_api.create_form(form_model)
                if res.get('status_code') == 201:
                    print('res=', res)

                    updated_at = res['json']['updated_at']['$date']
                    print('form veriosn', form_model['updated_at'])
                    item.update({
                        'updated_by':self.get_user_data(),
                        'form_version':form_model['updated_at'],
                        'updated_at':updated_at
                        })
                    update_query = {'_id':item['_id']}
                    self.update(update_query, item)
        else:
            #Creating New Form
            if form_model.get('form_id'):
                form_model.pop('form_id')
            res = lkf_api.create_form(form_model)
            if res.get('status_code') == 201:
                form_id = res['json']['form_id']
                item_info = {
                    'created_by' : self.get_user_data(),
                    'updated_by' : self.get_user_data(),
                    'created_at':int(time.time()),
                    'updated_at':int(time.time()),
                    'module': module,
                    'form_id': form_id,
                    'form_type': 'form',
                    'form_name':form_name,
                    'form_version':form_model['updated_at']
                }
                self.create(item_info)


