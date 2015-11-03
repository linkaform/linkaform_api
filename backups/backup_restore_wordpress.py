# coding: utf-8

__author__ = "josepato.villarreal"
"""
Script para automatizar las setup del backend de Infosync, en un server:
Configuracion Ubuntu Server 12.04 LTS
"""

from cuisine import *
from fabric.api import env, execute, task
from fabric import operations
from sys import argv

testing_server = 'www.linkaform.com'
production_server = 'test.linkaform.com'

#TODO:
#PUT PASSWORDS ON FIELS


@task
def backup_mysqldb():
    """
    Crear un archivo tar de directorio remoto
    """
    env.host_string = testing_server
    env.user = 'infosync'
    env.key_filename = '/home/josepato/.ssh/id_rsa_goddady'
    print 'starting....'
    db_backup_name = 'infosync_wp1.sql'
    run ("mysqldump -uinfosync_wp1 -pB*tD7dMZIv16.~9   infosync_wp1 > %s"%(db_backup_name))
    print 'Backup done....'
    return db_backup_name

@task
def backup_public_html():
    """
    Crear un archivo tar de directorio remoto
    """
    dbname = backup_mysqldb()
    env.host_string = testing_server
    env.user = 'infosync'
    env.key_filename = '/home/josepato/.ssh/id_rsa_goddady'
    print 'starting....'
    tar_name = 'linkaform_bakup.tar.gz'
    #run("tar cfz %s public_html/ %s"%(tar_name,dbname))
    return tar_name

@task
def restores_remote_db():
    """
    Copies and restores the databse form the remote server
    """
    with mode_local():
        env.host_string = production_server
        #env.user = 'infosync'
        #env.key_filename = '/home/josepato/.ssh/id_rsa_goddady'
        #setups scripts
        script = """use infosync_wp1;
drop database infosync_wp1;
create database infosync_wp1;
use infosync_wp1;
GRANT ALL PRIVILEGES ON infosync_wp1.* TO "infosync"@"hostname"  IDENTIFIED BY "director";
FLUSH PRIVILEGES;"""
        update_script ="update infosync_wp1.wp_options set option_value ='http://%s' where option_id=1 or option_id=37;"%(production_server)
        file_write('/tmp/sql_drop.sql', script)
        file_write('/tmp/update_script.sql', update_script )
        #makes remote backup
    db_name = backup_mysqldb()
    #copies dbs
    print 'Coping files...'
    run_local("scp -i .ssh/id_rsa_goddady infosync@%s:%s ./"%(testing_server,db_name))
    print 'droping db . . .'
    run_local("mysql -uroot -pdirector infosync_wp1 < /tmp/sql_drop.sql")
    print 'Restoring . . .'
    run_local("mysql -uinfosync -pdirector infosync_wp1 < infosync_wp1.sql ")
    print 'Updates...'
    run_local("mysql -uinfosync -pdirector infosync_wp1 < /tmp/update_script.sql")
    print 'restores_remote_db DONE'

def restores_remote_wordpress():
    """
    Copies and restores remote wordpress
    """
    restores_remote_db()
    backup_name = backup_public_html()
    print 'coping files...'
    env.host_string = 'localhost' #production_server
    env.user = 'josepato'
    env.key_filename = '/home/josepato/.ssh/id_rsa'
    run_local("scp -i .ssh/id_rsa_goddady infosync@%s:%s ./"%(testing_server, backup_name))
    print 'Restoring ',backup_name
    print 'Files Ready'
    with mode_local():
        with mode_sudo():
            dir_attribs("/srv/wordpress/linkaform.com", mode=777, owner='www-data', group='www-data', recursive=True)
    with mode_local():
        with mode_sudo():
            run_local("tar xfz %s -C /srv/wordpress/linkaform.com/ --strip-components=1"%(backup_name))
            dir_attribs("/srv/wordpress/linkaform.com", mode=774, owner='www-data', group='www-data', recursive=True)
    print 'restores_remote_wordpress = Done'

if __name__ == "__main__":
    try:
        if argv[1] == 'all':
            print 'the hole echilada'
            execute(restores_remote_wordpress)
        else:
            print ' olny db'
            execute(restores_remote_db)
    except IndexError:
        execute(restores_remote_db)
        print 'only bd'
