# -*- coding: utf-8 -*-
import sys, simplejson
import settings, utils, carga_universal
# from account_settings import *


settings.mongo_hosts = 'dbs2.lkf.cloud:27918'
settings.mongo_port = 27918
settings.MONGODB_URI = 'mongodb://%s/'%(settings.mongo_hosts)
my_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImxpbmthZm9ybUBtYWdub2xpYWdhcmRlbnMuY29tIiwidXNlcl9pZCI6OTkwOCwicGFyZW50X2lkIjo5OTA4LCJpc19tb2JpbGUiOmZhbHNlLCJleHAiOjE2NzgyMzA2MDksImRldmljZV9vcyI6IndlYiIsImVtYWlsIjoibGlua2Fmb3JtQG1hZ25vbGlhZ2FyZGVucy5jb20ifQ.lJN9M_yC9fPs0Tw-YrYZsWEe_Zh_PGXu-PQ28PPYajII0geyYColmK9MwK5GXXJmqpYKPItArdLxmQVm0Wk26duFkViFiJqnJ3hGmDcwkIO6Sbacdxmcucl35qqkALiByCju1seg1Ad95bIdsoZiivPhKiYJzB8KqZelV_o8d8REJMXWofLtZ_2J9lLn8lsmKWhR05RtojiOYnpi1i-i7J4hPJpfTI6Ct2xSZA2-UUoAJoXJuy2yg3cZAb83_J47GWggcxXWJkptEfZi7QPikCoafYoovOk7m-EWOwbadTgy-X94L_TAsYtpMW0JPql7HSVMRaIHSO79QhdWAiHGC-HoosTeRtYo-o_27Pc5twJyq1oeI0FFI5tQEGVKhrnFxQ0kzyOso2NilRAS5HwcV1r66X6VnjfhvNnjZRUUNTwxPYsoXieamqmp1d0mzHVZm0lbrvVZyOqOYwz7lWCBlKAyjqha-DeonErOMSaRcKnuGsG6cvRwX3AQrv0jlOZlMAzPyUhE8iE1ogEDeyI6Q5T1KwFZ6gDhSWCZISbiL_i0Dq3tvLcRwOYgc63hKymruRxLNIS_cvh5q7pxTCWVAWtnVvdWfxw8c3JLqEWIy3W48aduPaSVt5WZOlhxsaLdXE95ImU1nyPoyubuBpM8_bbP9h78h_LH_st19QK16TA'
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
                "file_url": "https://f001.backblazeb2.com/file/slimey-linkaform/public-client-9908/95681/5e32fae308a46b2ea5fbde86/63ff73bbbb827baa38591eab.xlsx"
            }
        },
        'folio': '119807-9908',
        'form_id': 81339,
        '_id': {'$oid': '63fe87226a134635d9591e84'}
    }

    lkf_api = utils.Cache(settings)
    # current_record = lkf_api.drop_fields_for_patch(current_record)
    record_id = current_record['_id']['$oid']
    class_cu = carga_universal.CargaUniversal(settings=settings, field_id_catalog_form=field_id_catalog)
    resp_cu = class_cu.carga_doctos(current_record, record_id)