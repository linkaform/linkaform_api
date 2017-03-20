# coding: utf-8
#!/usr/bin/python
import time
import requests
import simplejson
import os, re

from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime
from sys import stderr, argv

from re import findall

#linkaform api
import settings
from forms import Form
from urls import api_url
from settings import config
from file_loader import load_answers, get_files_from_path, file_is_catalogo
import network


# ENUMS
class FieldType:
    GROUP_FIELD = 1
    ONE_FIELD = 2



class ImportData:
    MONGO = 1
    REST = 2


if __name__ == "__main__":
    all_files = get_files_from_path()
    print 'all_files', all_files
    try:
        test = argv[1]
    except:
        test = False
    for file_name in all_files:
        if file_name:
            file_path = config['FILE_PATH_DIR'] + file_name
            #print "Filename: {0}".format(file_path)
            time_started = time.time()
            metadata = {
                'form_id' : None,
                'lat' : 25.644885499999997,
                'glong' : -100.3862645,
                'start_timestamp' : 123456789,
                'created_at' : None,
                'is_catalog': file_is_catalogo(file_path),
            }
            answers = load_answers(metadata, file_path)
            print "Total answers: ",len(answers)
            try:
                print "Sample of answers:"
                print answers[0]
                print answers[1]
                print answers[2]
                # print answers[3]
            except:
                pass
            if len(answers) > 0:
                print "%s answers loaded." % len(answers)
                if settings.config['LOAD_DATA_USING'] == ImportData.MONGO:
                    network.upload_answers_to_database(answers)
                elif settings.config['LOAD_DATA_USING'] == ImportData.REST:
                    network.post_forms_answers(answers, test)
                else:
                    raise ValueError("LOAD_DATA_USING {0} is invalid".format(settings.config['LOAD_DATA_USING']))
            else:
                 "No answers loaded."
    if test or len(settings.GLOBAL_ERRORS):
        print '=================== TEST RESULTS ================================'
        print 'total errors', len(GLOBAL_ERRORS)
        for error in settings.GLOBAL_ERRORS:
            print error
