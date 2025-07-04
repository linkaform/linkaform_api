# coding: utf-8
#!/usr/bin/python

#Python Imports
import simplejson, time, concurrent.futures
import threading
import wget, bson
from math import ceil
from copy import deepcopy
#import concurrent.futures
#from forms import Form
from linkaform_api import network, lkf_object
from linkaform_api  import couch_util
from datetime import datetime
import pyexcel
import xml.etree.ElementTree as ET
import xml.dom.minidom
import hashlib
from twilio.rest import Client




# from ..models import LKFException

#Linkaform Imports
from . import network

class Cache:

    def __init__(self, settings):
        self.items = {}
        self.items_data = {}
        self.items_fields = {}
        self.settings = settings
        from linkaform_api import urls
        self.api_url = urls.Api_url(settings)
        self.network = network.Network(self.settings)
        if hasattr(self, 'couch'):
            self.couch = self.couch
        else:
            self.couch = couch_util.Couch_utils(self.settings)
        self.lkf_object = lkf_object.LKFBaseObject(id='', created_by={}, settings=self.settings)
        self.thread_dict = {}

    def check_delete(self):
        pass

    def assigne_user_records(self, user_id, record_id_list, send_email=False,
        send_push_notification=False, previos_user_id=False, jwt_settings_key=False):
        url_method = self.api_url.record['assigne_user']
        data = {'user_id': user_id, 'records': record_id_list,
                  'send_push_notification': send_push_notification,
                  'send_mail': send_email}
        if previos_user_id:
            data.update({'prev_user_id':previos_user_id})

        response = self.network.dispatch(url_method=url_method, data=data, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']

        return response

    def assigne_group_records(self, group_id, record_id_list, send_email=False,
        send_push_notification=True, previos_user_id=False, jwt_settings_key=False):
        url_method = self.api_url.record['assigne_user']
        data = {'group_id': group_id, 'records': record_id_list,
                  'send_push_notification': send_push_notification,
                  'from_api': True,
                  }
        if previos_user_id:
            data.update({'prev_user_id':previos_user_id})

        response = self.network.dispatch(url_method=url_method, data=data, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']

        return response

    def assigne_connection_records(self, connection_id, record_id_list, user_of_connection=False,
        send_email=False, send_push_notification=False, from_api=True, jwt_settings_key=False):
        url_method = self.api_url.record['assigne_connection']
        data = {'connection_id': connection_id, 'records': record_id_list,
                  'send_push_notification': send_push_notification,
                  'send_mail': send_email, 'from_api': from_api}
        if user_of_connection:
            data['userOfConnection'] = user_of_connection

        response = self.network.dispatch(url_method=url_method, data=data, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']

        return response

    def catalog_view(self, catalog_id, form_id, options={}, parent_catalog_id=None, jwt_settings_key=False):
        ''' Obtiene las vistas de los catalogos en un froma
        catalog_id: id del catalogo
        form_id: id de la foma
        options: Objetco con startkey, endkey y group_level
        parent_catalog_id: id del catalogo dependiente si llegase a existir
        '''
        if not options:
            options = {
                'startkey': [],
                'endkey': [],
                'group_level': 1,
            }
        group_level = options['group_level']
        url = self.api_url.catalog['catalog_view']['url']
        method = self.api_url.catalog['catalog_view']['method']
        data = {
            "catalog_id": catalog_id,
            "form_id": form_id,
            "options": options,
            "parent_catalog_id":parent_catalog_id,
        }
        response = self.network.dispatch(url=url, method=method, use_api_key=False, data=data, jwt_settings_key=jwt_settings_key)
        data = response.get('data',{})
        try:
            data = simplejson.loads(data)
        except:
            data = {}
        rows = data.get('rows',[])
        rows = [r.get('key')[group_level-1] for r in rows]
        return rows      

    def create_catalog(self, catalog_model, jwt_settings_key=False):
        url = self.api_url.catalog['create_catalog']['url']
        method = self.api_url.catalog['create_catalog']['method']
        return self.network.dispatch(url=url, method=method, data=catalog_model, use_api_key=False, jwt_settings_key=jwt_settings_key)

    def create_filter(self, catalog_id, filter_name, filter_to_search, filter_selected=None, jwt_settings_key=False):
        url = self.api_url.catalog['create_filter']['url']
        method = self.api_url.catalog['create_filter']['method']
        data_for_post = {
            "catalog_id": catalog_id,
            "filter": filter_to_search,
            "filter_name": filter_name,
            "filter_selected":filter_selected,
            "pageSize": 20
        }
        response = self.network.dispatch(url=url, method=method, use_api_key=False, data=data_for_post, jwt_settings_key=jwt_settings_key)
        return response

    def create_folder(self, folder_type, folder_name, jwt_settings_key=False):
        """
        Create any item folder, it could be on the forms list, catalog list, 
        script list or report list
        Args:
            folder_type (str): valid options are form, catalog, script or report
            folder_name(str): Any valid string, the / character will be consider as a folder route or path
        """
        if folder_type == 'form':
            url = self.api_url.form['create_folder']
        elif folder_type == 'catalog':
            url = self.api_url.catalog['create_folder']
        elif folder_type == 'script':
            url = self.api_url.script['create_folder']
        elif folder_type == 'report':
            url = self.api_url.report['create_folder']
        else:
            raise('{} is not a valid folder type, available options are: form, catalog, script or report')


        return self.network.dispatch(url, data={'name':folder_name}, jwt_settings_key=jwt_settings_key)

    def create_form(self, data, jwt_settings_key=False):
        url = '{}'.format(self.api_url.form['create_form']['url'])
        method = self.api_url.form['create_form']['method']
        return self.network.dispatch(url=url, method=method, data=data, jwt_settings_key=jwt_settings_key)

    def create_report(self, data, jwt_settings_key=False):
        url = '{}'.format(self.api_url.report['create_report']['url'])
        method = self.api_url.form['create_form']['method']
        return self.network.dispatch(url=url, method=method, data=data, jwt_settings_key=jwt_settings_key)

    def create_user(self, data, jwt_settings_key=False):
        #TODO UPDATE SELF.ITESM
        #Returns all the connections
        # {"first_name":"new","last_name":null,
        # "username":null,"email":"new@new.com",
        # "password":"123456","password2":"123456","position":"111","phone":1,"permissions":["add_form"]}
        url = self.api_url.users['create_user']['url']
        method = self.api_url.users['create_user']['method']
        user = self.network.dispatch(url=url, method=method, data=data, jwt_settings_key=jwt_settings_key)
        return user

    def delete_inbox_records(self, delete_records, jwt_settings_key=False):
        #  delete_records {user_id:[record_id,]}
        url_method = self.api_url.record['delete_inbox']
        data = {'delete_records': delete_records}
        response = self.network.dispatch(url_method=url_method, data=data, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']
        return response

    def delete_users_inbox_thread_function(self, url_method, inboxes, jwt_settings_key=False):
        print('stop', url_method)
        print('inbox=', inboxes)
        response = self.network.dispatch(url_method=url_method, data=inboxes, jwt_settings_key=jwt_settings_key)
        if response.get('data'):
            records_updated = response['data']
            if isinstance(records_updated, str):
                records_updated = simplejson.loads(records_updated)
        return response 

    def delete_inbox_format(self, inboxes):
        res = []
        for inbox in inboxes:
            r = {
                '_id': inbox.get('id',inbox.get('_id',inbox.get('key'))), 
                '_deleted': True
            }
            revision = inbox.get('_rev',inbox.get('value',{}).get('rev'))
            if revision:
                r.update({'_rev':revision})
            res.append(r)
        return res

    def delete_users_inbox(self, user_id, inboxes, threading=False, jwt_settings_key=False):
        #DETELES the users inbox
        #params:
        # inboxes: list of dicts of users inbox
        url_method = self.api_url.users['delete_inboxes']
        data = {
            "inbox_records": self.delete_inbox_format(inboxes),
            "user_id":user_id
            }

        if threading:
            with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
                usr_data = []
                records_updated = {}
                for inbox in inboxes:
                    user_data = {
                       "user_id": user_id,
                       "inbox_records": {usr_id:self.delete_inbox_format(inbox)},
                    }
                    usr_data.append(user_data)
                print('doning this many post', len(usr_data))
                to_multi_patch = [executor.submit(
                    self.delete_users_inbox_thread_function, url_method, u_data, jwt_settings_key=jwt_settings_key) 
                    for u_data in usr_data]
                for thread_post in concurrent.futures.as_completed(to_multi_patch):
                    resp = thread_post.result()
                    resp_objects = resp.get('data', {})
                    if isinstance(resp_objects, str):
                        res = simplejson.loads(resp_objects)
                        records_updated.update(res)
        else:
            records_updated = self.delete_users_inbox_thread_function(url_method, data, jwt_settings_key=jwt_settings_key)
        return records_updated

    def delete_form_records(self, delete_record_ids, jwt_settings_key=False):
        data = {'deleted_objects':[]}
        url = self.api_url.record['form_answer_patch']['url'] 
        url = url.replace(self.api_url.dest_url, '')
        if isinstance(delete_record_ids ,list):
            data['deleted_objects'] = [f"{url}{x}/" for x in delete_record_ids]
        else:
            data['deleted_objects'] = [f"{url}{delete_record_ids}/",]
        print('DELETEING RECORDS=', data)
        return self.patch_record(data, jwt_settings_key=jwt_settings_key)

    def drop_fields_for_patch(self, record):
        fields_to_drop = ['end_date','editable','updated_at','duration','index',
                        'created_at', 'version', 'start_date', 'updated_by','voucher' ,
                        'voucher_id','connection_record_id','other_versions','mobile_record_id']
        for field in fields_to_drop:
            try:
                record.pop(field)
            except KeyError:
                pass

        return record

    def ftp_upload(self, server, username, password, file_name, file_path):
        import ftplib
        session = ftplib.FTP(server, username, password)
        file = open(file_path,'rb')
        session.storbinary('STOR {}'.format(file_name), file)
        file.close()
        session.quit()
        return True

    def get(self, item_type, item_id):
        if not self.items.get(item_type):
            #self.items[item_type] = self.get_all_items(item_type)
            self.items[item_type] = {}
        if not self.items[item_type].get(item_id):
            self.items[item_type][item_id] = self.get_item_id(item_type, item_id)
        return self.items[item_type][item_id]

    def get_last_version(self, last_version_uri, answers_only=True, jwt_settings_key=False):
        if type(last_version_uri) == dict:
            uri = last_version_uri.get('uri')
        else:
            uri = last_version_uri

        url = self.api_url.dest_url +  uri
        method = self.api_url.form['version']['method']

        response = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)

        if response['status_code'] == 200:
            if answers_only:
                return response['data'].get('answers')
            return response['data']
        return False

    def get_data(self, item_type, item_id, refresh=False):
        if not self.items_data.get(item_type):
            self.items_data[item_type] = {}
        if not self.items_data[item_type].get(item_id):
            self.items_data[item_type][item_id] = self.get_item_answer(item_type, item_id)
        return self.items_data[item_type][item_id]

    def get_user_inbox_thread_function(self, url_method, data, jwt_settings_key):
        response = self.network.dispatch(url_method=url_method, data=data, jwt_settings_key=jwt_settings_key)
        # self.thread_dict[record] = res
        return response
        #logging.info("Finishing with code"%(record, res))

    def get_user_inbox(self, users=[], group_id=None, is_group=False, threading=False, jwt_settings_key=False):
        #Gets the users inbox
        #params:
        # users: list of users
        # group_id: is send will get the group inbox
        # is_group: boolean 
        url_method = self.api_url.users['user_inbox']
        data = {
            "users":users,
            "group_id":group_id,
            "is_group":is_group}
        if threading:
            with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
                usr_data = []
                records_updated = {}
                for usr in data['users']:
                    user_data = {
                       "users": [usr,],
                        "group_id":group_id,
                        "is_group":is_group
                    }
                    usr_data.append(user_data)
                to_multi_patch = [executor.submit(
                    self.get_user_inbox_thread_function, url_method, u_data, jwt_settings_key=jwt_settings_key) 
                    for u_data in usr_data]
                for thread_post in concurrent.futures.as_completed(to_multi_patch):
                    resp = thread_post.result()
                    resp_objects = resp.get('data', {})
                    if isinstance(resp_objects, str):
                        res = simplejson.loads(resp_objects)
                        records_updated.update(res)
            return records_updated
        else:
            response = self.network.dispatch(url_method=url_method, data=data, jwt_settings_key=jwt_settings_key)
            if response.get('data'):
                res = response['data']
                if isinstance(res, str):
                    records_updated = simplejson.loads(res)
        return records_updated

    def get_item_fields(self, item_type, item_id, refresh=False):
        if not self.items_fields.get(item_type):
            self.items_fields[item_type] = {}
        if not self.items_fields[item_type].get(item_id):
            self.items_fields[item_type][item_id] = self.get_item_fields(item_type, item_id)
        return self.items_fields[item_type][item_id]

    def get_item_answer(self, item_type, item_id, jwt_settings_key=False):
        if item_type =='form':
            url = self.api_url.form['form_answer']['url'] + str(item_id)
            method = self.api_url.form['form_answer']['method']
        if item_type =='catalog':
            url = self.api_url['catalog']['catalog_answer']['url'] + str(item_id)
            method = self.api_url['catalog']['catalog_answer']['method']
        response = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']
        return False

    def get_item_fields(self, item_type, item_id, jwt_settings_key=False):
        if item_type =='form':
            url = self.api_url.form['get_form_id_fields']['url'] + str(item_id)
            method = self.api_url.form['get_form_id_fields']['method']
        if item_type =='catalog':
            url = self.api_url['catalog']['catalog_id_fields']['url'] + str(item_id)
            method = self.api_url['catalog']['catalog_id_fields']['method']
        response = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']
        return False

    def get_form_id_fields(self, form_id, jwt_settings_key=False):
        url = self.api_url.form['get_form_id_fields']['url']+str(form_id)
        method = self.api_url.form['get_form_id_fields']['method']
        response = self.network.dispatch(url=url, method=method, use_api_key=False, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']
        return False

    def get_folder_forms(self, folder_id, jwt_settings_key=False):
        url = self.api_url.form['get_folder_forms']['url']+str(folder_id)
        method = self.api_url.form['get_folder_forms']['method']
        response = self.network.dispatch(url=url, method=method, use_api_key=False, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']
        return False

    def get_all_items(self, item_type, jwt_settings_key=False):
        if item_type =='form':
            return self.get_all_forms()
        if item_type == 'catalog':
            return self.get_all_catalogs()

    def get_item_id(self, item_type, item_id, jwt_settings_key=False):
        if item_type =='form':
            url = self.api_url.form['get_form_id']['url'] + str(item_id)
            method = self.api_url.form['get_form_id']['method']
        if item_type =='catalog':
            url = self.api_url['catalog']['get_catalog_id']['url'] + str(item_id)
            method = self.api_url['catalog']['get_catalog_id']['method']
        response = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        return response

    def get_all_forms(self, use_jwt=False, jwt_settings_key=False):
        #TODO UPDATE SELF.ITESM
        #recives the url name on the config file,GET_FORMS or GET_CATALOGS
        items = []
        if use_jwt:
            all_items = self.network.dispatch(self.api_url.form['all_forms'], use_jwt=use_jwt, jwt_settings_key=jwt_settings_key)
        all_items = self.network.dispatch(self.api_url.form['all_forms'], jwt_settings_key=jwt_settings_key)
        objects = all_items['data']
        for obj in objects:
            if obj['itype'] == 'form':# or obj['itype'] == 'catalog':
                    items.append(obj)
        return items

    def get_mobile_form(self, jwt_settings_key=False):
        url = self.api_url.form['get_mobile_form']['url']
        method = self.api_url.form['get_mobile_form']['method']
        response = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        return response

    def get_all_connections(self, jwt_settings_key=False):
        #TODO UPDATE SELF.ITESM
        #Returns all the connections
        connections = []
        all_connections = self.network.dispatch(self.api_url.connections['all_connections'], jwt_settings_key=jwt_settings_key)
        objects = all_connections['data']
        return objects

    def get_user_twilio_creds(self, use_api_key=False, jwt_settings_key=False):
        post_json = self.api_url.get_users_url()['twilio_creds']
        url = post_json['url']
        return self.network.dispatch(url=url, method=post_json['method'], use_api_key=use_api_key,  jwt_settings_key=jwt_settings_key)

    def get_user_google_wallet(self, use_api_key=False, jwt_settings_key=False):
        post_json = self.api_url.get_users_url()['google_wallet']
        url = post_json['url']
        return self.network.dispatch(url=url, method=post_json['method'], use_api_key=use_api_key,  jwt_settings_key=jwt_settings_key)

    def get_user_by_email(self, user_email, jwt_settings_key=False):
        post_json = self.api_url.get_users_url()['user_id_by_email']
        url = post_json['url'].format(user_email)
        response = self.network.dispatch(url=url, method=post_json['method'], jwt_settings_key=jwt_settings_key)
        all_users = response.get('objects', [])
        if not all_users:
            all_users = response.get('json',{}).get('objects', [])
        return all_users

    def get_updated_users(self, date_epoc, jwt_settings_key=False):
        post_json = self.api_url.get_users_url()['updated_users']
        url = post_json['url'].format(date_epoc)
        response = self.network.dispatch(url=url, method=post_json['method'], jwt_settings_key=jwt_settings_key)
        all_users = response.get('objects', [])
        if not all_users:
            all_users = response.get('json',{}).get('objects', [])
        return all_users

    def get_form_users(self, form_id, include_users=True, include_connections=True, include_owner=True,
        is_catalog=False, jwt_settings_key=False, format_response=True):
        #Returns all the form usrs... by default includes users and connections
        connections = []
        post_json = self.api_url.get_users_url()['get_form_users']
        url = post_json['url'].format(form_id)
        response = self.network.dispatch(url=url, method=post_json['method'], jwt_settings_key=jwt_settings_key)

        if is_catalog:
            return response

        if format_response:
            all_form_users = response.get('data', [])
            if type(all_form_users) == dict:
                all_form_users = [all_form_users,]

            if include_connections == False:
                [all_form_users.pop(pos) for pos, user in enumerate(all_form_users) if user['is_connection']]

            if include_users == False:
                [all_form_users.pop(pos) for pos, user in enumerate(all_form_users) if not user['is_connection']]

            if include_owner:
                all_form_users.append(response.get('json',{}).get('owner', {}))
        else:
            all_form_users = response

        return all_form_users

    def get_md5hash(self, file_name):
        try:
            md5 = hashlib.md5(open(file_name,'rb').read()).hexdigest()
        except FileNotFoundError:
            md5 = None
        return md5

    def get_jwt(self, user=None, password=None, get_jwt=True, api_key=None, get_user=False):
        session = False
        if not user:
            user = self.settings.config.get('USERNAME',self.settings.config.get('AUTHORIZATION_EMAIL_VALUE'))
        if not password:
            password = self.settings.config.get('PASS')
        if api_key:
            if type(api_key) == bool:
                api_key = self.settings.config.get('api_key')
            jwt = self.network.login(session, username=user, get_jwt=get_jwt, api_key=api_key, get_user=get_user)
        else:
            jwt = self.network.login(session, user, password, get_jwt=get_jwt, get_user=get_user)
        return jwt

    def get_pdf_record(self, record_id, template_id=None, upload_data=None, send_url=False, name_pdf='', jwt_settings_key=False):
        return self.network.pdf_record(record_id , template_id=template_id, upload_data=upload_data, send_url=send_url, name_pdf=name_pdf, jwt_settings_key=jwt_settings_key)

    def get_item(self, item_id, item_type=None, jwt_settings_key=False):
        # Delete an item
        url = self.api_url.item['get_item']['url'].format(item_id)
        url += '&itype__exact={}'.format(item_type)
        method = self.api_url.item['get_item']['method']
        return self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)

    def get_records_by_filter(self, filter_id, limit=20, jwt_settings_key=False):
        url = self.api_url.record['get_form_records_filter']['url'].format(filter_id, limit)
        method = self.api_url.record['get_form_records_filter']['method']
        records = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        objects = records['data']
        return objects

    def get_group_users(self, group_id, user_type='users', jwt_settings_key=False):
        #Returns all users of a group
        #user_type 'users', 'admin_users','supervisor_users'
        post_json = self.api_url.get_groups_url()['get_group_users']
        url = post_json['url'].format(group_id)
        response = self.network.dispatch(url=url, method=post_json['method'], jwt_settings_key=jwt_settings_key)
        if user_type in ('users', 'admin_users','supervisor_users'):
            return response.get('data', {}).get(user_type,[])
        else:
            return response.get('data', {})

    def get_updated_groups(self, date_epoc, jwt_settings_key=False):
        post_json = self.api_url.get_groups_url()['updated_groups']
        url = post_json['url'].format(date_epoc)
        response = self.network.dispatch(url=url, method=post_json['method'], jwt_settings_key=jwt_settings_key)
        all_groups = response.get('objects', [])
        if not all_groups:
            all_groups = response.get('json',{}).get('objects', [])
        return all_groups

    def get_form_workflows(self, form_id, jwt_settings_key=False):
        url = self.api_url.form['get_form_workflows']['url']+str(form_id)
        method = self.api_url.form['get_form_workflows']['method']
        response = self.network.dispatch(url=url, method=method, use_api_key=False, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']
        return False

    def get_form_to_duplicate(self, form_id, jwt_settings_key=False):
        form_with_fields = self.get_form_id_fields(form_id, jwt_settings_key=jwt_settings_key)
        if form_with_fields:
            dict_form = form_with_fields[0]
            dict_form.pop('form_id')
            dict_form.pop('fields')
            return dict_form

    def get_form_connections(self, form_id, jwt_settings_key=False):
        #TODO UPDATE SELF.ITESM
        #Returns all the connections
        connections = []
        post_json = self.api_url.get_connections_url()['form_connections']
        post_json['url'] = post_json['url'] + str(form_id)
        form_connections = self.network.dispatch(post_json, jwt_settings_key=jwt_settings_key)
        objects = form_connections['data']
        return objects

    def get_connection_by_id(self, connection_id, jwt_settings_key=False):
        #TODO UPDATE SELF.ITESM
        #Returns the connections info
        url = self.api_url.connecions['connection_by_id']['url'] + str(connection_id) + '/'
        method = self.api_url.connecions['connection_by_id']['method']
        connection = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        objects = connection['data']
        return objects

    def get_all_users(self, jwt_settings_key=False):
        all_users = self.network.dispatch(self.api_url.users['all_users'], jwt_settings_key=jwt_settings_key)
        objects = all_users['data']
        return objects

    def get_user_by_id(self, user_id, jwt_settings_key=False):
        #TODO UPDATE SELF.ITESM
        #Returns all the connections
        connections = []
        url = self.api_url.users['user_by_id']['url'] + str(user_id) + '/'
        method = self.api_url.users['user_by_id']['method']
        user = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        objects = user['data']
        return objects

    def get_licences(self, jwt_settings_key=False):
        url = self.api_url.users['get_licenses']['url']
        method = self.api_url.users['get_licenses']['method']
        licenses = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        return licenses['data']

    def get_from_fields(self, form_id, jwt_settings_key=False):
        url = self.api_url.form['get_form_fields']['url'] + str(form_id) + '/'
        method = self.api_url.form['get_form_fields']['method']
        fields =  self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        objects = fields['data']
        return objects

    def get_form_for_answer(self, form_id, jwt_settings_key=False):
        url = self.api_url.form['get_form_for_answer']['url'] + str(form_id) + '/'
        method = self.api_url.form['get_form_for_answer']['method']
        fields =  self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        objects = fields['data']
        return objects

    def get_user_fileshare(self, form_id, user_id, jwt_settings_key=False):
        url_list = self.api_url.connecions['user_fileshare']['url'].split('&')
        url = url_list[0] + str(form_id)
        url += '&' + url_list[1] + str(user_id)
        method = self.api_url.form['user_fileshare']['method']
        response = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        return response

    def get_user_forms(self, user_id, jwt_settings_key=False):
        """
        Regresa todas las formas que el usuario tiene compartidas
        """
        url = self.api_url.users['get_user_forms']['url'].format(user_id)
        method = self.api_url.users['get_user_forms']['method']
        response = self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)
        return response

    def get_record_answer(self, params = {}, jwt_settings_key=False):
        if not params:
            params = {'limit':20,'offset':0}
        response = self.network.dispatch(self.api_url.record['form_answer'], params=params, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']
        return False

    def get_metadata(self, form_id=False, user_id=False):
        time_started = time.time()
        metadata = {
            "form_id" : form_id,
            "geolocation": [-100.3862645,25.644885499999997],
            "geolocation_method":{"method": "HTML5", "accuracy": 0},
            "start_timestamp" : time.time(),
            "end_timestamp" : time.time(),
        }
        if user_id:
            metadata['user_id'] = int(user_id)
        if not form_id:
            metadata.pop('form_id')
        return metadata

    def get_form_rules(self, form_id, jwt_settings_key=False):
        url = self.api_url.form['get_form_rules']['url']+str(form_id)
        method = self.api_url.form['get_form_rules']['method']
        response = self.network.dispatch(url=url, method=method, use_api_key=False, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']
        return False

    def guess(self, value, answer):
        count = last_find = valuation = 0
        was_int = False
        org_value = value
        if type(answer) == int:
            was_int = True
            answer = str(answer)
        for letter in answer:
            index = value.find(letter)
            if index >= 0:
                count+=1
                if index == last_find:
                    count = count * 2
                    if was_int and index == 0:
                        count = count + 3
                value = value[:index] + value[index+1:]
                last_find = index
        return (count, org_value)

    def get_catalog_id_fields(self, catalog_id, jwt_settings_key=False):
        url = self.api_url.catalog['catalog_id_fields']['url']+str(catalog_id)+'/'
        method = self.api_url.catalog['catalog_id_fields']['method']
        response = self.network.dispatch(url=url, method=method, use_api_key=False, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return response['data']
        return False

    def get_catalog_metadata(self, catalog_id=False):
        time_started = time.time()
        metadata = {
        "catalog_id": catalog_id,
        "geolocation": [],
        "start_timestamp" : time.time(),
        "end_timestamp" : time.time()
        }
        if not catalog_id:
            metadata.pop('catalog_id')
        return metadata

    def get_catalog_record_by_folio(self, catalog_id, catalog_folio, jwt_settings_key=False):
        mango = {
            'selector':{
                '$and':[{'_id':{'$eq':catalog_folio}}]
            }
        }
        return self.search_catalog(catalog_id, mango, jwt_settings_key=jwt_settings_key)

    def get_exchange_rate(self, type_currency='USD', from_date='', jwt_settings_key=False):
        if not from_date:
            current_date = datetime.now()
            from_date = datetime.strftime(current_date, '%Y-%m-%d')
        mango_query = {
            "selector":{"answers": {"$and":[ 
                {"645545b5738f34f5a955e4ce": {'$eq': type_currency}},
                {"645545b5738f34f5a955e4cf": {"$lte": from_date}}
            ]}},
            "limit":10000,
            "skip":0,
            #"sort":[{"645545b5738f34f5a955e4cf": "desc"}]
        }
        record_found = self.search_catalog(100534, mango_query, jwt_settings_key=jwt_settings_key)
        if record_found:
            record_found.sort(key=lambda x: x.get("645545b5738f34f5a955e4cf"), reverse=True)
            return record_found[0]
        return record_found

    def get_catalog_filters(self, catalog_id, jwt_settings_key=False):
        url = self.api_url.catalog['get_catalog_filters']['url'] + str(catalog_id)
        method = self.api_url.catalog['get_catalog_filters']['method']
        response = self.network.dispatch(url=url, method=method, use_api_key=False, jwt_settings_key=jwt_settings_key)
        return response

    def get_records(self, catalog_db, rec_ids, batch_size):
        mango_query = {
            "selector": {
                "_id": {
                    "$in": rec_ids
                    }
                },
            "limit":batch_size+1
            }
        result = catalog_db.find(mango_query)
        res = [x for x in result]
        return res

    def get_last_seq(self, db_cr, catalog_from):
        mango_query = {
            "selector": {
                "_id": "last_seq_{}".format(catalog_from)
                },
            "limit":1
        }
        result = db_cr.find(mango_query)
        res = [x for x in result]
        return res

    def get_all_user_connection(self, email_user, jwt_settings_key=False):
        # Returns all users and connections
        connections = []
        url_data = self.api_url.get_connections_url()['all_user_connection']
        url_data['url'] = '{}?data={}'.format(url_data['url'], email_user)
        response = self.network.dispatch(url_data, jwt_settings_key=jwt_settings_key)

        return response

    def get_supervised_users(self, jwt_settings_key=False):
        url_data = self.api_url.get_users_url()['supervised_users']
        url = url_data['url']
        res =  self.network.dispatch(url=url, method=url_data['method'], jwt_settings_key=jwt_settings_key)
        if res.get('data'):
            return res['data']
        return res

    def get_user_connection(self, email_user, jwt_settings_key=False):
        # TODO UPDATE SELF.ITESM
        # Returns a user or connection
        connections = []
        post_json = self.api_url.get_connections_url()['user_connection']
        post_json['url'] = '{}{}'.format(post_json['url'], email_user)
        user_connection = self.network.dispatch(post_json, jwt_settings_key=jwt_settings_key)
        objects = user_connection['data']

        return objects

    def make_excel_file(self, header, records, form_id, file_field_id, upload_name=None, jwt_settings_key='JWT_KEY', is_tmp=False):
        records.insert(0, header)
        #rows = make_array(orders)
        date = time.strftime('%Y_%m_%d_%H_%M_%S')
        if not upload_name:
            upload_name = 'file_' + date
        file_name = '/tmp/output_{}.xlsx'.format(date)

        pyexcel.save_as(array=records, dest_file_name=file_name)
        #os_file_name = self.make_excel_file(record_errors)
        csv_file = open(file_name,'rb')
        csv_file_dir = {'File': csv_file}

        if is_tmp:
            upload_data = {'file_name': file_name}
            upload_url = self.post_upload_tmp(data=upload_data, up_file=csv_file_dir, jwt_settings_key=jwt_settings_key)
            try:
                file_url = upload_url['json'][0]['file_url']
                data = {'file_url': file_url}
            except KeyError:
                pass
        else:
            upload_data = {'form_id': form_id, 'field_id': file_field_id}
            upload_url = self.post_upload_file(data=upload_data, up_file=csv_file_dir, jwt_settings_key=jwt_settings_key)
            try:
                file_url = upload_url['data']['file']
                data = {file_field_id: {'file_name':'{}.xlsx'.format(upload_name), 'file_url':file_url}}
            except KeyError:
                pass

        csv_file.close()

        return data

    def make_infosync_select_json(self, answer, element, best_effort=False):
        if type(answer) != str:
                answer = str(answer)
        try:
            answer = answer.decode('utf-8')
        except Exception as e:
            pass

        if element.get('options') and  element.get('options'):
            options = element['options']
            default = False
            best_guess = (0,0)
            for opt in options:
                if answer == opt['value']:
                    return opt['value']
                if answer.lower().replace(' ', '_') == opt['value']:
                    return opt['value']
                elif answer == opt['label']:
                    return opt['value']
                elif opt.get('selected') and opt['selected']:
                    default = opt['value']
                elif opt.get('default') and opt['default']:
                    default = opt['value']
                if best_effort:
                    best_guess_opt = self.guess(opt['value'], answer)
                    if best_guess_opt[0] > best_guess[0]:
                        best_guess = best_guess_opt
            if best_guess[0] > 0:
                return best_guess[1]
            if default:
                return default
        return False


        raise ValueError('element should have the keys field_type and field_id')

    def make_infosync_json(self, answer, element, best_effort=False):
        #answer: The answer or answer of certain field
        #element: should be the field for the answer
        #this should contain ['field_type'] and ['field_id']
        #If best_effort is selected then it will try the best options
        # a select field has
        #if answer or answer == 0:
        if answer or (answer==0 and element.get('field_type') and element['field_type'] in ('integer','float','decimal')):
            try:
                if not element.get('field_type') or not element.get('field_id'):
                    raise ValueError('element should have the keys field_type and field_id')
                if element['field_type'] in ('text', 'textarea', 'email', 'password'):
                    return {element['field_id']:str(answer)}
                if element['field_type'] in ('select-one', 'radio', 'select'):
                    answer = self.make_infosync_select_json(answer, element, best_effort)
                    if answer or answer == 0:
                        return {element['field_id']:answer}
                if element['field_type'] in ('checkbox'):
                    answer_list = []
                    for answer in answer.split(','):
                        answer = self.make_infosync_select_json(answer, element, best_effort)
                        if answer:
                            answer_list.append(answer)
                    if answer_list:
                        return {element['field_id']:answer_list}
                if element['field_type'] in ('integer'):
                    return {element['field_id']:int(answer)}
                if element['field_type'] in ('decimal','float'):
                    return {element['field_id']:float(answer)}
                if element['field_type'] in ('date', 'time', 'datetime'):
                    date_str = self.validate(str(answer), check=element['field_type'])
                    return {element['field_id']:date_str}
            except ValueError as e:
                #print('error', e)
                #print('value', answer)
                return {}
        return {}

    def move_item(self, parent_id, items, jwt_settings_key=False):
        """
        Moves one item or items inside other item. Moving items inside a folder
        Args:
            parent_id (str): Folder id to move to
            items (list): List of folder ids
        """
        url = self.api_url.item['move_item']
        return self.network.dispatch(url, data={'items':items, 'parent':parent_id}, jwt_settings_key=jwt_settings_key)

    def thread_function_dict(self, record, data, type_update, jwt_settings_key):
        #if record not in self.thread_dict.keys():
        data[type_update] = [record]
        res = self.network.dispatch(self.api_url.record['form_answer_patch_multi'], data=data,
            jwt_settings_key=jwt_settings_key)
        self.thread_dict[record] = res
        return res
        #logging.info("Finishing with code"%(record, res))

    def patch_multi_record(self, answers, form_id, folios=[], record_id=[], jwt_settings_key=False, threading=False):
        if not answers or not (folios or record_id):
            return {}
        data = {'all_responses': True}
        data = {'type': {'selected': True}}
        data['answers'] = answers
        data['form_id'] = form_id
        type_update = 'records'

        if folios and not record_id:
            data['folios'] = folios
            type_update = 'folios'

        elif not folios and record_id:
            data['records'] = record_id
        else:
            data['records'] = record_id

        data['form_id'] = form_id

        records_updated = []

        if threading:
            self.thread_dict = {}
            with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
                if data.get(type_update, False):
                    records = data.pop(type_update)
                    to_multi_patch = [executor.submit(self.thread_function_dict, record, data, type_update, jwt_settings_key=jwt_settings_key) for record in records]
                    for one_multi_patch in concurrent.futures.as_completed(to_multi_patch):
                        resp = one_multi_patch.result()
                        objects_updated = resp.get('json', {})
                        if objects_updated.get('objects'):
                            objects_updated = objects_updated['objects']
                        else:
                            objects_updated = [objects_updated,]
                        for o in objects_updated:
                            for f in o:
                                if type_update == 'folios':
                                    records_updated.append(o)
                                else:
                                    records_updated.append(o)
                    '''
                    for record in records:
                        data['records'] = [record]
                        executor.map(lambda x: self.thread_function_dict(x, data,
                            jwt_settings_key=jwt_settings_key), [record])
                    '''
                # elif data.get('folios', False):
                #     folios = data.pop('folios')
                #     for folio in folios:
                #         executor.map(lambda x: self.thread_function_dict(x, data,
                #             jwt_settings_key=jwt_settings_key), [folio])
            # no_records_updated = []
            # print('records_updated=',records_updated)
            # if record_id:
            #     print(']]]]]]]]]]]]]]]]]')
            #     print('record_id=', record_id)
            #     print('records_updated=', records_updated)
            #     no_records_updated = list( set(record_id) - set(records_updated) )
            # elif folios:
            #     no_records_updated = list( set(folios) - set(records_updated) )
            # print('no_records_updated=',no_records_updated)
            # for no_update in no_records_updated:
            #     self.thread_dict[ no_update ] = {'status_code': 400, 'error': 'Error al acutalizar el registro con multi_record, favor de reintenar'}
            return  records_updated

        return self.network.dispatch(self.api_url.record['form_answer_patch_multi'], data=data,
            jwt_settings_key=jwt_settings_key)

    def thread_function_bulk_patch(self, data, form_id,  jwt_settings_key):
        #if record not in self.thread_dict.keys():
        data['form_id'] = form_id

        res = self.network.dispatch(self.api_url.record['form_answer_patch_multi'], data=data,
            jwt_settings_key=jwt_settings_key)
        if data.get('folio'):
            self.thread_dict[data['folio']] = res
        else:
            self.thread_dict[data['records']] = res
        #logging.info("Finishing with code"%(record, res))

    def bulk_patch(self, records, form_id, jwt_settings_key=False, threading=False):
        # if not records:
        #     print('bulk_patch >> no obtubo answers o folios')
        #     return {}
        # if not records.get('folios') or records.get('records'):
        #     print('no folio provided')
        #     return {}
        if threading:
            with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
                for data in records:
                    executor.map(lambda x: self.thread_function_bulk_patch(x, form_id,
                        jwt_settings_key=jwt_settings_key), [data])
            return  self.thread_dict
        return self.network.dispatch(self.api_url.record['form_answer_patch_multi'], data=data, jwt_settings_key=jwt_settings_key)

    def post_upload_file(self, data, up_file, jwt_settings_key=False):
        #data:
        #up_file:
        return self.network.dispatch(self.api_url.form['upload_file'], data=data, up_file=up_file, jwt_settings_key=jwt_settings_key)

    def post_upload_script(self, dir_script, script_id=None, image=None, jwt_settings_key=False):
        url = self.api_url.script['upload_script']['url']
        method = self.api_url.script['upload_script']['method']
        if script_id:
            url += str(script_id)
        if not image:
            image = "linkaform/python3_lkf:latest"
        script_file = open(dir_script, 'rb')
        name_script = dir_script.split('/')[-1]
        script_file_dir = [('File', (name_script, script_file, 'application/octet-stream'))]
        data_script = {
            'name': name_script,
            'is_script': True,
            'properties': '{"container":"' + image + '"}'
        }
        return self.network.dispatch(url=url, method=method, data=data_script, up_file=script_file_dir, jwt_settings_key=jwt_settings_key)

    def update_report(self, report_id, properites, jwt_settings_key=False):
        url = self.api_url.report['update_report']['url'].format(report_id)
        method = self.api_url.report['update_report']['method']
        return self.network.dispatch(url=url, method=method, data=properites, jwt_settings_key=jwt_settings_key)

    def update_script(self, script_id, properites, jwt_settings_key=False):
        url = self.api_url.script['update_script']['url'].format(script_id)
        method = self.api_url.script['update_script']['method']
        return self.network.dispatch(url=url, method=method, data=properites, jwt_settings_key=jwt_settings_key)

    def post_upload_tmp(self, data, up_file, jwt_settings_key=False):
        #data:
        #up_file:
        return self.network.dispatch(self.api_url.form['upload_tmp'], data=data, up_file=up_file, jwt_settings_key=jwt_settings_key)

    def cdb_upload(self, data, jwt_settings_key=False):
        #data:
        url = self.api_url.record['cdb_upload']['url']
        method = self.api_url.record['cdb_upload']['method']
        response = self.network.dispatch(url=url, method=method, data=data,  jwt_settings_key=jwt_settings_key)
        return response

    def patch_record(self, data, record_id=None, jwt_settings_key=False):
        #If no record_id is send, it is asuemed that the record_id
        #all ready comes inside the data dictionary
        if record_id:
            data['_id'] = record_id
        return self.network.patch_forms_answers(data , jwt_settings_key=jwt_settings_key)

    def patch_record_list(self, data, jwt_settings_key=False):
        #If no record_id is send, it is asuemed that the record_id
        #all ready comes inside the data dictionary
        return self.network.patch_forms_answers_list(data, jwt_settings_key=jwt_settings_key)

    def post_forms_answers(self, answers, test=False, jwt_settings_key=False):
        return self.network.post_forms_answers(answers, jwt_settings_key=jwt_settings_key)

    def post_forms_answers_list(self, answers, test=False, jwt_settings_key=False ):
        return self.network.post_forms_answers_list(answers, jwt_settings_key=jwt_settings_key)

    def validate(self, date_str, check='date'):
        #check args date, time or datetime
        if check == 'datetime':
            check_str = '%Y-%m-%d %H:%M:%S'
            date_str = date_str=str(date_str)[:19]
        elif check == 'time':
            check_str = '%H:%M:%S'
            date_str = str(date_str)[:8]
        else:
            check_str = '%Y-%m-%d'
            date_str = str(date_str)[:10]
        try:
            datetime.strptime(date_str, check_str)
            return date_str
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    def run_script(self, data, jwt_settings_key=False):
        return self.network.dispatch(self.api_url.script['run_script'], data=data, jwt_settings_key=jwt_settings_key)

    def run_workflow_action(self, data, jwt_settings_key=False):
        """
        Run workflow action
        data:
        {
            "action_id":1, #el action id
            "record_id":"58e522a2b43fdd4ae10e7210", #record id al que se le va aplicar la accion
            "extra_args": {
                "form_id":35376 #forma donde eta registra la accion
            },
            "configuration": {
            }
        }
        """
        return self.network.dispatch(self.api_url.form['run_wf_action'], data=data, jwt_settings_key=jwt_settings_key)


    """
    ITEMS
    """
    def delete_item(self, item_id, jwt_settings_key=False):
        # Delete an item
        url = self.api_url.item['delete_item']['url'].format(item_id)
        method = self.api_url.item['delete_item']['method']
        return self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)

    """
    Formas
    """
    def download_form(self, form_id, jwt_settings_key=False):
        url = '{}{}/'.format(self.api_url.form['download_form_data']['url'], form_id)
        method = self.api_url.form['download_form_data']['method']
        return self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)


    """
    GROUPS
    """
    def delete_group(self, group_id, jwt_settings_key=False):
        post_json = self.api_url.groups['delete_group']
        url = post_json['url'].format(group_id)
        response = self.network.dispatch(url=url, method=post_json['method'], jwt_settings_key=jwt_settings_key)

        return response

    def edit_group(self, group_id, data, jwt_settings_key=False):
        post_json = self.api_url.groups['edit_group']
        url = post_json['url'].format(group_id)
        response = self.network.dispatch(url=url, method=post_json['method'], data=data, jwt_settings_key=jwt_settings_key)

        return response

    """
    Rules
    """

    def upload_rules(self, data, method='POST', jwt_settings_key=False):
        if method == 'PATCH':
            url = self.api_url.form['upload_rules']['url'] + data.get('id') +'/'
        else:
            url = self.api_url.form['upload_rules']['url']
        return self.network.dispatch(url=url, method=method, data=data, jwt_settings_key=jwt_settings_key)

    """
    Items
    """
    def share_form(self, data_to_share, unshare=False, jwt_settings_key=False):
        # Compartir y descompartir items
        url = self.api_url.form['share_form']['url']
        method = self.api_url.form['share_form']['method']
        if unshare:
            data = {'objects': [], 'deleted_objects': data_to_share}
        else:
            data = {'objects': [data_to_share,]}

        return self.network.dispatch(url=url, method=method, data=data, jwt_settings_key=jwt_settings_key)

    """
    Workflows
    """
    def upload_workflows(self, data, method='POST', jwt_settings_key=False):
        if method == 'PATCH':
            url = self.api_url.form['upload_workflows']['url'] + data.get('id') +'/'
        else:
            url = self.api_url.form['upload_workflows']['url']
        return self.network.dispatch(url=url, method=method, data=data, jwt_settings_key=jwt_settings_key)

    """
    Catalogos
    """

    def update_catalog_model(self, catalog_id, catalog_model, jwt_settings_key=False):
        url = self.api_url.catalog['update_catalog_model']['url'].format(catalog_id)
        method = self.api_url.catalog['update_catalog_model']['method']
        r = self.network.dispatch(url=url, method=method, data=catalog_model, jwt_settings_key=jwt_settings_key)
        return r

    def catalog_load_rows(self, catalog_id, catalog_map, spreadsheet_url, jwt_settings_key=False):
        url = self.api_url.catalog['load_rows']['url']
        method = self.api_url.catalog['load_rows']['method']
        data ={
            'catalog_id': catalog_id,
            'mapping': catalog_map,
            'spreadsheet_url': spreadsheet_url
        }
        r = self.network.dispatch(url=url, method=method, data=data, jwt_settings_key=jwt_settings_key)
        return r

    def download_catalog_model(self, catalog_id, jwt_settings_key=False):
        url = '{}{}/'.format(self.api_url.catalog['download_catalog_model']['url'], catalog_id)
        method = self.api_url.catalog['download_catalog_model']['method']
        return self.network.dispatch(url=url, method=method, jwt_settings_key=jwt_settings_key)

    def post_catalog_answers(self, answers, test=False, jwt_settings_key=False):
        return self.network.post_catalog_answers(answers, jwt_settings_key=jwt_settings_key)

    def post_catalog_answers_list(self, answers, test=False, jwt_settings_key=False ):
        return self.network.post_catalog_answers_list(answers, jwt_settings_key=jwt_settings_key)

    def prepare_response_find(self, response, **kwargs):
        limit = kwargs.get('limit')
        list_data = response.get('json',{}).get('objects',[])
        list_to_response = []
        for d in list_data:
            answers_data = d.get('answers',{})
            answers_data.update(
                {'_id':d.get('_id',''),
                '_rev':d.get('_rev',''),
                'created_at':d.get('created_at',''),
                'updated_at':d.get('updated_at',''),
                })
            if limit and limit == 1:
                return answers_data
            list_to_response.append(answers_data)
        return list_to_response

    def search_catalog_answers(self, catalog_id, answers={}, jwt_settings_key=False, **kwargs):
        limit =  kwargs.get('limit', 10000)
        skip =  kwargs.get('skip', 0)
        mango_query = {
               "selector": {'answers':answers},
                "limit":limit,
                "skip":skip
            }
        return self.search_catalog(catalog_id, mango_query=mango_query, jwt_settings_key=jwt_settings_key, **kwargs)

    def search_catalog(self, catalog_id, mango_query={}, jwt_settings_key=False, **kwargs):
        limit =  kwargs.get('limit', 10000)
        skip =  kwargs.get('skip', 0)
        if not mango_query:
            mango_query = {
               "selector": {
                  "_id": {
                     "$gt": None
                     } 
                },
                "limit":limit,
                "skip":skip
            }
        url = self.api_url.catalog['get_record_by_folio']['url']
        method = self.api_url.catalog['get_record_by_folio']['method']
        data_for_post = {
            'catalog_id':catalog_id,
            'mango':mango_query
            }
        response = self.network.dispatch(url=url, method=method, use_api_key=False, data=data_for_post, jwt_settings_key=jwt_settings_key)
        if response['status_code'] == 200:
            return self.prepare_response_find(response, **kwargs)
        if response['status_code'] == 440:
            if response.get('json'):
                return response['json'].get('error')
            if response.get('content'):
                return response['content'].get('error')
        return False

    def update_catalog_answers(self, data, record_id=None, jwt_settings_key=False):
        if record_id:
            data['_id'] = record_id
        return self.network.patch_catalog_answers(data, jwt_settings_key=jwt_settings_key)

    def thread_function_bulk_patch_catalog(self, data, catalog_id,  jwt_settings_key):
        data['catalog_id'] = catalog_id
        post_json = deepcopy(self.api_url.catalog['update_catalog_multi'])
        post_json['url'] = post_json['url'].format(data['record_id'])
        res = self.network.dispatch(post_json, data=data,
            jwt_settings_key=jwt_settings_key)
        if data.get('_id'):
            self.thread_dict[data['_id']] = res
        else:
            self.thread_dict[data['records']] = res

    def bulk_patch_catalog(self, records, catalog_id, jwt_settings_key=False, threading=False):
        if threading:
            with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
                for data in records:
                    executor.map(lambda x: self.thread_function_bulk_patch_catalog(x, catalog_id,
                        jwt_settings_key=jwt_settings_key), [data])
            return  self.thread_dict
        else:
            res = []
            for data in records:
                post_json = deepcopy(self.api_url.catalog['update_catalog_multi'])
                post_json['url'] = post_json['url'].format(data['record_id'])
                res.append(self.network.dispatch(post_json, data=data, jwt_settings_key=jwt_settings_key))
        return res

    def delete_catalog_record(self, catalog_id, id_record, rev, jwt_settings_key=False):
        url = self.api_url.catalog['delete_catalog_record']
        data_for_post = {"docs":[{"_id":id_record, "_rev":rev, "_deleted":True, "index":0}],"catalog_id":catalog_id}
        response = self.network.dispatch(url, data=data_for_post, jwt_settings_key=jwt_settings_key)
        return response

    def update_catalog_multi_record(self, answers, catalog_id, record_id=[], jwt_settings_key=False):
        if not answers or not record_id:
            return {}
        data = {
            'answers': answers,
            'catalog_id': catalog_id,
            'objects': record_id
        }
        return self.network.dispatch(self.api_url.catalog['catalog_answer_patch_multi'], data=data, jwt_settings_key=jwt_settings_key)

    def delete_filter(self, catalog_id, filter_name, jwt_settings_key=False):
        url = self.api_url.catalog['delete_filter']['url']
        method = self.api_url.catalog['delete_filter']['method']
        data_for_post = {
            "catalog_id": catalog_id,
            "filter_name": filter_name
        }
        response = self.network.dispatch(url=url, method=method, use_api_key=False, data=data_for_post, jwt_settings_key=jwt_settings_key)
        return response

    def share_catalog(self, data_to_share, unshare=False, jwt_settings_key=False):
        url = self.api_url.catalog['share_catalog']['url']
        method = self.api_url.catalog['share_catalog']['method']
        if unshare:
            data = { 'objects': [], 'deleted_objects': data_to_share }
        else:
            data = { 'objects': [ data_to_share, ] }
        r = self.network.dispatch(url=url, method=method, data=data, jwt_settings_key=jwt_settings_key)
        return r

    def find_record(self, db_cr, rec_id):
        mango_query = {
              "selector": {
                "_id":rec_id
              },
               "limit": 1
          }
        result = db_cr.find(mango_query)
        res = [x for x in result]
        return res

    def record_etl(self, db_cr, catalog_map, record):
        rec_id = record.pop('_id')
        rec = self.find_record(db_cr, rec_id)
        ans = {}
        rec_rev = False
        if rec:
            rec_rev = rec[0].pop('_rev')
            ans = rec[0].get('answers',{})
        new_rec = {
            'answers':ans,
            '_id':rec_id,
            # '_rev':record.pop('_rev'),
        }
        if rec_rev:
            new_rec.update({'_rev':rec_rev})
        record.pop('_rev')
        answers = record.pop('answers')
        if answers:
            for key, value in catalog_map.items():
                if answers.get(key):
                    new_rec['answers'][value] = answers.pop(key)
        new_rec.update(record)
        return new_rec

    def update_records(self, db_cr_to, records, catalog_map):
        update_docs = []
        for idx, rec in enumerate(records):
            new_rec = self.record_etl(db_cr_to, catalog_map, rec)
            r = db_cr_to.save(new_rec)
        return True

    def send_sms(self, phone_to, body, use_api_key=False, jwt_settings_key=False):
        twilio_creds = self.get_user_twilio_creds(use_api_key=use_api_key, jwt_settings_key=jwt_settings_key)
        if twilio_creds.get('status_code') == 201:
            twilio_creds = twilio_creds['json']
        else:
            Exception({"msg":"Error al obtener credecniales de Twilio"})

        api_key_sid = twilio_creds['api_key_sid']
        api_key_secret = twilio_creds['api_key_secret']
        account_sid = twilio_creds['twilio_sid']
        phone_twilio = twilio_creds['phone']

        client = Client(api_key_sid, api_key_secret, account_sid)
        
        message_data = {
            "phone_to": phone_to,
            "body": body,
            "status": "pendiente",
            "created_at": datetime.now(),
        }
        message_record = self.lkf_object.create(_object=message_data, is_json=True, collection="messages")
        message_id = message_record.get('_id')
        
        try:
            response = client.messages.create(
                from_=phone_twilio,
                body=body,
                to=phone_to,
            )

            status_update = {
                "status": "enviado",
                "twilio_message_sid": response.sid,
                "updated_at": datetime.now()
            }
            self.lkf_object.update({"_id": message_id}, status_update, collection="messages")
        except Exception as e:
            error_message = str(e)

            cleaned_message = error_message.replace("\x1b[31m", "").replace("\x1b[49m", "") \
                                            .replace("\x1b[37m", "").replace("\x1b[49m", "") \
                                            .replace("\x1b[36m", "").replace("\x1b[34m", "") \
                                            .replace("\x1b[0m", "")

            cleaned_message = cleaned_message.replace('\n', ' ').strip()

            if 'TwilioRestException' in cleaned_message:
                cleaned_message = cleaned_message.split('TwilioRestException')[0]

            status_update = {
                "status": "error",
                "error_message": cleaned_message,
                "updated_at": datetime.now()
            }
            self.lkf_object.update({"_id": message_id}, status_update, collection="messages")
            return 'Error sending sms error: ', e
        return response

    def sync_catalogs(self, catalog_from_id, catlog_to_id, query, catalog_map):
        cdb_obj = couch_util.Couch_utils(self.settings)
        cdb = cdb_obj.cdb
        catalog_from = "catalog_records_{}".format(catalog_from_id)
        catalog_to = "catalog_records_{}".format(catlog_to_id)
        db_cr = cdb[catalog_from]
        # db_cr = cdb[catalog_from]
        db_cr_to = cdb[catalog_to]
        # db_cr_to = cdb[catalog_to]
        last_seq = self.get_last_seq(db_cr_to, catalog_from_id)
        if last_seq:
            last_seq = last_seq[0].get('last_seq')
        else:
            last_seq = None
        change = db_cr.changes(since=last_seq)
        results = change['results']
        last_seq = change['last_seq']
        change_id = [ rec.get('id') for rec in results if rec.get('id')[0] != '_' ]
        change_id = change_id[0:200]
        total_rec = len(change_id)
        batch_size = 400
        records_bach = []
        threads = []
        for x in range(int(ceil(total_rec/float(batch_size)))):
            form_id = x * batch_size
            to_id = (x+1) * batch_size
            batch_rec = change_id[form_id:to_id]
            recs = self.get_records(db_cr, batch_rec, batch_size)
            threads.append(threading.Thread(
                target = self.update_records,
                args = (db_cr_to, recs, catalog_map)
            ))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        last_seq_id = 'last_seq_{}'.format(catalog_from_id)
        last_seq_rec = self.find_record(db_cr_to, last_seq_id)
        update_seq = {
            '_id': last_seq_id,
            'last_seq':last_seq
        }
        if last_seq_rec:
            update_seq.update({'_rev':last_seq_rec[0]['_rev']})
        r = db_cr_to.save(update_seq)
        return True

    def sync_catalogs_records(self, data, jwt_settings_key=False):
        """
        Sinconiza el registro de una forma a un catalogo 
        data:
        {
            "catalogs_ids":[7777, 1234],# $id de los catalogos en si
            "form_answers_ids":["58e522a2b43fdd4ae10e7210", "58e522a2b43fdd4ae10e7210"], #record id al que se le va aplicar la accion
            "status":"created/edited/deleted"
        }
        """
        
        # Split form_answers_ids into chunks of 200
        catalogs_ids = data["catalogs_ids"]
        status = data["status"]
        form_answers_ids = data["form_answers_ids"]
        
        # Create chunks of 200 form answers
        chunk_size = 200
        chunks = [form_answers_ids[i:i + chunk_size] for i in range(0, len(form_answers_ids), chunk_size)]
        
        # Process each chunk in parallel using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
            futures = []
            for chunk in chunks:
                chunk_data = {
                    "catalogs_ids": catalogs_ids,
                    "form_answers_ids": chunk,
                    "status": status
                }
                future = executor.submit(
                    self.network.dispatch,
                    self.api_url.catalog['sync_catalogs_records'],
                    data=chunk_data,
                    jwt_settings_key=jwt_settings_key
                )
                futures.append(future)
            
            # Wait for all threads to complete
            concurrent.futures.wait(futures)
            
            # Get results from all threads
            results = [future.result() for future in futures]
            
        # Return the combined results
        return results

    def read_current_record_from_txt(self, file_url):
        name_downloded = self.download_pdf( file_url, is_txt=True )
        f = open( "/tmp/{}".format( name_downloded ) )
        return simplejson.loads( f.read() )

    """
    PDF
    """
    def download_pdf(self, file_url, is_txt=False):
        oc_name = 'oc_{}.pdf'.format(str(bson.ObjectId()))
        if is_txt:
            oc_name = 'file_{}.txt'.format(str(bson.ObjectId()))
        wget.download(file_url, '/tmp/{}'.format(oc_name))
        return oc_name


    """
    CRON
    """
    def subscribe_cron(self, body, jwt_settings_key=False):
        #Returns all users of a group
        #user_type 'users', 'admin_users','supervisor_users'
        post_json = self.api_url.get_airflow()['subscribe']
        url = post_json['url']
        response = self.network.dispatch(url=url, method=post_json['method'], data=body, jwt_settings_key=jwt_settings_key)
        return response

    def update_cron(self, body, jwt_settings_key=False):
        #Returns all users of a group
        #user_type 'users', 'admin_users','supervisor_users'
        post_json = self.api_url.get_airflow()['update']
        url = post_json['url']
        response = self.network.dispatch(url=url, method=post_json['method'], data=body, jwt_settings_key=jwt_settings_key)
        return response

    def delete_cron(self, schedule_id, delete_all_events=True, jwt_settings_key=False):
        #Returns all users of a group
        #user_type 'users', 'admin_users','supervisor_users'
        post_json = self.api_url.get_airflow()['delete_schedule']
        url = post_json['url']
        method = post_json['method']
        body = {
            "_id": schedule_id,
            "delete_all_events":delete_all_events
        }
        response = self.network.dispatch(url=url, method=method, data=body, jwt_settings_key=jwt_settings_key)
        return response
    
    """
    ADDONS
    """

    def unlink_device(self, user_id, jwt_settings_key=False):
        post_json = self.api_url.globals['unlink_device']
        url = post_json['url']
        method = post_json['method']
        body = {
            "user_id": user_id,
            "unlink_all":True
        }
        response = self.network.dispatch(url=url, method=method, data=body, jwt_settings_key=jwt_settings_key)
        return response        

    def xml_to_json(self, xml_data):
        #TODO AGUAS CON LOS ENTEROS
        # Create an ElementTree object from the XML data
        try:
            tree = ET.ElementTree(ET.fromstring(xml_data))
        except Exception as e:
            print("Warning: Couldn't read file error: {}, returning an empty json ".format(e))
            return {}
        # Function to recursively convert XML elements to JSON
        def element_to_json(element):
            data = {}
            # Process attributes of the element (excluding "item" elements)
            if element.tag != "item" and element.attrib:
                #TODO SPECIAL ATRIBUTS LIKE A VALUE IS A STRING NOT AN INTEGER
                data[element.tag] = data.get(element.tag,{})
                data[element.tag].update(element.attrib)
                # data["@attributes"] = element.attrib
            # Process child elements of the element
            if element.findall("*"):
                for child in element:
                    if child.tag == "item":
                        if child.tag in data:
                            if isinstance(data[child.tag], list):
                                data[child.tag].append(element_to_json(child))
                            else:
                                data[child.tag] = [data[child.tag], element_to_json(child)]
                        else:
                            data[child.tag] = [element_to_json(child)]
                    else:
                        if child.tag in data:
                            if isinstance(data[child.tag], list):
                                data[child.tag].append(element_to_json(child))
                            else:
                                data[child.tag] = [data[child.tag], element_to_json(child)]
                        else:
                            res = element_to_json(child)
                            child_data = deepcopy(res)
                            if isinstance(child_data, dict):
                                if not child_data:
                                    data[child.tag] = ''
                                for key, value in child_data.items():
                                    if key == 'item':
                                        data[tv(child.tag)] = data.get(child.tag, [])
                                        data[tv(child.tag)] = value
                                    else:
                                        data[tv(child.tag)] = data.get(child.tag, {})
                                        ch_data = get_same_properites(child.tag, res)
                                        data[tv(child.tag)] = transform_dict_values(ch_data)
                            else:
                                if tv(child.tag) == 'font_size' and tv(element.tag) == 'watermark_config':
                                    data[tv(child.tag)] = str(child_data)
                                else:
                                    data[tv(child.tag)] = tv(child_data)
            # Process text content of the element
            if element.text:
                text = element.text.strip()
                if data:
                    if text:
                        data['value'] = text
                    #Do not delete or move
                    pass
                else:
                    data = text
            return data
        # Convert the root element to JSON
        json_data = element_to_json(tree.getroot())
        # print('json_data', simplejson.dumps(json_data, indent=4))
        return json_data

    def json_to_xml(self, json_data, pretty=True):
        # Create the root element of the XML tree
        root = ET.Element('lkf')
        # Function to recursively convert JSON data to XML elements
        def json_to_xml_elements(data, parent):
            if isinstance(data, dict):
                if data:
                    for key, value in data.items():
                        element = ET.SubElement(parent, key)
                        json_to_xml_elements(value, element)
                else:
                    parent.text = '{}'
            elif isinstance(data, list):
                if data == []:
                    parent.text = '[]'
                for item in data:
                    element = ET.SubElement(parent, 'item')
                    json_to_xml_elements(item, element)
            else:
                if isinstance(data, str):
                    x = str(data.encode('utf-8').decode('utf-8'))
                    parent.text = x
                else:
                    parent.text = str(data)
        # Convert JSON data to XML elements
        json_to_xml_elements(json_data, root)
        # Create an XML tree from the root element
        tree = ET.ElementTree(root)
        # Convert the XML tree to a string
        xml_str = ET.tostring(root, encoding='utf-8').decode()
        if pretty:
            dom = xml.dom.minidom.parseString(xml_str)
            xml_str = dom.toprettyxml(indent="    ")
        return xml_str


def warning(*objs):
    '''
    To print(stuff at stderr)
    '''
    output = "warning:%s\n" % objs
    stderr.write(output)

def transform_dict_values(data):
    #return { tv(k):(tv(v)) for k,v in data.items()}
    res={}
    for k,v in  data.items():
        if k == 'font_size':
            res[tv(k)] = str(v)
        else:
            res[tv(k)] = tv(v)
    return res

def tv(value):
    #check if is boolean
    if value == 1:
        value = value
    elif value == 0:
        value = value
    elif value == '[]' or value == []:
        value = []
    elif value == '{}' or value == {}:
        value = {}
    elif value == 'False' or value == 'false' or value == False:
        value = False
    elif value == 'True' or value == 'true' or value == True:
        value = True
    elif value == 'None' or value == 'none' or value == None or not value:
        value = None
    elif isinstance(value, str) and value.find('amp_') == 0:
        value = value.replace('amp_','$')
    elif isinstance(value, str) and value.find('num_') == 0:
        value = value.replace('num_','')
    else:

        #checks if its a numeric value
        value = get_numeric(value)
    return value

def get_numeric(value):
    if isinstance(value, str):
        has_decimal = value.find('.')
        if has_decimal < 0:
            if value.find('0') == 0 or len(value) == 24:
                return value
            try:
                value = int(value)
            except ValueError:
                return value
        else:
            try:
                value = float(value)
            except:
                return value
    return value

def get_same_properites(key, values):
    if values.get(key):
        update_vals = values.pop(key)
        values.update(update_vals)
    return values
