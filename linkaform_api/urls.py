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
        self.script = self.get_script()


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
            'upload_file': {'url': self.dest_url + '/api/infosync/cloud_upload/', 'method':'POST'},
            'get_form_fields':  {'url': self.dest_url + '/api/infosync/get_form_fields/', 'method':'GET'},
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
                'catalog_id_fields': {'url': self.dest_url + '/api/infosync/catalog_model/send_catalog/', 'method':'GET'},
                'set_catalog_answer': {'url': self.dest_url + '/api/infosync/catalog_answers/', 'method':'POST'},
                'get_record_by_folio': {'url': self.dest_url + '/api/infosync/catalog/find/', 'method':'POST'},
                'delete_catalog_record': {'url': self.dest_url + '/api/infosync/catalog/bulk_docs/', 'method': 'POST'},
                'get_record_by_folio': {'url': self.dest_url + '/api/infosync/catalog/find/', 'method':'POST'},
                'update_catalog_answer': {'url': self.dest_url + '/api/infosync/catalog_answers/', 'method': 'PATCH'},
                'delete_catalog_record': {'url': self.dest_url + '/api/infosync/catalog/bulk_docs/', 'method': 'POST'}

                }


    def get_users_url(self):
        return  {
                'all_users': {'url': self.dest_url + '/api/infosync/user_admin/', 'method':'GET'},
                'user_by_id': {'url': self.dest_url + '/api/infosync/user_admin/', 'method':'GET'},
                'get_form_users' :{'url': self.dest_url + '/api/infosync/item/{0}/get_users/?limit=0', 'method':'GET'},
                }


    def get_connections_url(self):
        return  {
                'all_connections': {'url': self.dest_url + '/api/infosync/connection/', 'method':'GET'},
                'connection_by_id': {'url': self.dest_url + '/api/infosync/connection/', 'method':'GET'},
                'form_connections': {'url': self.dest_url + '/api/infosync/connection_record_filter/?form_id=', 'method':'GET'},
                'user_by_form' : {'url': self.dest_url + '/api/infosync/file_shared/?form_id=&user_id=', 'method':'GET'},
                }

    def get_script(self):
        return  {
                'run_script': {'url': self.dest_url + '/api/infosync/scripts/run/', 'method':'POST'},
                }
