# coding: utf-8
#!/usr/bin/python
from pymongo import MongoClient
from pymongo.collection import Collection

class Database:

    connection = None
    db_name_format = 'infosync_answers_client_{0}'
    
    def __init__(self, host, port, user_id):
        self.host = host
        self.port = port
        self.user_id = user_id
        
    def update_records_at_collection(self, records, collection):
        '''
        Update records a given collection
        '''
        errors_counter = 0
        total_records = len(records)

        print "> Updating {} records ...".format(total_records)        
        n = 0
        
        for record in records:
            n =  n + 1
            try:
                print "> Updating {0} record with id {1}".format(n, record['_id'])
                collection.update({'_id': record['_id']}, record)
            except Exception as e:
                errors_counter = errors_counter + 1
                raise ValueError("Something went wrong checking: {0}".format(e.message))
        if (errors_counter == 0 and n == total_records):
            return True
        return False

    
    def create_collection(collection, create_collection=False):
        '''
        Create a collection given name collection and optionally create a new collection in case it does not exist
        '''
        print "> Creating Collection ..."
        connection = self.get_user_connection()
        if create_collection and collection in connection['db'].collection_names():
            oldCollection = connection['db'][collection]
            oldCollection.drop()
        newCollection = Collection(user_connection['db'], collection, create=create_collection)
        return newCollection

    def get_user_connection(self):
        '''
        Get the user connection to database
        '''
        if connection is None:
            self.create_user_connection()
        return self.connection

    def create_user_connection(self):
        '''
        Create user connection to database
        '''
        if self.host is None or self.port is None or self.user_id is None:
            raise ValueError("Need host, port and user_id to work.")
        
        print "> Getting user connection ..."
        connection = {}
        connection['client'] = MongoClient(self.host, self.port)
        user_db_name = self.db_name_format.format(self.user_id)
        if  not user_db_name:
            return None
        connection['db'] = connection['client'][user_db_name]
        self.connection = connection


    def get_collection(self, collection):
        try:
            if self.connection is None:
                raise ValueError("Connection is not defined")
            collection = self.connection['db'][collection]
        except:
            print "Create a connection before get a collection"
        return collection


    def get_records(self, collection, attributes=None):
        if isinstance(collection, Collection):
            if attributes is None:
                return collection.find()
            else:
                return collection.find(attributes)
        else:
            raise TypeError("Collection object received is not an instance of Collection")
        return None

        
    def check_ids_to_replace_at_answers(self, answers_doc, ids_to_migrate, counter = None):
        '''
        Check if in answers document has ids to migrate, if there is at least one id changed 
        the counter dictionary will say "1" to the id changed.
        '''
        if counter is None:        
            counter = dict.fromkeys(ids_to_migrate.keys())
            
        for items in answers_doc:
            if isinstance(items, dict):
                for i_key, i_value in items.iteritems():
                    new_id, counter = self.compare_id_with_ids_to_migrate(i_key, ids_to_migrate, counter)
                    value = i_value
                    if (i_key != new_id):
                        del items[i_key]
                        items[new_id] = value
                    
                    if isinstance(i_value, list):
                        result = self.check_ids_to_replace_at_answers(i_value, ids_to_migrate, counter)
                        items[i_key] = list(result[0])
                        counter = result[1]
        return answers_doc, counter


    def check_ids_to_replace_at_voucher_fields(self, voucher_fields_doc, ids_to_migrate, counter = None):
        '''
        Check if in voucher fields document has ids to migrate, if there is at least one id changed 
        the counter dictionary will say "1" to the id changed.
        '''        
        if counter is None:
            counter = dict.fromkeys(ids_to_migrate.keys())

        for field in voucher_fields_doc:
            for property_key, property_value in field.iteritems():
                if property_key == "field_id":
                    field["field_id"]["id"], counter = self.compare_id_with_ids_to_migrate(field["field_id"]["id"], ids_to_migrate, counter)
        return voucher_fields_doc, counter

    
    def check_ids_to_replace_at_form_pages(self, form_pages_doc, ids_to_migrate, counter = None):
        '''
        Check if in form pages document has ids to migrate, if there is at least one id changed 
        the counter dictionary will say "1" to the id changed.
        '''    
        if counter is None:
            counter = dict.fromkeys(ids_to_migrate.keys())
            
        for page_field in form_pages_doc:            
            page_field["page_fields"], counter = self.check_ids_to_replace_at_voucher_fields(page_field["page_fields"], ids_to_migrate, counter)
        return form_pages_doc, counter

    
    def compare_id_with_ids_to_migrate(self, id_doc, ids_to_migrate, counter):
        '''
        Verify if an id exists in ids to migrate, if exists then the id to migrate will 
        be returned along with the counter which is a counter of the ids modified.
        '''
        for f_key, f_value in ids_to_migrate.iteritems():
            if id_doc in f_value:
                counter[f_key] = 1
                return f_key, counter
        return id_doc, counter


    def print_counter_stats(self, counter, print_counter=True):
        '''
        Print every counter equal to 1
        '''
        keys = counter.keys()
        flag = False
        initial_format = "Counter stats:\n"
        for key in keys:
            if counter[key] is not None:
                initial_format = initial_format + key + " = " + str(counter[key]) + "\n"
                flag = True
        if flag and print_counter:
            delimiter("-")
            print initial_format
            delimiter("-")
            return 1
        return 0
        
    
    def replace_ids_in_records_at_collection(self, ids_to_migrate, collection, attributes = None):
        '''
        Replace ids in a collection given ids to migrate, optionally accepts query attributes.

        Docs to get from json:
        -"answers"
        -"voucher"->"fields"
        -"voucher"->"form_pages"
        '''    
        records = self.get_records(collection, attributes)
        n = 0
        total_records = records.count()

        total_completed = 0
        total_trunked = 0
        total_not_changed = 0

        records_to_modified = list()
        
        print "Total records: #{0}".format(total_records)
        
        for record in records:
            
            flag_answers = 0
            flag_fields = 0
            flag_form_pages = 0
            
            n = n + 1
            delimiter()
            try:
                record["answers"], counter = self.check_ids_to_replace_at_answers([record["answers"]], ids_to_migrate)
                print "> Replacing at answers doc with record {0}".format(n)
                flag_answers = self.print_counter_stats(counter)
            except Exception as e:                
                raise ValueError("Something went wrong checking of ids at answers doc. {0}".format(e.message))
                        
            try:
                record["voucher"]["fields"], counter = self.check_ids_to_replace_at_voucher_fields(record["voucher"]["fields"], ids_to_migrate)            
                print "> Replacing at voucher fields doc with record {0}".format(n)
                flag_fields = self.print_counter_stats(counter)
            except Exception as e:
                raise ValueError("Something went wrong checking of ids at voucher fields doc. {0}".format(e.message))
                
            try:
                record["voucher"]["form_pages"], counter = self.check_ids_to_replace_at_form_pages(record["voucher"]["form_pages"], ids_to_migrate)
                print "> Replacing at form pages doc with record {0}".format(n)
                flag_form_pages = self.print_counter_stats(counter)
            except Exception as e:
                raise ValueError("Something went wrong checking of ids at voucher form pages doc. {0}".format(e.message))


            if (flag_answers == 1 and flag_fields == 1 and flag_form_pages == 1):
                records_to_modified.append(record)
                total_completed = total_completed + 1
            elif (flag_answers == 1 or flag_fields == 1 or flag_form_pages == 1):
                total_trunked = total_trunked + 1
            else:
                total_not_changed = total_not_changed + 1
                
            print "Record {0} of {1}".format(n, total_records)
            delimiter()
        print "Summary:\n\tRecords completed:\t\t{0}\n\tRecords trunked:\t\t{1}\n\tRecords not changed:\t\t{2}\n\tTotal Records:\t\t\t{3}".format(total_completed, total_trunked, total_not_changed, total_records)
        return records_to_modified

def delimiter(string="="):
    '''
    Print delimiter
    '''
    print string*50

config = {
    'HOST' : 'localhost',
    'PORT' : 27017,
    'USER_ID' : 414
}

ids_to_migrate = {
    #Fecha
    '000000000000000000000001' : [
        '5589a03701a4de7bba84fb2f',
        '5589a09c01a4de7bba84fb4d',
        '5589a0bc01a4de7bba84fb55',
        '552fdbf501a4de288f4275e8',
        '552fc75201a4de289005537b',
        '5592abc201a4de7bba852a0f',
        '552fc35b01a4de288f4275cf',
        '552e89ae01a4de288eebef32',
        '552e89da01a4de28900552ed',
        '55899c9401a4de2ea94629e7',
        '55899ce801a4de2ea94629f4',
        '552fc36801a4de2890055363'
    ],
    
    #Granja
    '000000000000000000000002' : [
        '5589a03701a4de7bba84fb30',
        '5589a09c01a4de7bba84fb4e',
        '5589a0bc01a4de7bba84fb56',
        '552fdbf501a4de288f4275e9',
        '552fc75201a4de289005537c',
        '5592abc201a4de7bba852a10',
        '552fc35b01a4de288f4275d0',
        '552e89ae01a4de288eebef33',
        '552e89da01a4de28900552ee',
        '55899c9401a4de2ea94629e8',
        '55899ce801a4de2ea94629f5',
        '552fc36801a4de2890055364'
    ],
    
    #Total de Muertos
    '000000000000000000000003' : [
        '5589a03701a4de7bba84fb32',
        '5589a09c01a4de7bba84fb50',
        '5589a0bc01a4de7bba84fb58',
        '552fdbf501a4de288f4275ee',
        '552fc75201a4de2890055381',
        '5592abc201a4de7bba852a12',
        '552fc35b01a4de288f4275d5',
        '552e89ae01a4de288eebef38',
        '552e89da01a4de28900552f3',
        '55899c9401a4de2ea94629ea',
        '55899ce801a4de2ea94629f7',
        '552fc36801a4de2890055369'
    ],    
}


if __name__ == '__main__':
    db = Database(config['HOST'], config['PORT'], config['USER_ID'])
    db.create_user_connection()
    collection = db.get_collection('form_answer')
    records = db.replace_ids_in_records_at_collection(ids_to_migrate, collection)
    result = db.update_records_at_collection(records, collection)
    if result:
        print "> Updated correctly."
    else:
        print "> Updated incorrectly."
