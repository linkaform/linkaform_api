#!/bin/python

#### MongoDB Dump and Restore Script
#### This is the first draft.....


client_id=900
server ='db3.linkaform.com'
host_port='10.1.66.32:27032'
# client_id =126
# server ='db2.linkaform.com'

mongodump ='mongodump -d infosync_answers_client_%s --host %s --out /var/tmp/mongo_back_client_%s'%(client_id,server,client_id)
removedir = 'rm -rf /var/tmp/mongo_back*'
dotar = 'tar -zcvf /var/tmp/mongo_back_client_%s.tar.gz ./mongo_back_client_%s'%(client_id,client_id)
remove = 'rm -rf /var/tmp/mongo_back_client_%s'%(client_id)
copy_tar = 'scp %s:/var/tmp/mongo_back_client_%s.tar.gz /var/tmp/'%(server,client_id)
untar = 'tar -zxvf mongo_back_client_%s.tar.gz'%(client_id)
restore = 'mongorestore /var/tmp/mongo_back_client_%s'%(client_id)
print '--------- remote host ------------'
print 'ssh %s'%(server)
print 'cd /var/tmp/'
print removedir
print mongodump
print dotar
print remove
print 'exit'
print '---------- on localhost------------'
print 'cd /var/tmp/'
print removedir
print copy_tar
print untar
print 'mongo'
print 'use infosync_answers_client_%s'%(client_id)
print 'db.dropDatabase()'
print 'exit'
print restore
print 'done=================='
# print 'scp %s:/var/tmp/mongo_infosync_back.tar.gz /var/tmp/'%(server)
# print 'tar -zxcf mongo_infosync_back.tar.gz'
# print 'mongorestore --host %s /var/tmp/mongo_infosync_back'%(host_port,client_id)
