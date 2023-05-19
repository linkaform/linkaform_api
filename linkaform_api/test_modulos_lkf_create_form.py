# -*- coding: utf-8 -*-
# import sys, simplejson
# from linkaform_api import settings, network, utils
# from pci_settings import *
import sys, simplejson
import settings
from utils import Cache

settings.mongo_hosts = 'dbs2.lkf.cloud:27918'
settings.mongo_port = 27918
settings.MONGODB_URI = 'mongodb://%s/'%(settings.mongo_hosts)
my_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImxpbmthZm9ybUBvcGVyYWNpb25wY2kuY29tLm14IiwidXNlcl9pZCI6MTQzMywicGFyZW50X2lkIjoxMjU5LCJpc19tb2JpbGUiOmZhbHNlLCJleHAiOjE2ODQ0NzE5MjAsImRldmljZV9vcyI6IndlYiIsImVtYWlsIjoibGlua2Fmb3JtQG9wZXJhY2lvbnBjaS5jb20ubXgifQ.LSUkY2xYEdT6zJtk_YRC2-Pzd07MJBIKdbcIRPwNr7gtbJkIF_VaBSVVGuTQPKjUIsts1f0vYdv10VUuZ5L-oh5aj11uMXUKm15ODGq-FKWRQV6ZDaxVEBe_HBFvspVqedKHtmkFbmotDBDtc6T9SF2j1DRXeWOYg1gOdJa4QUv1oFjED0UiksbKyFLbhIhhBkV2MCxA1T_CvjYcNWMyOaVkWV05xhUxYP7v0gjzGYYE93a_Qg6BpA-BL-rfDWaKAPQV1r80ECe5nWqWFOsYdWgcaABjPArqb8Kl2A61MxASto9SKSypxSjVGH4RBSThtzcfEzbbgfnw2RsUhdfX-UsM0tuaTK2Z6AehxyUiZMUZmwLpbmUCMwJ67aYimKui5Q0euxdKqwXb4x2XE-k_zZE6hqkNt5Ukof78wEuAnHAcOV8uN8qkmoe4FxD6XRPUZ2lG9KT7NieJxxMNPkz48IhBxgjqD-57Apv1z0hbMpFlQVBa_xt5zGvLzZSOcswQCrn6d9w2CCAjHaY6xOAzHFpAPYoagXTWe9K3VqTPSueHvUNRqM08K5BX_fFFAaIYznUeXVTrUQ8rbKnl7OYMFWt8VKJCtATxGEgZFVOCk7GszNf8TkW2PlYKbgTFKGSs8N6-bKWZ-CDDUkhPiI_jaopcz67on0CdRV_o9NPdE-g'
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
    dir_script = 'TestUploadScript/delete_old_images.py'
    resp_upload_script = lkf_api.post_upload_script(dir_script, jwt_settings_key='USER_JWT_KEY')
    print('resp_upload_script =',resp_upload_script)
    if resp_upload_script.get('status_code') == 200:
        print('Script cargado')