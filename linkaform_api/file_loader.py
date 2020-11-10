# coding: utf-8
#!/usr/bin/python
import os, re


#linkaform api
from utils import Cache
from forms import Form, Catalog, Item
from urls import api_url
import settings


def get_files_from_path():
    files = os.popen('ls %s*.csv' % settings.config['FILE_PATH_DIR'])
    all_files = files.read().split('\n')
    file_names = [file[len(settings.config['FILE_PATH_DIR']):] for file in all_files]
    return file_names

def load_answers(metadata, file_path):
    print('file_path', file_path)
    load_file = get_file_to_import(file_path)
    answers = []
    item = Item(
        **{
            "file_name" : file_path,
            "form_id" : metadata['form_id'],
            "is_catalog": metadata['is_catalog'],
            "geolocation" : [metadata['lat'], metadata['glong']],
            "start_timestamp" : metadata['start_timestamp'],
            "end_timestamp" : metadata['start_timestamp'],
            "created_at" : metadata['created_at'],
            #"answers" : answer_line
        }
    )
    if item.form_id:
        form = Form(
            **{
                "file_name" : file_path,
                "form_id" : metadata['form_id'],
                "is_catalog": metadata['is_catalog'],
                "geolocation" : [metadata['lat'], metadata['glong']],
                "start_timestamp" : metadata['start_timestamp'],
                "end_timestamp" : metadata['start_timestamp'],
                #"created_at" : metadata['created_at'],
                #"answers" : answer_line
            }
        )
        answer_metadata = form.get_form()
    if item.catalog_id:
        answer_metadata = {'catalog_id': item.catalog_id}
    print('load_file', load_file)
    for answer_line in load_file:
        print('answer_line', answer_line)
        line = item.get_answers(answer_line)
        print(' line', line)
        print(ds)
        if item.catalog_id:
            line = {'answers':line}
        line.update(answer_metadata)
        answers.append(line)
    print('============= ALL RECORDS LOADED ======== ')
    return answers

def get_file_to_import(file_path):
    answers = []
    with open(file_path) as file:
        headers = file.readline().strip().split(',')
        for line in file:
            line = line.strip().split(',')
            field_map = zip(headers, line)
            answers.append(dict(field_map))
    return answers

def file_is_catalogo(file_path):
    prefix = file_path.split('_')[0]
    if prefix == 'catalogo' or prefix == 'catalog':
        return True
    elif 'catalogo' in file_path:
        return True
    elif 'catalog' in file_path:
        return True
    else:
        return False
