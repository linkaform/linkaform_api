# coding: utf-8
#!/usr/bin/python


class Api_url:

    def __init__(self, settings):
        self.urls = {}
        # LKF
        self.dest_url = settings.config['PROTOCOL'] + '://' + settings.config['HOST']
        self.catalog = self.get_catalog_url()
        self.connections = self.get_connections_url()
        self.form = self.get_forms_url()
        self.item = self.get_items_url()
        self.globals = self.get_global_url()
        self.groups = self.get_groups_url()
        self.record = self.get_records_url()
        self.report = self.get_report()
        self.script = self.get_script()
        self.users = self.get_users_url()
        # AIRFLOW
        self.airflow_dest_url = settings.config['AIRFLOW_PROTOCOL'] + '://' + settings.config['AIRFLOW_HOST']
        if settings.config.get('AIRFLOW_PORT'):
            self.airflow_dest_url += ':{}'.format(settings.config['AIRFLOW_PORT'])
        self.airflow = self.get_airflow()
        self.bob_url = settings.config['PROTOCOL'] + '://' + settings.config['HOST']

    def get_airflow(self):
        return  {
            'update': {'url': self.airflow_dest_url + '/cron', 'method':'PATCH'},
            'subscribe': {'url': self.airflow_dest_url + '/cron', 'method':'POST'},
            'delete_schedule': {'url': self.airflow_dest_url + '/cron', 'method':'DELETE'},
        }

    def get_catalog_url(self):
        return  {
            'catalog_id_fields': {'url': self.dest_url + '/api/infosync/catalog_model/send_catalog/', 'method':'GET'},
            'catalog_answer_patch_multi': {'url': self.dest_url + '/api/infosync/catalog_answers/update_catalogs/', 'method': 'PATCH'},
            'catalog_view': {'url': self.dest_url + '/api/infosync/catalog/view/', 'method': 'POST'},
            'create_folder': {'url': self.dest_url + '/api/infosync/catalog_folder/', 'method':'POST'},
            'create_catalog': {'url': self.dest_url + '/api/infosync/catalog_model/', 'method':'POST'},
            'create_filter': {'url': self.dest_url + '/api/infosync/user_properties/create_filter/', 'method': 'POST'},
            'delete_catalog_record': {'url': self.dest_url + '/api/infosync/catalog/bulk_docs/', 'method': 'POST'},
            'delete_filter': {'url': self.dest_url + '/api/infosync/catalog/delete_filter/', 'method': 'POST'},
            'download_catalog_model': {'url': self.dest_url + '/api/infosync/catalog_model/download/', 'method':'GET'},
            'load_rows': {'url': self.dest_url + '/api/infosync/catalog_answers/sheet_to_catalog/', 'method': 'POST'},
            'get_catalog_filters': {'url': self.dest_url + '/api/infosync/catalog/get_catalog_filters/?catalog_id=', 'method': 'GET'},
            'get_record_by_folio': {'url': self.dest_url + '/api/infosync/catalog/find/', 'method':'POST'},
            'set_catalog_answer': {'url': self.dest_url + '/api/infosync/catalog_answers/', 'method':'POST'},
            'share_catalog': {'url': self.dest_url + '/api/infosync/file_shared/', 'method': 'PATCH'},
            'update_catalog_answer': {'url': self.dest_url + '/api/infosync/catalog_answers/', 'method': 'PATCH'},
            'update_catalog_model': {'url': self.dest_url + '/api/infosync/catalog_model/{0}/', 'method': 'PATCH'},
            'update_catalog_multi': {'url': self.dest_url + '/api/infosync/catalog_answers/{}/', 'method': 'PATCH'},
        }

    def get_connections_url(self):
        return  {
            'all_connections': {'url': self.dest_url + '/api/infosync/connection/', 'method':'GET'},
            'all_user_connection': {'url': self.dest_url + '/api/infosync/user_connection/', 'method': 'GET'},
            'connection_by_id': {'url': self.dest_url + '/api/infosync/connection/', 'method':'GET'},
            'form_connections': {'url': self.dest_url + '/api/infosync/connection_record_filter/?form_id=', 'method':'GET'},
            'user_by_form' : {'url': self.dest_url + '/api/infosync/file_shared/?form_id=&user_id=', 'method':'GET'},
            'user_connection': {'url': self.dest_url + '/api/infosync/user_connection/load_user/?email=', 'method': 'GET'}
        }

    def get_forms_url(self):
        return {
            'all_forms': {'url': self.dest_url + '/api/infosync/item/', 'method':'GET'},
            'create_folder': {'url': self.dest_url + '/api/infosync/folder/', 'method':'POST'},
            'create_form': {'url': self.dest_url + '/api/infosync/form_data/', 'method':'POST'},
            'download_form_data': {'url': self.dest_url + '/api/infosync/form_data/download/', 'method':'GET'},
            'form_answer': {'url': self.dest_url + '/api/infosync/form_answer/', 'method':'GET'},
            'get_folder_forms': {'url': self.dest_url + '/api/infosync/item/?parent=', 'method':'GET'},
            'get_form_fields': {'url': self.dest_url + '/api/infosync/get_form_fields/', 'method':'GET'},
            'get_form_id_fields': {'url': self.dest_url + '/api/infosync/get_form/?form_id=', 'method':'GET'},
            'share_form': {'url': self.dest_url + '/api/infosync/file_shared/', 'method': 'PATCH'},
            'set_form_answer': {'url': self.dest_url + '/api/infosync/form_answer/', 'method':'POST'},
            'upload_file': {'url': self.dest_url + '/api/infosync/cloud_upload/', 'method':'POST'},
            'upload_tmp': {'url': self.dest_url + '/api/infosync/upload_tmp/', 'method':'POST'},
            'upload_rules': {'url': self.dest_url + '/api/infosync/form_rules/', 'method':'POST'},
            'upload_workflows': {'url': self.dest_url + '/api/infosync/workflows/', 'method':'POST'},
            'get_form_rules': {'url': self.dest_url + '/api/infosync/form_rules/?form_id=', 'method':'GET'},
            'get_form_workflows': {'url': self.dest_url + '/api/infosync/workflows/?form_id=', 'method':'GET'},
            'unshare_item': {'url': self.dest_url + '/api/infosync/file_shared/', 'method': 'PATCH'},
            'version': {'url': self.dest_url + '/api/infosync/version/', 'method':'GET'},
            'get_inbox_forms': {'url': self.dest_url + '/api/infosync/form/?id__in=', 'method':'GET'},
        }

    def get_global_url(self):
        return {
            'login': {'url': self.dest_url + '/api/infosync/user_admin/login/', 'method':'POST'},
            'db_password': {'url': self.dest_url + '/api/infosync/user_admin/mongodb_pwd/', 'method':'GET'},
            'unlink_device': {'url': self.dest_url + '/api/infosync/device/unlink_device/', 'method':'POST'},
        }

    def get_groups_url(self):
        return  {
            'create_group': {'url': self.dest_url + '/api/infosync/group/', 'method':'POST'},
            'delete_group': {'url': self.dest_url + '/api/infosync/group/{}/', 'method':'DELETE'},
            'edit_group': {'url': self.dest_url + '/api/infosync/group/{}/', 'method':'PATCH'},
            'get_group_users': {'url': self.dest_url + '/api/infosync/group/{}/', 'method':'GET'},
            'updated_groups': {'url': self.dest_url + '/api/infosync/group/?limit=0&updated_at__gte={}/', 'method':'GET'},
        }

    def get_items_url(self):
        return {
            'delete_item': {'url': self.dest_url + '/api/infosync/item/{}/', 'method':'DELETE'},
            'get_item': {'url': self.dest_url + '/api/infosync/item/?id={}', 'method':'GET'},
            'move_item': {'url': self.dest_url + '/api/infosync/item/move/', 'method':'POST'},
        }

    def get_records_url(self):
        return  {
            'form_answer': {'url': self.dest_url + '/api/infosync/form_answer/', 'method':'GET'},
            'cdb_upload': {'url': self.dest_url + '/api/infosync/cdb_upload/', 'method':'POST'},
            'form_answer_patch': {'url': self.dest_url + '/api/infosync/form_answer/', 'method':'PATCH'},
            'form_answer_patch_multi': {'url': self.dest_url + '/api/infosync/form_answer/update_records/', 'method':'PATCH'},
            'assigne_user':{'url': self.dest_url + '/api/infosync/form_answer/assign_lead/', 'method':'POST'},
            'delete_inbox':{'url': self.dest_url + '/api/infosync/device/delete_inbox/', 'method':'POST'},
            'assigne_connection': {'url': self.dest_url + '/api/infosync/form_answer/assign_lead_connection/', 'method':'POST'},
            'get_record_pdf': {'url': self.dest_url + '/api/infosync/form_answer/pdf/', 'method':'POST'},
            'get_pdf_multi_records': {'url': self.dest_url + '/api/infosync/form_answer/records_pdf/', 'method':'POST'},
            'get_form_records_filter': {'url': self.dest_url + '/api/infosync/form_answer/?filter_id={}&deleted=false&archived=false&limit={}&offset=0', 'method': 'GET'}
        }

    def get_report(self):
        return  {
            'create_folder': {'url': self.dest_url + '/api/infosync/report_folder/', 'method':'POST'},
            'create_report': {'url': self.dest_url + '/api/infosync/report/', 'method':'POST'},
            'update_report': {'url': self.dest_url + '/api/infosync/report/{}/', 'method':'PATCH'},
        }

    def get_script(self):
        return  {
            'create_folder': {'url': self.dest_url + '/api/infosync/script_folder/', 'method':'POST'},
            'run_script': {'url': self.dest_url + '/api/infosync/scripts/run/', 'method':'POST'},
            'upload_script': {'url': self.dest_url + '/api/infosync/upload_script/', 'method': 'POST'},
            'update_script': {'url': self.dest_url + '/api/infosync/scripts/{}/', 'method': 'PATCH'}
        }

    def get_users_url(self):
        return  {
            'all_users': {'url': self.dest_url + '/api/infosync/user_admin/?limit=0', 'method':'GET'},
            'create_user': {'url': self.dest_url + '/api/infosync/user_admin/', 'method':'POST'},
            'delete_inboxes': {'url': self.dest_url + '/api/infosync/inbox/bulk_docs/', 'method':'POST'},
            'get_form_users' :{'url': self.dest_url + '/api/infosync/item/{0}/get_users/?limit=0', 'method':'GET'},
            'get_licenses': {'url': self.dest_url + '/api/infosync/licenses/?limit=0', 'method': 'GET'},
            'supervised_users': {'url': self.dest_url + '/api/infosync/group/supervised_users/', 'method': 'GET'},
            'twilio_creds': {'url': self.dest_url + '/api/infosync/user_admin/twilio_creds/', 'method':'GET'},
            'updated_users' :{'url': self.dest_url + '/api/infosync/user_admin/?limit=0&updated_at__gte={}', 'method':'GET'},
            'user_by_id': {'url': self.dest_url + '/api/infosync/user_admin/', 'method':'GET'},
            'user_id_by_email': {'url': self.dest_url + '/api/infosync/user/?email__contains={0}', 'method':'GET'},
            'user_inbox': {'url': self.dest_url + '/api/infosync/inbox/all_docs/', 'method': 'POST'},
        }

