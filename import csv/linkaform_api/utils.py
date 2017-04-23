# coding: utf-8
#!/usr/bin/python

from forms import Form

class Cache(object):

    def __init__(self):
        self.items = {}

    def get(self, item_type, item_id):
        if not self.items.has_key(item_type):
            self.items[item_type] = self.get_items(item_type)
        if not self.items[item_type].has_key(item_id):
            self.items[item_type][item_id] = get_items_from_somewhere()
        return self.items['type'][item_id]

    def get_all_items(self, item_type):
        if item_type =='form':
            return Form.get_all_forms('GET_FORMS')
        if item_type == 'catalog':
            return Form.get_all_forms('GET_CATALOGS')

    def get_item_id(self, item_type, item_id):
            if item_type =='form':
                return Form.get_forms_id('GET_FORMS', item_id)
            if item_type == 'catalog':
                return Form.get_catalog_id('GET_CATALOGS', item_id)

def warning(*objs):
    '''
    To print stuff at stderr
    '''
    output = "warning:%s\n" % objs
    stderr.write(output)
