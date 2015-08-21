#coding: utf-8
#Created by jpv

from lxml import etree
from pymongo import MongoClient
from pymongo.collection import Collection
import os

##### TODO 
##### no incluirl los campos tipo grupo 
##### no incluirl los campos  que no tengan descripcion
##### Campos con nombres repetitivos irles agregando un consecutivo. 1,2,3... N

class dataDesignFactory(object):

    def __init__(self, host='localhost', port=27019):
        self.SOURCE_ID = 2
        self.host= host
        self.port = port
        self.collectionName = "form_answer"
        self.analysis_type = {'radio':'dimension',
                            'checkbox':'dimension',
                            'select':'dimension',
                            'text':'dimension',
                            'textarea':'dimension',
                            'email':'dimension',
                            'password':'dimension',
                            'decimal': 'measure',
                            'integer':'measure',
                            'date':'dimension',
                            'datetime':'dimension',
                            'time':'dimension',
                            'geolocation':'dimension'}
        self.dataType = {'radio':'string',
                        'checkbox':'string',
                        'select':'string',
                        'text':'string',
                        'textarea':'string',
                        'email':'string',
                        'password':'string',
                        'integer':'integer',
                        'decimal': 'decimal',
                        'date':'date',
                        'datetime':'date-time',
                        'time':'time',
                        'geolocation':'string'
                        }
        self.skiptypes = ['image','signature', 'file', 'description','group']


    def getXmlRoot(self, root="root", attributs={}):
        root = etree.Element(root,attributs)
        return root

    def printXML(self, xml):
        print(etree.tostring(xml, pretty_print=True))

    def get_user_connection(self, user_id):
        connection = {}
        connection['client'] = MongoClient('mongodb://%s:%d'%(self.host, self.port))
        user_db_name = "infosync_answers_client_{0}".format(user_id) 
        if not user_db_name:
            return None
        connection['db'] = connection['client'][user_db_name]   
        return connection

    def get_infosync_connection(self):
        try:
            connection = MongoClient('mongodb://%s:%d'%(self.host, self.port))
            #connects to the database infosync
            db_infosync = connection.infosync
            #connects to the collection form_data
            form_data = db_infosync.form_data
        except:
            return 'No connection to Mongo'
        return form_data

    def getForm(self, form_id):
        form_data = self.get_infosync_connection()
        form = form_data.find_one({'form_id':form_id})
        return form 

    def getMongoFields(self, items_to_search):
        id_label = {}
        for field in items_to_search:
            #form = self.getForm(form_id)
            if field['field_type'] in self.skiptypes:
                continue
            id_label[field['field_id']] = field['label'] 
        return id_label

    def setChildNode(self, elemnet, tag, attributs={}, text=None):
        #element is an etree element
        #tag is the name of the child node
        #attributs is a dict with the key, value pairs of the attributs to have
        #text is the text that the child node will have
        structure_property = etree.SubElement(elemnet, tag)
        for key, value in attributs.iteritems():
            structure_property.set(key, value)
        if text:
            structure_property.text = text
        return structure_property

    def getColumnHintsSctructure(self, structure, field_id, label, field_type='text'):
        #analysis_type = self.getAnalysisType()
        self.setChildNode(structure, "property", {"name":"columnName"}, "answers.%s"%field_id)
        self.setChildNode(structure, "property", {"name":"alias"}, label)
        atype = self.analysis_type.get(field_type,'dimension')
        self.setChildNode(structure, "property", {"name":"analysis"}, atype)
        self.setChildNode(structure, "text-property", {"name":"displayName"}, label)
        self.setChildNode(structure, "text-property", {"name":"heading"}, label)
        self.setChildNode(structure, "property", {"name":"indexcolumn"}, "false")
        self.setChildNode(structure, "property", {"name":"compressed"}, "false")
        return structure

    def get_metadata_columns(self):
        metadata_fields = {
            'browser':'Browser',
            'created_at':'Created At',
            'duration':'Duration',
            'end_date':'End Date',
            'folio':'Folio',
            'geolocation':'Geolocation',
            'ip':'IP Address',
            'plataform':'Plataform',
            'start_date':'Start Date',
            'updated_at':'Updated At',
            'user_id':'User ID',
            'version':'Version'
        }
        return metadata_fields

    def list_property_columnHints(self, data_sets_element, form):
        list_poroperty = etree.SubElement(data_sets_element, "list-property")
        list_poroperty.set("name","columnHints" )
        #root = getXmlRoot('list-property', {"name":"columnHints"})
        if form:
            for field in form['fields']:
                if field['field_type'] in self.skiptypes:
                    continue
                structure = etree.SubElement(list_poroperty, "structure")
                structure = self.getColumnHintsSctructure(structure, field['field_id'], field['label'], field['field_type'])
        return data_sets_element

    def getResultSetSctructure(self, structure, position, label, field_type='text'):
        #analysis_type = getAnalysisType()
        self.setChildNode(structure, "property", {"name":"position"}, str(position))
        self.setChildNode(structure, "property", {"name":"name"}, label)
        atype = self.dataType.get(field_type,'string')
        self.setChildNode(structure, "property", {"name":"dataType"}, atype)
        return structure

    def getResultSetSctructureExtras(self, structure_resultSet, field_id, field_type='text'):
        #analysis_type = getAnalysisType()
        self.setChildNode(structure_resultSet, "property", {"name":"nativeName"}, field_id )
        self.setChildNode(structure_resultSet, "property", {"name":"nativeDataType"}, "2")
        return structure_resultSet

    def list_property_resultSet(self, data_sets_element, form, client_name):
        cachedMetaData_structure = etree.SubElement(data_sets_element, "structure")
        cachedMetaData_structure.set("name", "cachedMetaData")

        data_sets_property = etree.SubElement(data_sets_element, "property")
        data_sets_property.set("name", "dataSource")
        data_sets_property.text = "Data Source: " + client_name

        list_poroperty = etree.SubElement(cachedMetaData_structure, "list-property")
        list_poroperty.set("name","resultSet" )

        list_poroperty_resultSet = etree.SubElement(data_sets_element, "list-property")
        list_poroperty_resultSet.set("name","resultSet" )

        #root = self.getXmlRoot('list-property', {"name":"resultSet"})
        if form:
            position = 1
            for field in form['fields']:
                if field['field_type'] in self.skiptypes:
                    continue
                structure = etree.SubElement(list_poroperty, "structure")
                structure = self.getResultSetSctructure(structure, position, field['label'], field['field_type'])

                structure_resultSet = etree.SubElement(list_poroperty_resultSet, "structure")
                structure_resultSet = self.getResultSetSctructure(structure_resultSet, position, field['label'], field['field_type'])
                structure_resultSet = self.getResultSetSctructureExtras(structure_resultSet, str(field['field_id']), field['field_type'])
                
                position += 1 
        
        return data_sets_element 


    def getSelectedField(self, fields):
        selectedFields = []
        for field in fields:
            if field['field_type'] in self.skiptypes:
                    continue
            selectedFields.append("answers." + str(field['field_id']))
        return selectedFields

    def getMongoOperation(self, form_id, collectionName, selectedFields=[]):
        query = {}
        query["operationExpr"] = "[{$match:{form_id:%s}}]"%(form_id)
        query["operationType"] = "AGGREGATE"
        query["selectedFields"] = selectedFields
        query["collectionName"] = collectionName
        query_string = str(query)
        query_string = query_string.replace("'", '"')
        return str(query_string)

    def getQueryText(self, data_sets_element, form):
        list_poroperty = etree.SubElement(data_sets_element, "xml-property")
        list_poroperty.set("name","queryText" )
        selectedFields = self.getSelectedField(form['fields'])
        cData_string = self.getMongoOperation(str(form['form_id']), self.collectionName, selectedFields)
        list_poroperty.text = etree.CDATA(cData_string)
        #root = getXmlRoot('list-property', {"name":"columnHints"})
        return data_sets_element

    def setDesignerState(self, data_sets_element):
        structure = self.setChildNode(data_sets_element, "structure", {"name":"designerState"})
        self.setChildNode(structure, "property", {"name":"version"}, "1.0")
        self.setChildNode(structure, "property", {"name":"stateContentAsString"}, "false,100")
        return data_sets_element

    def setDesignerValues(self, data_sets_element, form):
        list_poroperty = etree.SubElement(data_sets_element, "xml-property")
        list_poroperty.set("name","designerValues" )
        cData_string = self.getDesignerValues(form)
        list_poroperty.text = etree.CDATA(cData_string)
        return data_sets_element

    def getDesignerValues(self, form):
        text = """<?xml version="1.0" encoding="UTF-8"?>
<model:DesignValues xmlns:design="http://www.eclipse.org/datatools/connectivity/oda/design" xmlns:model="http://www.eclipse.org/birt/report/model/adapter/odaModel">
  <Version>2.0</Version>
  <design:ResultSets derivedMetaData="true">
  </design:ResultSets>
</model:DesignValues>"""
        return text

    def setDefaults(self):
        xml_header = '<?xml version="1.0" encoding="UTF-8"?>'
        XHTML_NAMESPACE  = "http://www.eclipse.org/birt/2005/design"
        XHTML = "{%s}" % XHTML_NAMESPACE
        NSMAP = {None : XHTML_NAMESPACE}
        VERSION = "3.2.23"
        ID = "1"
        xhtml = etree.Element(XHTML + "datamart", nsmap=NSMAP, version=VERSION, id=ID)
        return xhtml
     
    def setProperties(self, datadesign):
        propperty_tag = etree.SubElement(datadesign, "property")
        propperty_tag.set("name","createdBy")
        propperty_tag.text = "Eclipse BIRT Designer Version 4.4.0.v20150206-1039 Build &lt;4.2.3.v20150206-1039>"
        return propperty_tag

         #<property name="createdBy">Eclipse BIRT Designer Version 4.4.0.v20150206-1039 Build &lt;4.2.3.v20150206-1039></property>

    def dataSources(self, datadesign, database_source):
        data_sources_element = etree.SubElement(datadesign, "data-sources")
        for database in database_source:
            database['id'] = str(self.SOURCE_ID)
            self.SOURCE_ID += 1
            self.setDataSource(data_sources_element, database)
        return datadesign

    def setDataSource(self, data_sources_element, dataSourceDict):
        properties = dataSourceDict.pop("properties", None)
        source = self.setChildNode(data_sources_element, "oda-data-source", dataSourceDict)
        if properties:
            for parameter, text in properties.iteritems():
                self.setChildNode(source, "property", {"name":parameter}, text)
        return data_sources_element

    def dataSets(self, datadesing, datasets, client_name):
        data_sets_element = etree.SubElement(datadesing, "data-sets")
        for dataset in datasets:
            dataset['id'] = str(dataset["form_id"])
            #dataset['id'] = str(self.SOURCE_ID)
            self.SOURCE_ID +=1
            self.setDataSet(data_sets_element, dataset, client_name)
        return datadesing

    def setDataSet(self, data_sets_element, dataSetDict, client_name):
        properties = dataSetDict.pop("properties", None)
        form_id = dataSetDict.pop("form_id", None)
        dset_element = self.setChildNode(data_sets_element, "oda-data-set", dataSetDict)
        if properties:
            for parameter, text in properties.iteritems():
                print 'parameter', parameter
                self.setChildNode(dset_element, "property", {"name":parameter}, text)
        #sets property columnHints
        if form_id:
            form = self.getForm(form_id)
            data_sets_element = self.list_property_columnHints(dset_element, form)
            data_sets_element = self.list_property_resultSet(dset_element, form, client_name)
            data_sets_element = self.getQueryText(dset_element, form)
            data_sets_element = self.setDesignerState(dset_element)
            data_sets_element = self.setDesignerValues(dset_element, form)

            #data_sets_property = self.setChildNode(data_sets_element, "property", {"name":"dataSource"}, "Data Source: " + str(form_id))
        return data_sets_element