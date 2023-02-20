# -*- coding: utf-8 -*-
import sys, simplejson
import settings, utils, carga_universal
# from account_settings import *


settings.mongo_hosts = 'dbs2.lkf.cloud:27918'
settings.mongo_port = 27918
settings.MONGODB_URI = 'mongodb://%s/'%(settings.mongo_hosts)
my_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImxpbmthZm9ybUBtYWdub2xpYWdhcmRlbnMuY29tIiwidXNlcl9pZCI6OTkwOCwicGFyZW50X2lkIjo5OTA4LCJpc19tb2JpbGUiOmZhbHNlLCJleHAiOjE2NzcxNjMzODgsImRldmljZV9vcyI6IndlYiIsImVtYWlsIjoibGlua2Fmb3JtQG1hZ25vbGlhZ2FyZGVucy5jb20ifQ.gj8cjJ2XvVsck1qKUDQ-tHjOFXQEc_Qa_PQWMG5GhNQ0-tb39qEekmdRfzR6rUo450mySXwZXx7oNYqA1BaXJoa3ygRHQFC5W5RKoXPEjSnqflh1YgHsb0F1siRkkUXvA104i83MFVwTtjQjwOty-0yJHjf2p-iPwzUFxz4silrZ75-QDgvpUuTd02EJtIBiuUV_W0DULDmuCs_1RZOMlKhITnv2yO_g466VB7d502UiaKFtNK19PmafIG2yDuVXsxmEUNx5P2vI4CRms28KL_uWYhbzlOhWqhebDMii6JCq6CZD5HwCIRtuXFD1aiPMqknGg_cz8Vbe77GrTgYhlkXHzY5EqItKcSgJSLrtS8ez-5ZXwGfs8Z92L5jTwPws2giMcpGFRcyGGmiQZw4lESznmA4Xc3mA7FHfV2Wewguadjxl30XBLpPEXPB4V74ZX1UVviaCiqSIp9A52mkHGF3PKogirPcYTMgMy34WUOMfuFAQZHKlSLx0i371m4TyvTpJG2Js9WMAXw8WRmmKJ4tYCZdBgny2euAMzmBETHeY0MfyUIEfudd9JSg0vmzBamP8kObeEqpB5AzBKzCa-cTwW2GICa4y98w8ATcgWkrNfk1xDaFNm4ys44riu57U3DWi5hrEx53LUb01jEQj6H_CGXUnNSEaIKaFCJLvX9E'
config = {
    'USERNAME' : 'linkaform@magnoliagardens.com',
    'PASS' : '',
    'COLLECTION' : 'form_answer',
    'PROTOCOL' : 'https', #http or https
    'HOST' : 'preprod.linkaform.com',
    'MONGODB_PORT':settings.mongo_port,
    'MONGODB_HOST': settings.mongo_hosts,
    'MONGODB_USER': 'account_9908',
    'MONGODB_PASSWORD': 'aa313a07e3c910c0b0400b954eea811dbcbef669',
    'PORT' : settings.mongo_port,
    'USER_ID' : 9908,
    'ACCOUNT_ID' : 9908,
    'KEYS_POSITION' : {},
    'IS_USING_APIKEY' : False,
    'USE_JWT' : True,
    'JWT_KEY':'',
    'AUTHORIZATION_EMAIL_VALUE' : 'linkaform@magnoliagardens.com',
    'AUTHORIZATION_TOKEN_VALUE' : '7d3bde3c53d7e189ed7dda80dad246de7f7e81a2',
    'API_KEY': 'e38ea1b666e739577e7c7c53abce771ae7ead028',
    'JWT_KEY': my_jwt,
    'USER_JWT_KEY': my_jwt
}

settings.config.update(config)


if __name__ == '__main__':
    '''
    current_record = simplejson.loads( sys.argv[1] )
    jwt_complete = simplejson.loads( sys.argv[2] )
    config['USER_JWT_KEY'] = jwt_complete["jwt"].split(' ')[1]
    settings.config.update(config)
    '''

    field_id_catalog = '620533fdef79040d965733fd'
    current_record = {
        'answers': {
            "5e32fbb498849f475cfbdca2": "cargar_documentos",
            "620533fdef79040d965733fd": {
                "5d810a982628de5556500d55": "Weekly Plantation Plan (green house)",
                "5d810a982628de5556500d56": [94878]
            },
            "5e32fae308a46b2ea5fbde86": {
                "file_name": "test_cu_api.xlsx",
                "file_url": "https://f001.backblazeb2.com/file/slimey-linkaform/public-client-9908/81339/5e32fae308a46b2ea5fbde86/63ee6bbd8dcecab96c7e76b2.xlsx"
            }
        },
        'folio': '119397-9908',
        'form_id': 81339,
        '_id': {'$oid': '63ee5c3da39bf4071a7e76a5'}
    }

    lkf_api = utils.Cache(settings)
    # current_record = lkf_api.drop_fields_for_patch(current_record)
    record_id = current_record['_id']['$oid']
    class_cu = carga_universal.CargaUniversal(settings=settings, field_id_catalog_form=field_id_catalog)
    resp_cu = class_cu.carga_doctos(current_record, record_id)