#!/bin/python

#### MongoDB Dump and Restore Script
#### This is the first draft.....


client_id =96 


mongodump ='mongodump -d infosync_answers_client_%s --out /var/tmp/mongo_back_client_%s'%(client_id,client_id)
removedir = 'rm -rf /var/tmp/mongo_back_client_%s'%(client_id)
dotar = 'tar -zcvf /var/tmp/mongo_back_client_%s.tar.gz ./mongo_back_client_%s'%(client_id,client_id)
remove = 'rm -rf /var/tmp/mongo_back_client_%s'%(client_id)
copy_tar = 'scp grover.info-sync.com:/var/tmp/mongo_back_client_%s.tar.gz /var/tmp/'%(client_id)
untar = 'tar -zxvf mongo_back_client_%s.tar.gz'%(client_id)
restore = ' mongorestore /var/tmp/mongo_back_client_%s'%client_id

print '--------- remote host ------------'
print 'cd /var/tmp/'
print removedir
print mongodump
print dotar
print remove
print '---------- on localhost------------'
print 'cd /var/tmp/'
print copy_tar
print untar
print restore
print 'done=================='
