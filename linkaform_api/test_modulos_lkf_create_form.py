# -*- coding: utf-8 -*-
# import sys, simplejson
# from linkaform_api import settings, network, utils
# from pci_settings import *
import settings
from utils import Cache

settings.mongo_hosts = 'dbs2.lkf.cloud:27918'
settings.mongo_port = 27918
settings.MONGODB_URI = 'mongodb://%s/'%(settings.mongo_hosts)
my_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImxpbmthZm9ybUBvcGVyYWNpb25wY2kuY29tLm14IiwidXNlcl9pZCI6MTQzMywicGFyZW50X2lkIjoxMjU5LCJpc19tb2JpbGUiOmZhbHNlLCJleHAiOjE2ODIzNjY2NTksImRldmljZV9vcyI6IndlYiIsImVtYWlsIjoibGlua2Fmb3JtQG9wZXJhY2lvbnBjaS5jb20ubXgifQ.I1Xg6ZQ77VY8tcBIpcjwUlf_oWq09EvRTsmxCfSq-VTAocV9NHXPkB_t5kQp1Qi6_ZAOP4Up-XXh_kY58-RivMc9VTMSKrf3mBA9WF26-6lXt0dnkPfvjs7eyeTXOPEupTLnxi372zYdHdDi2zlZ14Dt6bWFyeaYYpsBcbvXWt7xNQFAIdCpES65VIfQ4sJAFykCQhLLjUARK0VIhwEhCD1-sg6UtIRmz-w_5h9bRUd-nQ8bHyQTQbzNdseCdIAfKkJ8TQ1mbHrJ9cX83NIZPWL-nx0KnuJCQMmNIAI4jZjxlEaP-DOSzlVGs9swfkY0OJtsO308S7-Jpzd0t9dZh1Fq9gqZMWXixd9V30TXjQqs50o8FfnHNZlUPpK7bP6n3__lDWcB7Z6EtNUsAcnv9Blp4yko7-JyYHvlclm7ONpQgm7smYsLFzqZLA-KrKmCu4b7ZQfeMkKV4vmohlsh5GTATDySxyyB04G-RAUFGqCTccb3HzJg7Hqg5RVJVaz8gSn8OghdOJzPRmWiNmV9CF91tLotHLWNNcrhB--IelEqwC830AKgfQP1Sp3_f8xJ4n4Den2ruzJ1bNDc38aVFFuM-2pVwwkDHqUFBXUAaYabN95fsLp40ozQXzWqbczQ2qr-wEbp7Eyu3HojlDbtWZC3estFQfPJfJvYxT0NxcQ'
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