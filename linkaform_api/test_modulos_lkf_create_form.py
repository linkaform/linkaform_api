# -*- coding: utf-8 -*-
# import sys, simplejson
# from linkaform_api import settings, network, utils
# from pci_settings import *
import sys, simplejson
import settings, carga_universal
from utils import Cache

settings.mongo_hosts = 'dbs2.lkf.cloud:27918'
settings.mongo_port = 27918
settings.MONGODB_URI = 'mongodb://%s/'%(settings.mongo_hosts)
my_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImxpbmthZm9ybUBvcGVyYWNpb25wY2kuY29tLm14IiwidXNlcl9pZCI6MTQzMywicGFyZW50X2lkIjoxMjU5LCJpc19tb2JpbGUiOmZhbHNlLCJleHAiOjE2ODUzNzQxMzUsImRldmljZV9vcyI6IndlYiIsImVtYWlsIjoibGlua2Fmb3JtQG9wZXJhY2lvbnBjaS5jb20ubXgifQ.PmWDCW7QXjQmpw6TnwnTquPPoY0sLx9rPl6cXhpDm42V5iMbJpLEpZZ07MOdavIUuxHoVlr8DeAzJvLR9eRVyPNqBqje20JtVKVqGB8w--NN_TzzjHebtKk6blbAQVxedB8CGllgSVpJlmDdquHXOZsPjswVAPD5no62aNlCrd14DNo4OCet63liTMOiLjIHYWPD_3NsCsVSl8arBNhUUnHysKRFsqkRjsqtyKYjB3GS1LfHIXOvlD1kCODVaTnUs986eSioMeBgoogN821R_7OvRbQOUkIhIbT3cZ2rxgju-R9ms7YaybrdOQi2Idao14GiSZZbJmBog4N5se0f5euwahKrYhbHzrd5egDBcuk8EjE2qXEluiSJeu5MiC7uDh7Mu4RVN8jgjmKgXFnuLil6d-idLaLfRnqxa_j9rRHxzX6vML5Gn4xYHXV1RnCXIFIyt1s2kEXbmjcrGOkJ_jJ9ccnRRhlnEdc5HPRQ7mlcveyQgXZSkbNHZj5KbOwZO0vSBlkU8or_AvR4kAVpfyjMrE8P2exOHbvbDvXKV6c7xi_wu0vfFLxLXxJR3XQqXndME2X7iPnR7uIVPZ6rZWFhpH5LeRV5QvdmCvz0rgN1m7j_xwjYFOLb4NXmQwjuBdqMZy0-fTbWsFckzgwf_2yAJkfmVj8w-svDrguXuGw'
config = {
    'USERNAME' : 'linkaform@operacionpci.com.mx',
    'PASS' : '',
    'COLLECTION' : 'form_answer',
    'PROTOCOL' : 'https', #http or https
    'HOST' : 'preprod.linkaform.com',
    'MONGODB_PORT':settings.mongo_port,
    'MONGODB_HOST': settings.mongo_hosts,
    'MONGODB_USER': 'account_1259',
    'MONGODB_PASSWORD': '0a0613e9281b6a88fbdc9703fa012e46168bcbf4',
    'PORT' : settings.mongo_port,
    'USER_ID' : 1433,
    'ACCOUNT_ID' : 1259,
    'KEYS_POSITION' : {},
    'IS_USING_APIKEY' : False,
    'USE_JWT' : True,
    'AUTHORIZATION_EMAIL_VALUE' : 'linkaform@operacionpci.com.mx',
    'AUTHORIZATION_TOKEN_VALUE' : '7d3bde3c53d7e189ed7dda80dad246de7f7e81a2',
    'JWT_KEY': my_jwt,
    'USER_JWT_KEY': my_jwt
}
settings.config.update(config)

if __name__ == '__main__':
    lkf_api = Cache(settings)

    """
    form_id_base = 98193
    '''
    # Se obtiene la forma con todos sus campos para duplicarla y crear una copia
    '''
    form_downloaded = lkf_api.get_form_to_duplicate(form_id_base, jwt_settings_key='USER_JWT_KEY')
    form_downloaded['name'] = 'Una forma mas ya con todo'
    response_create_form = lkf_api.create_form(form_downloaded, jwt_settings_key='USER_JWT_KEY')
    print('response_create_form =',response_create_form)
    if response_create_form.get('status_code') == 201:
        new_form_id = response_create_form.get('json', {}).get('form_id')
        print('new_form_id = ',new_form_id)
        '''
        # Duplico las Reglas
        '''
        form_rules = lkf_api.get_form_rules(form_id_base, jwt_settings_key='USER_JWT_KEY')
        if form_rules:
            form_rules = form_rules[0]
            form_rules.pop('id')
            form_rules['form_id'] = new_form_id
            response_rules = lkf_api.upload_rules(form_rules, jwt_settings_key='USER_JWT_KEY')
            #print('response_rules =',response_rules)
        '''
        # Duplico los Workflows
        '''
        form_workflows = lkf_api.get_form_workflows(form_id_base, jwt_settings_key='USER_JWT_KEY')
        if form_workflows:
            form_workflows = form_workflows[0]
            form_workflows.pop('id')
            form_workflows['form_id'] = new_form_id
            for w in form_workflows.get('workflows', []):
                if w.get('id'):
                    w.pop('id')
                for a in w.get('actions', []):
                    if a.get('_id'):
                        a.pop('_id')
            print(form_workflows)
            response_workflows = lkf_api.upload_workflows(form_workflows, jwt_settings_key='USER_JWT_KEY')
            #print('response_workflows =',response_workflows)
    """

    '''
    # Haciendo pruebas del catalogo
    json_catalog = {
        "name": "prueba creacion desde la Api",
        "active": True,
        "description": "",
        "edit_public_records": False,
        "catalog_pages": [
            {
                "page_fields": [
                    {
                        "field_id": None,
                        "field_type": "text",
                        "label": "hola mundo",
                        "visible": True,
                        "required": False,
                        "validations": {},
                        "default_value": "",
                        "rules": [],
                        "properties": {
                            "size": "complete",
                            "custom": None,
                            "send_email": False
                        },
                        "groups_fields": [],
                        "$$hashKey": "042"
                    }
                ],
                "page_name_tab": "page_name1",
                "page_name": "PAGE 1",
                "$$hashKey": "02T"
            }
        ],
        "advanced_options": {},
        "public": False
    }
    resp_create_catalog = lkf_api.create_catalog(json_catalog, jwt_settings_key='USER_JWT_KEY')
    #print('resp_create_catalog =',resp_create_catalog)
    if resp_create_catalog.get('status_code',0) == 201:
        data_catalog = simplejson.loads( resp_create_catalog.get('data', '{}') )
        print('Catalogo creado correctamente =',data_catalog.get('catalog_id'))
    '''

    # Haciendo pruebas de carga de scripts
    '''
    dir_script = 'TestUploadScript/delete_old_images.py'
    resp_upload_script = lkf_api.post_upload_script(dir_script, jwt_settings_key='USER_JWT_KEY')
    print('resp_upload_script =',resp_upload_script)
    if resp_upload_script.get('status_code') == 200:
        print('Script cargado')
    '''

    dir_excel = 'PruebasCU.xlsx'
    form_id_to_load = 43181
    class_cu = carga_universal.CargaUniversal(settings=settings)
    resp_cu = class_cu.carga_doctos(form_id_to_load=form_id_to_load, read_excel_from=dir_excel)
    print('resp_cu =',resp_cu)