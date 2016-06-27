# coding: utf-8
#!/usr/bin/python



forms_url = {
    'form_answer': {'url':'https://bigbird.info-sync.com/api/infosync/form_answer/', 'method':'GET'},
    'all_forms': {'url':'https://bigbird.linkaform.com/api/infosync/item/', 'method':'GET'},
    'all_forms': {'url':'https://bigbird.linkaform.com/api/infosync/item/', 'method':'GET'}
}

global_url ={
    'login': {'url':'https://bigbird.info-sync.com/api/infosync/user_admin/login/', 'method':'POST'},
    'all_catalogs': {'url':'https://bigbird.linkaform.com/api/infosync/catalog/', 'method':'GET'},
    'get_catalog_id': {'url':'https://bigbird.info-sync.com/api/infosync/catalog_data/?catalog_id=', 'method':'GET'},
    'catalog_answer': {'url':'https://bigbird.info-sync.com/api/infosync/catalog_answer/', 'method':'GET'},
}

catalog_url = {
    'catalog_answer': {'url':'https://bigbird.info-sync.com/api/infosync/catalog_answer/', 'method':'GET'}
}

api_url = {}
api_url['form'] = forms_url
api_url['global'] = global_url
api_url['catalog'] = catalog_url
