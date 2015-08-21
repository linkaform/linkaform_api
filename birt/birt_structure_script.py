
form = getForm(form_id, host, port)

form_id = 1
form_id=2050 #iesa
form_id = 2712 #produccion sanfandilia
form_id = 792 # Forma Rentokil QAI

form_list = [2712,2713,2810]
form_list = [2712,]

client_id = 96 # IESA
client_id = 101 # Rentokil


#Sanfandila
client_id = 414 #Sanfandila
client_name = "Sanfadilia"
form_list = [2989,]
form_list = [3091,]
form_list = [2654,2652,2638,2667,2639,2650] #mortandad
form_list = [3406,3407,3408] #mortandad huajotes

#InfoSync
client_id = 126
form_list = [3032,]
client_name = "Infosync"
form_list = [3153,3150,3155]
form_list = [3370,]

#InfoSync
client_id = 126
form_list = [3032,]
client_name = "Infosync"
form_list = [3153,3150,3155]
form_list = [3365,]


#Logistorage
client_id = 516
form_list = [3370,]
client_name = "Logistorage"
# 3509 cliente 516 de Logistorage
form_list = [3509,3448, 3447]
form_list = [3486,]


database_source_dict = [({"name": "Data Source: " + client_name,
                "extensionID":"org.eclipse.birt.data.oda.mongodb",
                "properties":{
                "mongoURI":"mongodb://meseta:Meseta.94@127.0.0.1:27019/infosync_answers_client_%s"%(client_id),
                "ignoreURI":"false", 
                "serverPort":"27017",
                "socketKeepAlive":"true", 
                "useRequestSession":"true"}}),]

#builds datasource
from dataDesignFactory import dataDesignFactory as df
from lxml import etree
data = df()

datadesign = data.setDefaults()
property_1 = data.setProperties(datadesign)
datadesign = data.dataSources(datadesign, database_source_dict)

for form_id in form_list:
    dataset_dict = [({"name": "Data Set:%s"%(form_id),
                 "extensionID":"org.eclipse.birt.data.oda.mongodb.dataSet",
                 "form_id":form_id})]
    datadesing = data.dataSets(datadesign, dataset_dict, client_name)

data.printXML(datadesign)

final_string = etree.tostring(datadesign, encoding='UTF-8', pretty_print=True)

#final_string += etree.tostring(cachedMetaData, encoding='UTF-8', pretty_print=True)

xml_file = open("%s_%s.datadesign"%(client_name,form_id),'w' )
xml_file.write(final_string)
xml_file.close()





resultSet =  data.list_property_resultSet(form)



cachedMetaData = getXmlRoot('structure', {"name":"cachedMetaData"})

#builds the ColumnHints section

#builds the cachedMetaData section
cachedMetaData.append(resultSet)





file_path = '/home/josepato/infosync/reportes-birt/InfoSync/Soluciones/Plagas/Reporte SPC os.rptdesign'

xml_file = open(file_path, 'r')
tree = etree.parse(xml_file)
