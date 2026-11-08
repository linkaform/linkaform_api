# coding: utf-8
#!/usr/bin/python


class Api_url:

    def __init__(self, settings):
        self.urls = {}
        # LKF
        self.dest_url = settings.config['PROTOCOL'] + '://' + settings.config['HOST']
        self.api_base = '{}/api/{}'.format(self.dest_url, self._api_product(settings))
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
        self.db_tools = self.get_db_tools()
        # AIRFLOW
        self.airflow_dest_url = settings.config['AIRFLOW_PROTOCOL'] + '://' + settings.config['AIRFLOW_HOST']
        if settings.config.get('AIRFLOW_PORT'):
            self.airflow_dest_url += ':{}'.format(settings.config['AIRFLOW_PORT'])
        self.airflow = self.get_airflow()
        self.bob_url = settings.config['PROTOCOL'] + '://' + settings.config['HOST']

    @staticmethod
    def _api_product(settings):
        # Prefijo /api/<producto>/ por cuenta, para que infra distinga el trafico de
        # Clave10. Sale del flag 'clave10' del config (account_settings.py en prod);
        # sin el flag queda /api/infosync. Las URIs dentro de los datos no cambian.
        if settings.config.get('clave10'):
            return 'clave10'
        return 'infosync'

    def get_airflow(self):
        return  {
            'update': {'url': self.airflow_dest_url + '/cron', 'method':'PATCH'},
            'subscribe': {'url': self.airflow_dest_url + '/cron', 'method':'POST'},
            'delete_schedule': {'url': self.airflow_dest_url + '/cron', 'method':'DELETE'},
            'run_dag': {'url': self.airflow_dest_url + '/cron/{0}', 'method':'POST'},
        }

    def get_catalog_url(self):
        return  {
            'catalog_id_fields': {'url': self.api_base + '/catalog_model/send_catalog/', 'method':'GET'},
            'catalog_answer_patch_multi': {'url': self.api_base + '/catalog_answers/update_catalogs/', 'method': 'PATCH'},
            'catalog_view': {'url': self.api_base + '/catalog/view/', 'method': 'POST'},
            'create_folder': {'url': self.api_base + '/catalog_folder/', 'method':'POST'},
            'create_catalog': {'url': self.api_base + '/catalog_model/', 'method':'POST'},
            'create_filter': {'url': self.api_base + '/user_properties/create_filter/', 'method': 'POST'},
            'delete_catalog_record': {'url': self.api_base + '/catalog/bulk_docs/', 'method': 'POST'},
            'delete_filter': {'url': self.api_base + '/catalog/delete_filter/', 'method': 'POST'},
            'download_catalog_model': {'url': self.api_base + '/catalog_model/download/', 'method':'GET'},
            'load_rows': {'url': self.api_base + '/catalog_answers/sheet_to_catalog/', 'method': 'POST'},
            'get_catalog_filters': {'url': self.api_base + '/catalog/get_catalog_filters/?catalog_id=', 'method': 'GET'},
            'get_record_by_folio': {'url': self.api_base + '/catalog/find/', 'method':'POST'},
            'set_catalog_answer': {'url': self.api_base + '/catalog_answers/', 'method':'POST'},
            'share_catalog': {'url': self.api_base + '/file_shared/', 'method': 'PATCH'},
            'sync_catalogs_records': {'url': self.api_base + '/catalog_answers/sync_catalogs_records/', 'method': 'POST'},
            'update_catalog_answer': {'url': self.api_base + '/catalog_answers/', 'method': 'PATCH'},
            'update_catalog_model': {'url': self.api_base + '/catalog_model/{0}/', 'method': 'PATCH'},
            'update_catalog_multi': {'url': self.api_base + '/catalog_answers/{}/', 'method': 'PATCH'},
        }

    def get_connections_url(self):
        return  {
            'all_connections': {'url': self.api_base + '/connection/', 'method':'GET'},
            'all_user_connection': {'url': self.api_base + '/user_connection/', 'method': 'GET'},
            'connection_by_id': {'url': self.api_base + '/connection/', 'method':'GET'},
            'form_connections': {'url': self.api_base + '/connection_record_filter/?form_id=', 'method':'GET'},
            'user_by_form' : {'url': self.api_base + '/file_shared/?form_id=&user_id=', 'method':'GET'},
            'user_connection': {'url': self.api_base + '/user_connection/load_user/?email=', 'method': 'GET'}
        }

    def get_forms_url(self):
        return {
            'all_forms': {'url': self.api_base + '/item/', 'method':'GET'},
            'download_form_data': {'url': self.api_base + '/form_data/download/', 'method':'GET'},
            'create_folder': {'url': self.api_base + '/folder/', 'method':'POST'},
            'create_form': {'url': self.api_base + '/form_data/', 'method':'POST'},
            'form_answer': {'url': self.api_base + '/form_answer/', 'method':'GET'},
            'get_folder_forms': {'url': self.api_base + '/item/?parent=', 'method':'GET'},
            'get_form_fields': {'url': self.api_base + '/get_form_fields/', 'method':'GET'},
            'get_form_id_fields': {'url': self.api_base + '/get_form/?form_id=', 'method':'GET'},
            'get_form_for_answer': {'url': self.api_base + '/get_form_for_answer/?form_id=', 'method':'GET'},
            'get_mobile_form': {'url': self.api_base + '/mobile_form/', 'method':'GET'},
            'get_inbox_forms': {'url': self.api_base + '/form/?id__in=', 'method':'GET'},
            'get_form_rules': {'url': self.api_base + '/form_rules/?form_id=', 'method':'GET'},
            'get_form_workflows': {'url': self.api_base + '/workflows/?form_id=', 'method':'GET'},
            'get_pdf_templates': {'url': self.api_base + '/templates/?form_id={}&filter_id=0&multiple_records=true', 'method':'GET'},
            'share_form': {'url': self.api_base + '/file_shared/', 'method': 'PATCH'},
            'set_form_answer': {'url': self.api_base + '/form_answer/', 'method':'POST'},
            'run_wf_action': {'url': self.api_base + '/workflow_action/execute_task/', 'method':'POST'},
            'unshare_item': {'url': self.api_base + '/file_shared/', 'method': 'PATCH'},
            'upload_file': {'url': self.api_base + '/cloud_upload/', 'method':'POST'},
            'upload_tmp': {'url': self.api_base + '/upload_tmp/', 'method':'POST'},
            'upload_rules': {'url': self.api_base + '/form_rules/', 'method':'POST'},
            'upload_workflows': {'url': self.api_base + '/workflows/', 'method':'POST'},
            'version': {'url': self.api_base + '/version/', 'method':'GET'},
        }

    def get_global_url(self):
        return {
            'login': {'url': self.api_base + '/user_admin/login/', 'method':'POST'},
            'db_password': {'url': self.api_base + '/user_admin/mongodb_pwd/', 'method':'GET'},
            'unlink_device': {'url': self.api_base + '/device/unlink_device/', 'method':'POST'},
        }

    def get_groups_url(self):
        return  {
            'create_group': {'url': self.api_base + '/group/', 'method':'POST'},
            'delete_group': {'url': self.api_base + '/group/{}/', 'method':'DELETE'},
            'edit_group': {'url': self.api_base + '/group/{}/', 'method':'PATCH'},
            'get_group_users': {'url': self.api_base + '/group/{}/', 'method':'GET'},
            'updated_groups': {'url': self.api_base + '/group/?limit=0&updated_at__gte={}/', 'method':'GET'},
        }

    def get_items_url(self):
        return {
            'delete_item': {'url': self.api_base + '/item/{}/', 'method':'DELETE'},
            'get_item': {'url': self.api_base + '/item/?id={}', 'method':'GET'},
            'move_item': {'url': self.api_base + '/item/move/', 'method':'POST'},
        }

    def get_records_url(self):
        return  {
            'form_answer': {'url': self.api_base + '/form_answer/', 'method':'GET'},
            'cdb_upload': {'url': self.api_base + '/cdb_upload/', 'method':'POST'},
            'form_answer_patch': {'url': self.api_base + '/form_answer/', 'method':'PATCH'},
            'form_answer_patch_multi': {'url': self.api_base + '/form_answer/update_records/', 'method':'PATCH'},
            'assigne_user':{'url': self.api_base + '/form_answer/assign_lead/', 'method':'POST'},
            'delete_inbox':{'url': self.api_base + '/device/delete_inbox/', 'method':'POST'},
            'assigne_connection': {'url': self.api_base + '/form_answer/assign_lead_connection/', 'method':'POST'},
            'get_record_pdf': {'url': self.api_base + '/form_answer/pdf/', 'method':'POST'},
            'get_pdf_multi_records': {'url': self.api_base + '/form_answer/records_pdf/', 'method':'POST'},
            'get_form_records_filter': {'url': self.api_base + '/form_answer/?filter_id={}&deleted=false&archived=false&limit={}&offset=0', 'method': 'GET'}
        }

    def get_report(self):
        return  {
            'create_folder': {'url': self.api_base + '/report_folder/', 'method':'POST'},
            'create_report': {'url': self.api_base + '/report/', 'method':'POST'},
            'update_report': {'url': self.api_base + '/report/{}/', 'method':'PATCH'},
        }

    def get_script(self):
        return  {
            'create_folder': {'url': self.api_base + '/script_folder/', 'method':'POST'},
            'run_script': {'url': self.api_base + '/scripts/run/', 'method':'POST'},
            'upload_script': {'url': self.api_base + '/upload_script/', 'method': 'POST'},
            'update_script': {'url': self.api_base + '/scripts/{}/', 'method': 'PATCH'},
            'share_script': {'url': self.api_base + '/file_shared/', 'method': 'PATCH'},
            'get_script_md5': {'url': self.api_base + '/scripts/{}/md5/', 'method': 'GET'},
        }

    def get_users_url(self):
        return  {
            'all_users': {'url': self.api_base + '/user_admin/?limit=0', 'method':'GET'},
            'activate_user': {'url': self.api_base + '/activate_user/', 'method':'POST'},
            'create_user': {'url': self.api_base + '/user_admin/', 'method':'POST'},
            'delete_inboxes': {'url': self.api_base + '/inbox/bulk_docs/', 'method':'POST'},
            'get_form_users' :{'url': self.api_base + '/item/{0}/get_users/?limit=0', 'method':'GET'},
            'get_user_catalog' :{'url': self.api_base + '/user_admin/{0}/catalogs/?limit=0', 'method':'GET'},
            'get_user_forms' :{'url': self.api_base + '/user_admin/{0}/forms/?limit=0', 'method':'GET'},
            'get_user_scripts': {'url': self.api_base + '/user_admin/{0}/scripts/?limit=0', 'method':'GET'},
            #'get_user_scripts': {'url': self.api_base + '/get_scripts/', 'method':'GET'},
            'get_licenses': {'url': self.api_base + '/licenses/?limit=0', 'method': 'GET'},
            'supervised_users': {'url': self.api_base + '/group/supervised_users/', 'method': 'GET'},
            'sms_creds': {'url': self.api_base + '/user_admin/sms_creds/', 'method':'GET'},
            'twilio_creds': {'url': self.api_base + '/user_admin/twilio_creds/', 'method':'GET'},
            'google_wallet': {'url': self.api_base + '/soter/google_wallet/', 'method':'GET'},
            'update_password': {'url': self.api_base + '/user_admin/{0}/', 'method': 'PATCH'},
            'updated_users' :{'url': self.api_base + '/user_admin/?limit=0&updated_at__gte={}', 'method':'GET'},
            'user_by_id': {'url': self.api_base + '/user_admin/', 'method':'GET'},
            #  Coincidencia EXACTA a proposito (sin __contains, como si lo usa
            #  user_id_by_email): 'ana' no debe matchear 'anabel'. El caller DEBE
            #  mandar el username ya validado (sin & # ? / = %): no hay urlencode.
            'user_by_username': {'url': self.api_base + '/user/?username={0}', 'method':'GET'},
            'user_id_by_email': {'url': self.api_base + '/user/?email__contains={0}', 'method':'GET'},
            'user_inbox': {'url': self.api_base + '/inbox/all_docs/', 'method': 'POST'},
        }

    def get_db_tools(self):
        return  {
            'create_couch_db': {'url': self.api_base + '/clave10_admin/create_db/', 'method':'POST'},
        }