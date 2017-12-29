# coding: utf-8
#!/usr/bin/python


class Api_url:

    def __init__(self, settings):
        self.urls = {}
        self.dest_url = settings.config['PROTOCOL'] + '://' + settings.config['HOST']
        self.globals = self.get_global_url()
        self.form = self.get_forms_url()
        self.record = self.get_records_url()
        self.catalog = self.get_catalog_url()
        self.users = self.get_users_url()
        self.connecions = self.get_connections_url()


    def get_global_url(self):
        return {
        'login': {'url': self.dest_url + '/api/infosync/user_admin/login/', 'method':'POST'},
        }


    def get_forms_url(self):
        return {
            'form_answer': {'url': self.dest_url + '/api/infosync/form_answer/', 'method':'GET'},
            'all_forms':  {'url': self.dest_url + '/api/infosync/item/', 'method':'GET'},
            'get_form_id_fields':  {'url': self.dest_url + '/api/infosync/get_form/?form_id=', 'method':'GET'},
            'set_form_answer': {'url': self.dest_url + '/api/infosync/form_answer/', 'method':'POST'},
            'upload_file': {'url': self.dest_url + '/api/infosync/upload/', 'method':'POST'},
            }


    def get_records_url(self):
        return  {
                'form_answer': {'url': self.dest_url + '/api/infosync/form_answer/', 'method':'GET'},
                'form_answer_patch': {'url': self.dest_url + '/api/infosync/form_answer/', 'method':'PATCH'},
                'form_answer_patch_multi': {'url': self.dest_url + '/api/infosync/form_answer/update_records/', 'method':'PATCH'},
                'assigne_user':{'url': self.dest_url + '/api/infosync/form_answer/assign_lead/', 'method':'POST'},
                'assigne_connection': {'url': self.dest_url + '/api/infosync/form_answer/assign_lead_connection/', 'method':'POST'}
                }


    def get_catalog_url(self):
        return  {
                'all_catalogs': {'url': self.dest_url + '/api/infosync/catalog/', 'method':'GET'},
                'catalog_answer': {'url': self.dest_url + '/api/infosync/catalog_answer/?catalog_id=', 'method':'GET'},
                'catalog_id_fields': {'url': self.dest_url + '/api/infosync/catalog_data/?catalog_id=', 'method':'GET'},
                'set_catalog_answer': {'url': self.dest_url + '/api/infosync/catalog_answer/', 'method':'POST'},
                }


    def get_users_url(self):
        return  {
                'all_users': {'url': self.dest_url + '/api/infosync/user_admin/', 'method':'GET'},
                'user_by_id': {'url': self.dest_url + '/api/infosync/user_admin/', 'method':'GET'},
                }


    def get_connections_url(self):
        return  {
                'all_connections': {'url': self.dest_url + '/api/infosync/connection/', 'method':'GET'},
                'connection_by_id': {'url': self.dest_url + '/api/infosync/connection/', 'method':'GET'},
                'form_connections': {'url': self.dest_url + '/api/infosync/connection_record_filter/?form_id=', 'method':'GET'},
                'user_by_form' : {'url': self.dest_url + '/api/infosync/file_shared/?form_id=&user_id=', 'method':'GET'},
                }
