# -*- coding: utf-8 -*-
import sys, simplejson
import settings, utils, carga_universal
# from account_settings import *


settings.mongo_hosts = 'dbs2.lkf.cloud:27918'
settings.mongo_port = 27918
settings.MONGODB_URI = 'mongodb://%s/'%(settings.mongo_hosts)
my_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImxpbmthZm9ybUBtYWdub2xpYWdhcmRlbnMuY29tIiwidXNlcl9pZCI6OTkwOCwicGFyZW50X2lkIjo5OTA4LCJpc19tb2JpbGUiOmZhbHNlLCJleHAiOjE2OTc2NTY2MzEsImRldmljZV9vcyI6IndlYiIsImVtYWlsIjoibGlua2Fmb3JtQG1hZ25vbGlhZ2FyZGVucy5jb20ifQ.aDMEAAdmMqZZWHxtSdI9zHILM4gMJXef8DgeZsAkE0gR_JXslKacSWhAzjJAdVbzrphPzA9hF9YK8bwKyEqx5FV_yS8tu4_Zg7sx-8Kxt7irCyYTjVC2S9oleTBjVowkbLK5VDiUW5tWr8UDRa2ajVXNKlJMZs4aCBQnfRu771FVZrTNecNif5IbtbDPFAnLDtEnMgUw96fHpgvWoj3oO7QDfNcb1bQcyfP5KRtEOQRjccq3greIdJ7qZmmRdhuwrhDs4yKSViSEJEC05cEn2W3i2lvjroQjuf5XX_gD2k7u6O6OkoseaH8uHKqcqH9ynt3-ETCB6SbVN6K0Ur1fDl2QTmHwD7FxRAkXQCMJOh45aeU9eJYF4tzDGEJk7mfI9QnMgy0B_qzpXCeBuHSKeSdbRnpfAc-1bAsgUIYSgrZXI6DLz1p9QAsas8zHlsRsZWYdAT7HkVppteCDisZgoQXWz8ZxZhi8yKXmlfA4m9oXc1rzz9QZ2ko8sGoaPJB7GJZfdVPtLEb7-YqeZ7XaqlYRH1R9Ma8wsYF4u8DvuhHkizOySUBUx17jfedfQ618toFBHZSGgU_e9nNTS888qNLr67zCjeoPFWgM5mQipdvXgRvjzlnMez4Xh_TQVeeiEW6GWuV_0Im0D3tUltEenvHANHSI5Ehj_ynpbm0JL88'
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
                #"file_url": "https://f001.backblazeb2.com/file/slimey-linkaform/public-client-9908/95681/5e32fae308a46b2ea5fbde86/63ff73bbbb827baa38591eab.xlsx"
                "file_url": "https://f001.backblazeb2.com/file/slimey-linkaform/public-client-9908/81339/5e32fae308a46b2ea5fbde86/6526f577a70ccc56337445b8.xlsx"
            }
        },
        'folio': '121816-9908',
        'form_id': 81339,
        '_id': {'$oid': '64d3a1a4296e3e93677705ff'}
    }

    lkf_api = utils.Cache(settings)
    # current_record = lkf_api.drop_fields_for_patch(current_record)
    record_id = current_record['_id']['$oid']
    class_cu = carga_universal.CargaUniversal(settings=settings, field_id_catalog_form=field_id_catalog)
    resp_cu = class_cu.carga_doctos(current_record, record_id)