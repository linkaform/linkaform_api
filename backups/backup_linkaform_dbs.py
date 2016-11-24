# coding: utf-8

__author__ = "josepato.villarreal"
"""
Script para automatizar los respaldos de las base de datos de Linkaform:
"""

import os
from sys import argv
from datetime import datetime

from cuisine import *
from fabric.api import env, execute, task
from fabric import operations
from cuisinepostgresql import cuisine_postgresql as cp

development_server = 'slimey.linkaform.com'
production_server = 'backend.linkaform.com'


#TODO:
#PUT PASSWORDS ON FIELS

USERNAME = os.popen('whoami').readline()[:-1]
key_filename = '/home/%s/.ssh/id_rsa'%(USERNAME)

def set_enviorment(ssh_args):
    if ssh_args.has_key('server'):
        env.host_string = ssh_args['server']
    if ssh_args.has_key('username'):
        env.user = ssh_args['username']
    if ssh_args.has_key('key_filename'):
        env.key_filename = ssh_args['key_filename']
    if ssh_args.has_key('port'):
        env.port = 2222


#@task
def backup_postgres_linkaform(production_server, key_filename, dbname, dbhost='127.0.0.1', dbport=5432):
    """
    Crear un archivo tar de directorio remoto
    """
    username = 'infosync'

    ## Va a hacer el respaldo de produccion
    dbname_prod='infosync'
    server_args = {'server':production_server, 'username':username, 'key_filename':key_filename}
    dbbackupd_name = cp.postgres_backup(dbname_prod, dbhost, dbport, ssh_args=server_args)
    file_name = dbbackupd_name.split('/')[-1]
    file_path = dbbackupd_name.strip(file_name)

    # Va a develop copia base de datos, borra la actual y restaura con la nueva
    server_args = {'server':development_server, 'username':username, 'key_filename':key_filename, 'port':2222}
    set_enviorment(server_args)
    dbname_dev='infosync_prod'

    cp.postgres_dropdb(dbname_dev, username, dbhost='10.1.66.19', ssh_args=server_args)
    cp.postgresql_database_create(dbname_dev, encoding='UNICODE' , owner=username, dbhost='10.1.66.19', ssh_args=server_args )

    dir_ensure(file_path)
    print '================'
    run("scp  infosync@%s:%s %s"%(production_server, dbbackupd_name, file_path))
    cp.postgres_restoredb(dbname_dev, dbbackupd_name , username=username, dbhost='10.1.66.19', ssh_args=server_args)
    #cp.postgresql_database_create(dbname, development_server, key_filename,
    #                              username, encoding='UNICODE', owner=username)
    #cp.postgres_restoredb(development_server, key_filename, username, dbname, dbhost='10.1.66.19', dbport='5434')
    return True


@task
def backup_public_html(key_filename='/home/infosync/.ssh/id_rsa'):
    """
    Crear un archivo tar de directorio remoto
    """
    dbname = backup_mysqldb()
    env.host_string = testing_server
    env.user = 'infosync'
    env.key_filename = key_filename
    print 'starting to do backup of all folders...'
    date = datetime.now()
    date = date.strftime("%Y_%m_%d")
    tar_name = 'linkaform_bakup_%s.tar.gz'%date
    run("tar cfz %s public_html/ %s"%(tar_name,dbname))
    print 'backup compleated',tar_name
    return tar_name

def restores_linkaform_db():
    """
    Copies and restores the databse form the remote server
    """
    script = """dropdb infosync_prod --username infosync -h 10.1.66.19
drop database infosync_wp1;
create database infosync_wp1;
use infosync_wp1;
GRANT ALL PRIVILEGES ON infosync_wp1.* TO "infosync"@"hostname"  IDENTIFIED BY "director";
FLUSH PRIVILEGES;"""
    update_script ="update infosync_wp1.wp_options set option_value ='http://%s' where option_id=1 or option_id=37;"%(production_server)
    db_name = backup_mysqldb()
    print 'Coping files...'
    for server in front_servers:
        env.host_string = server
        env.user = 'infosync'
        env.key_filename = '/home/infosync/.ssh/id_rsa'
        file_write('/tmp/sql_drop.sql', script)
        file_write('/tmp/update_script.sql', update_script )
        run("scp  infosync@%s:%s ./"%(testing_server,db_name))
        print 'droping db . . .'
        run("mysql -uroot -pdirector infosync_wp1 < %s"%"/tmp/sql_drop.sql")
        print 'Restoring . . .'
        run("mysql -uinfosync -pdirector infosync_wp1 < infosync_wp1.sql ")
        print 'Updates...'
        run("mysql -uinfosync -pdirector infosync_wp1 < %s"%"/tmp/update_script.sql")
        print 'restores_remote_db DONE'
    return True


if __name__ == "__main__":
    if True:
        print 'Backup Postgres'
        backup_name = backup_postgres_linkaform(production_server, key_filename, dbname='infosync', dbport=5434)
        #copydb(backup_name)
    else:
        print 'Sorry no option selected, pleas use all, make_build, commit, restore_build, wordpress '
21
