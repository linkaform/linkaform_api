e
# -*- coding: utf-8 -*-
#!/usr/bin/python

#####
# Made by Jose Patricio VM
#####
# Script para generar pacos a partir de ordenes de Servicio de PCI Industrial
#
#
#####
import wget
import pyexcel
import datetime, time, re
from sys import argv
import simplejson

from linkaform_api import network, utils, settings

#Nombre del campo en la la Forma: Nombre en el Archvio

class LoadFile:

    def __init__(self, settings={}):
        self.settings = settings
        self.lkf_api = utils.Cache(settings)
        self.net = network.Network(settings)
        #self.cr = self.net.get_collections()


    def read_file(self, file_url='', file_name=''):
        #sheet = pyexcel.get_sheet(file_name="bolsa.xlsx")
        if file_name:
            sheet = pyexcel.get_sheet(file_name = file_name)
        if file_url:
            sheet = pyexcel.get_sheet(url = file_url)
        records = sheet.array
        header = records.pop(0)
        header = [str(col).lower().replace(u'\xa0',u' ').strip().replace(' ', '_') for col in header]
        return header, records


    def convert_to_epoch(self, strisodate):
        if type(strisodate) == datetime.date or type(strisodate) == datetime.datetime:
            return time.mktime(strisodate.timetuple())
        strisodate2 = re.sub(' ','',strisodate)
        strisodate2 = strisodate2.split(' ')[0]
        try:
            date_object = datetime.strptime(strisodate2, '%Y-%m-%d')
        except ValueError:
            date_object = datetime.strptime(strisodate2[:8],  '%d/%m/%y')
        return int(date_object.strftime("%s"))


    def convert_to_sting_date(self, strisodate):
        if type(strisodate) == datetime.date:
            return strisodate
        strisodate2 = re.sub(' ','',strisodate)
        strisodate2 = strisodate2.split(' ')[0]
        try:
            date_object = datetime.strptime(strisodate2, '%Y-%m-%d')
        except ValueError:
            try:
                date_object = datetime.strptime(strisodate2[:10],  '%d/%m/%Y')
            except ValueError:
                date_object = datetime.strptime(strisodate2[:8],  '%d/%m/%y')
        return date_object.strftime('%Y-%m-%d')


    def convert_to_sting_date(self, field):
        res = {'field_id':field['field_id'], 'field_type':field['field_type'], 'label':field['label'], 'options':field['options']}
        if field.has_key('group') and field['group']:
            res['group_id'] = field['group']['group_id']
        return res


    def make_header_dict(self, header):
        header_dict = {}
        for position in range(len(header)):
            content = header[position].encode('utf-8')
            if str(content).lower().replace(' ' ,'') in header_dict.keys():
                continue
            header_dict[str(content).lower().replace(' ' ,'')] = position
        return header_dict


    def get_pos_field_id_dict(self, header, form_id, equivalcens_map={}):
        #form_id=10378 el id de bolsa
        #pos_field_id ={3: {'field_type': 'text', 'field_id': '584648c8b43fdd7d44ae63d1'}, 9: {'field_type': 'text', 'field_id': '58464a29b43fdd773c240163'}, 51: {'field_type': 'integer', 'field_id': '584648c8b43fdd7d44ae63d0'}}
        #return pos_field_id
        pos_field_id = {}
        form_fields = self.lkf_api.get_form_id_fields(form_id)
        if not form_fields:
            raise ValueError('No data form FORM')
        header_dict = self.make_header_dict(header)
        aa = False
        assigne_headers = []
        if len(form_fields) > 0:
            fields = form_fields[0]['fields']
            fields_json = {}
            if 'folio' in header_dict.keys():
                pos_field_id[header_dict['folio']] = {'field_type':'folio'}
            elif equivalcens_map.has_key('folio'):
                for eq_opt in  equivalcens_map['folio']:
                    if eq_opt in header_dict.keys():
                        pos_field_id[header_dict[eq_opt]] = {'field_type':'folio'}
            for field in fields:
                label = field['label'].lower().replace(' ' ,'')
                label_underscore = field['label'].lower().replace(' ' ,'_')
                if label in header_dict.keys():
                    if label in assigne_headers:
                        continue
                    assigne_headers.append(label)
                    pos_field_id[header_dict[label]] = self.convert_to_sting_date(field)
                elif label_underscore in header_dict.keys():
                    if label in assigne_headers:
                        continue
                    assigne_headers.append(label)
                    pos_field_id[header_dict[label_underscore]] = self.convert_to_sting_date(field)
                elif field['label'] in equivalcens_map.keys():
                    header_lable = equivalcens_map[field['label']]
                    header_lable = header_lable.lower().replace(' ' ,'')
                    if header_lable in header_dict.keys():
                        if label in assigne_headers:
                            continue
                        assigne_headers.append(label)
                        pos_field_id[header_dict[header_lable]] = self.convert_to_sting_date(field)
        return pos_field_id


    def set_custom_values(self, pos_field_id, record):
        custom_answer = {}
        #set status de la orden
        #custom_answer['f1054000a030000000000002'] = 'por_asignar'
        return custom_answer


    def update_metadata_from_record(self, header, record):
        res = {}
        if 'created_at' in header.keys():
            pos = header['created_at']
            if record[pos]:
                #res['created_at'] = self.convert_to_sting_date(record[pos])
                res['created_at'] = convert_to_epoch(record[pos])
        if 'form_id' in header.keys():
            pos = header['form_id']
            if record[pos]:
                res['form_id'] = record[pos]
        return res


    def get_nongroup_fields(self, pos_field_id):
        res = []
        for pos, element in pos_field_id.iteritems():
            if element.has_key('group_id') and element['group_id']:
                continue
            else:
                res.append(pos)
        return res


    def check_record_is_group_iterration(self, non_group_fields, record):
        for pos in non_group_fields:
            if record[pos]:
                return False
        return True


    def prepare_record_list(self, pos_field_id, form_id, records, header):
        records_to_upload = []
        metadata = self.lkf_api.get_metadata(form_id=form_id, user_id=self.settings.config['USER_ID'] )
        header_dict = self.make_header_dict(header)
        non_group_fields = self.get_nongroup_fields(pos_field_id)
        print 'len records', len(records)
        for record in records:
            is_group_iteration = self.check_record_is_group_iterration(non_group_fields, record)
            is_group_iteration = False
            metadata.update(self.update_metadata_from_record(header_dict, record))
            cont = False
            answer = {}
            this_record = {}
            count = 0
            this_record.update(metadata)
            group_iteration = {}
            for pos, element in pos_field_id.iteritems():
                count +=1
                if element['field_type'] == 'folio':
                    this_record['folio'] = str(record[pos])
                else:
                    element_answer = self.lkf_api.make_infosync_json(record[pos], element)
                    if element.has_key('group_id') and element['group_id'] and element_answer:
                        if not answer.has_key(element['group_id']):
                            answer[element['group_id']] = []
                        #answer.update(element_answer)
                        if not group_iteration.has_key(element['group_id']):
                            group_iteration[element['group_id']] = {}
                        group_iteration[element['group_id']].update(element_answer)
                    else:
                        answer.update(element_answer)
            #answer[element['group_id']].append(group_iteration)
            answer.update(self.set_custom_values(pos_field_id, record ))
            if is_group_iteration:
                last_rec = records_to_upload[-1]
                for group_id  in group_iteration.keys():
                    last_rec['answers'][group_id].append(group_iteration[group_id])
                records_to_upload[-1] = last_rec
            else:
                for group_id  in group_iteration.keys():
                    answer[group_id].append(group_iteration[group_id])
                this_record["answers"] = answer
                records_to_upload.append(this_record)
        return records_to_upload


    def create_record(self, records_to_create):
        error_list = self.net.post_forms_answers_list(records_to_create)
        return error_list


    def remove_splecial_characters(self, text, replace_with='', remove_spaces=False):
        if type(text) == str:
            text = text.replace('\xa0', replace_with)
            text = text.replace('\xc2',replace_with)
            if remove_spaces:
                text = text.strip()
        if type(text) == unicode:
            text = text.replace(u'\xa0', replace_with)
            text = text.replace(u'\xc2', replace_with)
            if remove_spaces:
                text = text.strip()
        return text


    def remove_splecial_characters_list(self, text_list):
        res = []
        for text in text_list:
            res.append(self.remove_splecial_characters(text, '', True))
        return res


    def get_file_to_upload(self, file_url='', file_name='', form_id=None, equivalcens_map={}):
        if not form_id:
            raise ValueError('Must specify form id')
        if not file_url and not file_name:
            raise ValueError('Must specify either one, file_url or file_name')
        if file_url:
            header, records = self.read_file(file_url=file_url)
        elif file_name:
            header, records = self.read_file(file_name=file_name)
        header = self.remove_splecial_characters_list(header)
        return header, records


    def upload_file(self, file_url='', file_name='', form_id=None, equivalcens_map={}):
        header, records = self.get_file_to_upload(file_url=file_url, file_name=file_name, form_id=form_id, equivalcens_map=equivalcens_map)
        pos_field_id = self.get_pos_field_id_dict(header, form_id, equivalcens_map)
        records_to_upload = self.prepare_record_list(pos_field_id, form_id, records, header)
        error_list = self.create_record(records_to_upload)
        return error_list


    def print_help(self):
        print '---------------- HELP --------------------------'
        print 'more arguments needed'
        print 'the script should be run like this'
        print '''python upload_excel_file.py '{"file_name":"/tmp/personal.xlsx", "form_id":"1234", "equivalcens_map":{"foo":"bar"}}' '''
        print '* form_id: where 1234 is the id of the form, is a requierd argument'
        print '** file_name: file in you local machine'
        print '** file_url: file on a remote url'
        print 'if running from console you shoud send the settings json a second argument'
        print 'running from console example'
        print ''''python upload_excel_file.py '{"file_name":"/tmp/personal.xlsx", "form_id":"1234", "equivalcens_map":{"foo":"bar"}} '{"USERNAME": "mike"}' '''


if __name__ == "__main__":
    if len(argv) > 1:
        config = simplejson.loads(argv[1])
        if argv[1] == 'help' or argv[1] == '--help':
            LoadFile(settings).print_help()
        elif not config.has_key('form_id'):
            LoadFile(settings).print_help()
        elif not config.has_key('file_name') and not config.has_key('file_url'):
            LoadFile(settings).print_help()
        else:
            try:
                if argv[2]:
                    settings.config.update(simplejson.loads(argv[2]))
            except IndexError:
                import settings
            load_files = LoadFile(settings)
            load_files.upload_file(config.get('file_url'), config.get('file_name'),
                config.get('form_id'), config.get('equivalcens_map'))
    else:
        LoadFile(settings).print_help()
