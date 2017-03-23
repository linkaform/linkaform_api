# coding: utf-8
#!/usr/bin/python

#linkaform api
import settings

#print settings
#print dir(settings)
dset_url =  settings.config['PROTOCOL'] + '://' + settings.config['HOST']

forms_url = {
    'form_answer': {'url': dset_url + '/api/infosync/form_answer/', 'method':'GET'},
    'all_forms': {'url': dset_url + '/api/infosync/item/', 'method':'GET'},
    'get_form_id_fields': {'url': dset_url + '/api/infosync/get_form/?form_id=', 'method':'GET'},
    'set_form_answer': {'url': dset_url + '/api/infosync/form_answer/', 'method':'POST'},
    'upload_file': {'url': dset_url + '/api/infosync/upload/', 'method':'POST'},
}

records_url = {
    'form_answer': {'url': dset_url + '/api/infosync/form_answer/', 'method':'GET'},
    'form_answer_patch': {'url': dset_url + '/api/infosync/form_answer/', 'method':'PATCH'},

}

global_url ={
    'login': {'url': dset_url + '/api/infosync/user_admin/login/', 'method':'POST'},
}

catalog_url = {
    'all_catalogs': {'url': dset_url + '/api/infosync/catalog/', 'method':'GET'},
    'catalog_answer': {'url': dset_url + '/api/infosync/catalog_answer/?catalog_id=', 'method':'GET'},
    'catalog_id_fields': {'url': dset_url + '/api/infosync/catalog_data/?catalog_id=', 'method':'GET'},
    'set_catalog_answer': {'url': dset_url + '/api/infosync/catalog_answer/', 'method':'POST'},
}

users_url = {
    'all_users': {'url': dset_url + '/api/infosync/user_admin/', 'method':'GET'},
}

connections_url = {
    'all_connections': {'url': dset_url + '/api/infosync/connection/', 'method':'GET'},
}

api_url = {}
api_url['form'] = forms_url
api_url['record'] = records_url
api_url['global'] = global_url
api_url['catalog'] = catalog_url
api_url['users'] = users_url
api_url['connecions'] = connections_url
