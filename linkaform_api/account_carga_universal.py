# -*- coding: utf-8 -*-
import sys, simplejson
import settings, utils, carga_universal
# from account_settings import *


settings.mongo_hosts = 'dbs2.lkf.cloud:27918'
settings.mongo_port = 27918
settings.MONGODB_URI = 'mongodb://%s/'%(settings.mongo_hosts)
my_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpndmVsYW5kaWFAbGFiZ2VuY2VsbC5jb20iLCJ1c2VyX2lkIjoxNDIyNCwicGFyZW50X2lkIjoxNDIyNCwiaXNfbW9iaWxlIjpmYWxzZSwiZXhwIjoxNzAzMjcxMzk4LCJkZXZpY2Vfb3MiOiJ3ZWIiLCJlbWFpbCI6ImpndmVsYW5kaWFAbGFiZ2VuY2VsbC5jb20ifQ.ZVe0PHSzsVhwtwjgtiUcKpwL4OFmyYiJuezuY8Bz1IPN_UoVNcgkjpwQcuJuf4fVHA4YbMmOlufLCpc7oY_E9Gl1BXTXA-cZZaPdOwvCHbdbJeZXkNmBqBpxm2HOWsXuHE4uvqQhkKwkqT79XiZKAvasSKdsHbX4_SWdZiEx9AGCf7ts4W7DadL5RF78V1oNX5yW3wkrMb3lIuQZGKgWEnuR5J84vHRVgzUChOgyw8KiiDmujz-imZ_I5GuNVIBZ7cJUwkivni4cSdBbzTc-oWmTSu1lmzdDsPiiOJld0CZ3fIIxHGKxhPjFpIioM_fVhgUCOXUG-V9-cJdkAXbkBKC0NKvAsIoYVvUcXrNW4DSn7EY6vjXfw1zx9VdxLA3rR9amNTHmW1AyNFrjBwlUFpGM3aCSgm0YNlpDaADYyaJ6LBGTAqxQa1AWvmjeUWSjuBqqwMztohL37JnAywlaIHKUfBLyBqnET1RD3yoVwDrCo9RFgmOLi54B0fB0ig_VkZbING22aK4uexQ6vMxNS9Iv3qnQb0nnwXd_vARlh7aFmIb3yyFmHZYHzmWrIMT7PfXTs6DUdKFGTyRQpwUF-7p4Z4AAnIudR7wP2AA-nDJrZyZt8s-R_iEVIPMfcS7T5VFJ4fg0A-Q9__uExTbtLdeZVVwhn67shKeDIj_2c5M'
config = {
    'USERNAME' : 'jgvelandia@labgencell.com',
    'PASS' : '',
    'COLLECTION' : 'form_answer',
    'PROTOCOL' : 'https', #http or https
    'HOST' : 'preprod.linkaform.com',
    'MONGODB_PORT':settings.mongo_port,
    'MONGODB_HOST': settings.mongo_hosts,
    'MONGODB_USER': 'account_14224',
    'MONGODB_PASSWORD': 'b47f20a4da03c1b67ac7dc644dd4764422cc9d6c',
    'PORT' : settings.mongo_port,
    'USER_ID' : 14224,
    'ACCOUNT_ID' : 14224,
    'KEYS_POSITION' : {},
    'IS_USING_APIKEY' : False,
    'USE_JWT' : True,
    'JWT_KEY':'',
    'AUTHORIZATION_EMAIL_VALUE' : 'jgvelandia@labgencell.com',
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

    field_id_catalog = '6578c191580b5df09490f2e9'
    current_record = {
        'answers': {
            "5e32fbb498849f475cfbdca2": "cargar_documentos",
            "6578c191580b5df09490f2e9": {
                "5d810a982628de5556500d55": "Inventario de Equipos Biomédicos",
                "5d810a982628de5556500d56": [112591]
            },
            "5e32fae308a46b2ea5fbde86": {
                "file_name": "test_cu_api.xlsx",
                #"file_url": "https://f001.backblazeb2.com/file/slimey-linkaform/public-client-9908/95681/5e32fae308a46b2ea5fbde86/63ff73bbbb827baa38591eab.xlsx"
                #"file_url": "https://f001.backblazeb2.com/file/slimey-linkaform/public-client-9908/81339/5e32fae308a46b2ea5fbde86/6526f577a70ccc56337445b8.xlsx"
                "file_url": "https://f001.backblazeb2.com/file/app-linkaform/public-client-14224/112695/5e32fae308a46b2ea5fbde86/657b3686b9eea7facc0cad46.xlsx"
            }
        },
        'folio': '121816-9908',
        'form_id': 112695,
        '_id': {'$oid': '64d3a1a4296e3e93677705ff'}
    }

    lkf_api = utils.Cache(settings)
    # current_record = lkf_api.drop_fields_for_patch(current_record)
    record_id = current_record['_id']['$oid']
    class_cu = carga_universal.CargaUniversal(settings=settings, field_id_catalog_form=field_id_catalog)
    resp_cu = class_cu.carga_doctos(current_record, record_id)