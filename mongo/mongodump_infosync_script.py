#!/bin/python

#### MongoDB Dump and Restore Script
#### This is the first draft.....


client_id =414
server ='db4.linkaform.com'

mongodump ='mongodump -d infosync_answers_client_%s --host db4.linkaform.com --out /var/tmp/mongo_back_client_%s'%(client_id,client_id)
removedir = 'rm -rf /var/tmp/mongo_back*'
dotar = 'tar -zcvf /var/tmp/mongo_back_client_%s.tar.gz ./mongo_back_client_%s'%(client_id,client_id)
remove = 'rm -rf /var/tmp/mongo_back_client_%s'%(client_id)
copy_tar = 'scp %s:/var/tmp/mongo_back_client_%s.tar.gz /var/tmp/'%(server,client_id)
untar = 'tar -zxvf mongo_back_client_%s.tar.gz'%(client_id)
restore = 'mongorestore /var/tmp/mongo_back_client_%s'%client_id
print '--------- remote host ------------'
print 'ssh %s'%(server)
print 'cd /var/tmp/'
print removedir
print mongodump
print dotar
print remove
print '---------- on localhost------------'
print 'cd /var/tmp/'
print removedir
print copy_tar
print untar
print restore
print 'done=================='
