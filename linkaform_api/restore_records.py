# PYTHON
import mongo_util
import simplejson
from datetime import datetime

# MONGO
from bson.objectid import ObjectId
from pymongo import MongoClient

host = 'db4.linkaform.com'
#host = 'localhost'
port = 27017
collection_name = 'form_answer'
cr = MongoClient(host, port)
# mongo_dbname = 'infosync_answers_client_%s'%user_id
#databases = cr.database_names()
#databases = ['infosync_answers_client_126']

date = datetime.strptime('2017-02-20 00:00:00', "%Y-%m-%d %H:%M:%S")
records_with_errors = {}
databases_with_errors = []

def get_records(query):
    # query = {'voucher.fields': {'$exists':1}, 'deleted_at':{'$exists':0}, 'created_at':{'$gte':date}}
    result = mongo_util.get_collection_objects(cur_col, query)
    return result

def get_records_2fix(record):
    field_types = [field['field_type'] for field in record['voucher']['fields']]
    _continue = True
    has_image = False
    answer_count = 0
    for _type in ('image', 'signature', 'document', 'file'):
        if _type in field_types:
            _continue = False
    if _continue:
        return 0
    # print 'checking fields....'
    for field in record['voucher']['fields']:
        if _continue:
            return 0
        _id = field['field_id']['id']
        if field['field_type'] not in ('image', 'signature', 'document', 'file'):
            if field['required'] and not field.has_key('group'):
                if not record['answers'].has_key(_id):
                    # count += 1
                    # print 'folio=', record['folio']
                    # print 'form_id=', record['form_id']
                    # print 'version=', record['other_versions']
                    # print 'start_timestamp=', record['start_timestamp']
                    # print '======================'
                    answer_count += 1
                    _continue = True
                    return 1
                else:
                    answer_count += 1
            elif not field.has_key('group'):
                if record['answers'].has_key(_id):
                    answer_count += 1
                    _continue = True
        if field['field_type'] in ('image', 'signature', 'document', 'file'):
            if record['answers'].has_key(_id):
                has_image = True
    if answer_count == 0 and has_image:
        # count += 1
        # print 'folio=', record['folio']
        # print 'form_id=', record['form_id']
        # print 'version=', record['other_versions']
        # print 'start_timestamp=', record['start_timestamp']
        # print '======================'
        return 1
    return 0

def fix_records():
    records_file = open('registros96.txt','r')
    record_str = ''
    records_2send = []
    for line in records_file:
        record_str += line
        if line == '\n':
            records_2send.append(record_str)
            record_str = ''

    for record_str in records_2send:
        record = simplejson.loads(record_str)
        query = {'deleted_at':{'$exists':0}, 'start_timestamp':float(record['start_timestamp']), 'form_id':record['form_id'] }
        result = get_records(query)
        answers_post = record['answers']
        answers_pics = result[0]['answers']
        print 'folio', result[0]['folio']
        answers_pics.update(answers_post)
        cur_col.update(
            query,
            {
                "$set": {
                    "answers": answers_pics
                    }
            } )
    return

def update_groups(record):
    group_id = None
    field_id = None
    if not record.get('voucher', None):
        return
        # continue
    for field in record['voucher']['fields']:
        if field['field_type'] == 'group':
            group_id = field['field_id']['id']

        if group_id:
            # print 'folio=',record['folio']
            if record['answers'].has_key(group_id) and record['answers'][group_id]:
                # print record['answers'][group_id]
                if isinstance(record['answers'][group_id], dict):
                    print 'folio=',record['folio']
                    cur_col.update(
                        {'_id':ObjectId(record['_id'])},
                        {
                            "$set": {
                                "answers." + group_id: [record['answers'][group_id]]
                                }
                        } )
    return


for dbname in databases:
    if dbname in ['infosync', 'local']:
        continue

    print dbname.strip('infosync_answers_client_')
    # cur_db = mongo_util.connect_mongodb(dbname, host, port)
    cur_db = mongo_util.connect_mongodb(dbname, host, port)
    cur_col = mongo_util.get_mongo_collection(cur_db, collection_name)
    user_id = dbname.split('_')[-1]
    if not user_id:
        databases_with_errors.append(dbname)
        continue
    # Actualiza grupos
    # query = {'voucher.fields': {'$exists':1}, 'deleted_at':{'$exists':0}, 'created_at':{'$gte':date}}
    # Obtener registros de 2017-02-20 a la fecha
    query = {'deleted_at':{'$exists':0}, 'created_at':{'$gte':date}}

    # fix_records()

    result = get_records(query)
    records = [record for record in result]
    count = 0
    for record in records:
        count += get_records_2fix(record)
    if count > 0:
        print dbname ,',', count
