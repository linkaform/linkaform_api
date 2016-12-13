# coding: utf-8
#!/usr/bin/python


forms_url = {
    'form_answer': {'url':'https://www.linkaform.com/api/infosync/form_answer/', 'method':'GET'},
    'all_forms': {'url':'https://www.linkaform.com/api/infosync/item/', 'method':'GET'},
    'get_form_id_fields': {'url':'https://www.linkaform.com/api/infosync/get_form/?form_id=', 'method':'GET'},
    'set_form_answer': {'url':'https://www.linkaform.com/api/infosync/form_answer/', 'method':'POST'},
}

global_url ={
    'login': {'url':'https://www.linkaform.com/api/infosync/user_admin/login/', 'method':'POST'},
}

catalog_url = {
    'all_catalogs': {'url':'https://www.linkaform.com/api/infosync/catalog/', 'method':'GET'},
    'catalog_answer': {'url':'https://www.linkaform.com/api/infosync/catalog_answer/?catalog_id=', 'method':'GET'},
    'catalog_id_fields': {'url':'https://www.linkaform.com/api/infosync/catalog_data/?catalog_id=', 'method':'GET'},
    'set_catalog_answer': {'url':'https://www.linkaform.com/api/infosync/catalog_answer/', 'method':'POST'},
}

users_url = {
    'all_users': {'url':'https://www.linkaform.com/api/infosync/user_admin/', 'method':'GET'},
}

connections_url = {
    'all_connections': {'url':'https://www.linkaform.com/api/infosync/connection/', 'method':'GET'},
}

api_url = {}
api_url['form'] = forms_url
api_url['global'] = global_url
api_url['catalog'] = catalog_url
api_url['users'] = users_url
api_url['connecions'] = connections_url
