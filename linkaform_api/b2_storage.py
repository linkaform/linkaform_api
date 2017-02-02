# -*- coding: utf-8 -*-
'''
Author Jonathan
'''

# PYTHON
import datetime, base64, hashlib, json
from urllib2 import Request, urlopen

def decode(m):
    return m.decode('utf-8')

def encode(m):
    return m.encode('utf-8')

class B2Connection():
    """
    Contains information required to establish connections to the B2 api.
    """
    # LINKAFORM BACKBLAZE ACCOUNT
    ACCOUNT_ID = 'f5fde066eaac'
    APP_KEY = '001bada2501283bc9014a905a767c55761ecb3136c'
    # BUCKET_NAME = 'test-linkaform'
    BUCKET_NAME = 'app-linkaform'

    AUTH_ACCOUNT_URL = 'https://api.backblaze.com/b2api/v1/b2_authorize_account'
    CREATE_BUCKET_URL = '/b2api/v1/b2_create_bucket'
    LIST_BUCKETS_URL = '/b2api/v1/b2_list_buckets'
    valid_duration = datetime.timedelta(days=1) # duration of the authorization token

    def __init__(self, account_data=None):
        self.auth_request_time = datetime.datetime.now() - 42*self.valid_duration
        self.auth_data = self.get_auth_data()
        self.name_id_dict = dict()

    def get_auth_data(self):
        """
        Log in to the B2. Returns an authorization token and a URL for subsequent API calls.
        """
        # Check if the token is still valid
        if datetime.datetime.now() - self.auth_request_time >= self.valid_duration:
            id_and_key = self.ACCOUNT_ID + ':' + self.APP_KEY
            basic_auth_string = 'Basic ' + decode(base64.b64encode(id_and_key.encode('utf-8')))
            headers = {'Authorization' : basic_auth_string}
            request = Request(
                self.AUTH_ACCOUNT_URL,
                headers = headers
            )
            response = urlopen(request)
            self.auth_request_time = datetime.datetime.now() # reset time
            self.auth_data = json.loads(decode(response.read()))
            response.close()
        return self.auth_data

    @property
    def auth_token(self):
        """
        Returns authorization token to use with all calls.
        """
        return self.auth_data['authorizationToken']

    @property
    def api_url(self):
        """
        Returns api url. For all API calls except for uploading and downloading files.
        """
        return self.auth_data['apiUrl']

    @property
    def download_url(self):
        """
        Returns base URL to use for downloading files.
        """
        return self.auth_data['downloadUrl']

    def bucket_data(self, bucket_id):
        """
        Returns information needed for uploads.
        """
        request = Request(
            '%s/b2api/v1/b2_get_upload_url' % self.api_url,
            encode(json.dumps({ 'bucketId' : bucket_id })),
            headers = { 'Authorization': self.auth_token }
        )
        response = urlopen(request)
        _upload_data = json.loads(decode(response.read()))
        response.close()
        return _upload_data

    def get_file_id(self, name):
        """
        Returns the id of the file.
        """
        return self.name_id_dict[name]

    def b2_save(self, file_name, content, bucket_id):
        bucket_data = self.bucket_data(bucket_id)
        try:
            file_data = content.read()
            file_sha1 = hashlib.sha1(file_data).hexdigest()
            headers = {
                'Authorization' : bucket_data['authorizationToken'],
                'X-Bz-File-Name' : file_name,
                'Content-Type' : 'b2/x-auto',
                'X-Bz-Content-Sha1' : file_sha1
            }
            request = Request(bucket_data['uploadUrl'].encode('utf-8'), file_data, headers)

            response = urlopen(request)
            if response.getcode() != 200:
                response.close()
                return None

            response_data = json.loads(decode(response.read()))
            response.close()
            return self.b2_get_url_by_name(self.BUCKET_NAME, file_name)
        except Exception, e:
            print 'UPLOAD FILE ERROR=',e
            return None

    def b2_get_url_by_name(self, bucket_name, file_name):
        """
        Returns download url for using the name of the bucket and the name of the file.
        """
        return self.download_url + '/file/' + bucket_name + '/' + file_name

    def b2_list_file_names(self, bucket_id, max_file_count, start_file_name=None):
        """
        Returns an array of objects, each one describing one file
        """
        try:
            # bucket_data = self.connection.bucket_data(bucket_id)
            url = '%s/b2api/v1/b2_list_file_names' % self.api_url
            headers = {
                'Authorization' : self.auth_token
            }
            params = {
                'bucketId': bucket_id,
                'startFileName': start_file_name,
                'maxFileCount': max_file_count,
            }
            request = Request(url, json.dumps(params), headers)
            response = urlopen(request)
            if response.getcode() != 200:
                response.close()
                return None
            response_data = json.loads(decode(response.read()))
            response.close()
            return response_data['files']
        except Exception, e:
            print e
            return []