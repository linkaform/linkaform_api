# coding: utf-8

__author__ = "josepato.villarreal"
"""
Script para automatizar las setup del backend de Infosync, en un server:
Configuracion Ubuntu Server 12.04 LTS
"""

""" OJO ATENCION el servidor de godaddy no deja hacer una conexion de ssh
al servidor de git que tenemos detras del NAT en el puerto 2223.
Por lo que estamos haciendo un port fordward desde abby (git) hasta rostia
(blog.info-sync.com) con
sy dsede el servidor de godaddy

ssh -L 2223:localhost:2223 blog.info-sync.com

y luego apuntamos a localhost para hacer el ssh

ssh localhost -p 2223

;)

Estos estan correindo en un screen
"""

from cuisine import *
from fabric.api import env, execute, task
from fabric import operations
from sys import argv
from datetime import datetime

testing_server = 'test.linkaform.com'
production_server = 'app.linkaform.com'
front_servers = ['ernie.linkaform.com', 'ernie2.linkaform.com']
production_server_tetengo = 'ernie.tetengo.com'


#TODO:
#PUT PASSWORDS ON FIELS


@task
def backup_mysqldb(key_filename='/home/infosync/.ssh/id_rsa'):
    """
    Crear un archivo tar de directorio remoto
    """
    env.host_string = testing_server
    env.user = 'infosync'
    env.key_filename = key_filename
    print 'starting... to backup remote db'
    db_backup_name = 'infosync_wp1.sql'
    run ("mysqldump -uinfosync_wp1 -pB*tD7dMZIv16.~9   infosync_wp1 > %s"%(db_backup_name))
    print 'Backup done....'
    return db_backup_name

@task
def backup_mysqldb_tetengo(key_filename='/home/infosync/.ssh/id_rsa'):
    """
    Crear un archivo tar de directorio remoto
    """
    env.host_string = testing_server
    env.user = 'infosync'
    env.key_filename = key_filename
    print 'starting... to backup remote db'
    db_backup_name = 'tetengo_wp2.sql'
    run ("mysqldump -utetengo_wp1 -pB*tD7dMZIv16.~9  tetengo_wp2 > %s"%(db_backup_name))
    print 'Backup done....'
    return db_backup_name

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

@task
def backup_public_html_tetengo(key_filename='/home/infosync/.ssh/id_rsa'):
    """
    Crear un archivo tar de directorio remoto
    """
    env.host_string = testing_server
    env.user = 'infosync'
    env.key_filename = key_filename
    home_dir = '/home/infosync/public_html'
    home_production_dir = '/srv/wordpress/linkaform.com'
    user = 'infosync'
    branch='master'
    #dbname = backup_mysqldb_tetengo(key_filename)
    print 'starting to do backup of all folders...'
    date = datetime.now()
    date = date.strftime("%Y_%m_%d")
    #tar_name = 'tetengo_bakup_%s.tar.gz'%date
    #run("tar cfz %s public_html/ %s"%(tar_name,tetengo))
    #print 'backup compleated',tar_name
    git_wordpress_backup(testing_server,home_dir, 22,branch, user, key_filename)
    for server in front_servers:
        git_pull(server, home_production_dir, 22, branch, user, key_filename)
    restores_remote_db_tetengo(key_filename)
    return True

@task
def restores_remote_db():
    """
    Copies and restores the databse form the remote server
    """
    script = """use infosync_wp1;
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

def restores_remote_db_tetengo(key_filename = '/home/infosync/.ssh/id_rsa'):
    """
    Copies and restores the databse form the remote server
    """
    script = """use tetengo_wp2;
drop database tetengo_wp2;
create database tetengo_wp2;
use tetengo_wp2;
GRANT ALL PRIVILEGES ON tetengo_wp2.* TO "infosync"@"hostname"  IDENTIFIED BY "director";
FLUSH PRIVILEGES;"""
    #update_script ="update tetengo_wp2.wp_options set option_value ='http://%s' where option_value like http://test.tetengo%;"%(production_server_tetengo)
    db_name = backup_mysqldb_tetengo(key_filename)
    print 'Coping files...'
    for server in front_servers:
        update_script = "UPDATE wp_options SET option_value = REPLACE(option_value, 'test', 'www') WHERE option_value like 'http://test.tetengo%'; "#%(server)
        env.host_string = server
        env.user = 'infosync'
        env.key_filename = key_filename# '/home/infosync/.ssh/id_rsa'
        file_write('/tmp/sql_drop_tetengo.sql', script)
        file_write('/tmp/update_script_tetengo.sql', update_script )
        run("scp  infosync@%s:%s ./"%(testing_server, db_name))
        print 'droping db . . .'
        run("mysql -uroot -pdirector tetengo_wp2 < %s"%"/tmp/sql_drop_tetengo.sql")
        print 'Restoring . . .'
        run("mysql -uinfosync -pdirector tetengo_wp2 < ./tetengo_wp2.sql ")
        print 'Updates...'
        run("mysql -uinfosync -pdirector tetengo_wp2 < %s"%"/tmp/update_script_tetengo.sql")
        print 'restores_remote_db DONE'
    return True


def git_commit_delete_files(server, home_dir, port=22, branch='master', user='infosync', key_filename='/home/infosync/.ssh/id_rsa'):
    env.host_string = server
    env.user = user
    env.port = port
    print 'key_filename',key_filename
    env.key_filename = key_filename
    with cd(home_dir):
        run('git  checkout %s'%(branch))
        try:
            del_files = run('git status  | grep deleted:')
            if del_files:
                del_files = del_files.replace('#','')
                del_files = del_files.replace('\t','')
                del_files = del_files.replace('\n','')
                del_files = del_files.replace('\r','')
                del_files = del_files.replace('deleted:','')
                print 'del_files', del_files
                git_del = run('git rm %s'%(del_files))
                if git_del[:2] != 'rm':
                    return False
        except:
            return False
        return True

def git_commit_add_all_files(server, home_dir, port=22, branch='master', user = 'infosync', key_filename = '/home/infosync/.ssh/id_rsa', comments=''):
    env.host_string = server
    env.user = user
    env.key_filename = key_filename
    with cd(home_dir):
        hostname = run('hostname')
        date = datetime.now()
        date = date.strftime("%Y_%m_%d")
        add_files = run('git add ./')
        git_commit = run('git commit -m "%s : Auto commit at branch %s,  made by jvote on %s the %s"'%(comments,branch, hostname, date))
        return True

def git_status(server, home_dir, port=22, branch='master', user = 'infosync', key_filename = '/home/infosync/.ssh/id_rsa'):
    env.host_string = server
    env.user = user
    env.key_filename = key_filename
    with cd(home_dir):
        status = run('git status')
    return status

def git_push(server, home_dir, port=22, branch='master', user = 'infosync', key_filename = '/home/infosync/.ssh/id_rsa'):
    env.host_string = server
    env.user = user
    env.key_filename = key_filename
    with cd(home_dir):
        status = run('git push -u origin %s'%(branch))
    return status

def git_pull(server, home_dir, port=22, branch='master', sys_user = 'infosync', key_filename = '/home/infosync/.ssh/id_rsa'):
    env.host_string = server
    env.user = sys_user
    env.key_filename = key_filename
    env.port = port
    print 'running pull at', server , 'port', port
    with cd(home_dir):
        print 'home dir', home_dir
        print 'sys_user', sys_user
        status = run('git fetch')
        print status
        status = run('git checkout %s'%(branch))
        print 'checkout=', status
        status = run('git pull -u origin %s'%(branch))
        print 'pull=', status
    return status

def git_wordpress_backup(server, home_dir, port=22, branch='master', sys_user = 'infosync', key_filename = '/home/infosync/.ssh/id_rsa'):
    #home_dir = '/home/infosync/public_html'
    #branch='master'
    #user = 'infosync'
    #key_filename = '/home/infosync/.ssh/id_rsa'
    #port =22
    print 'removing files...'
    del_files_status = git_commit_delete_files(server, home_dir, port, branch, user, key_filename)
    print 'removed with status', del_files_status
    print 'adding files ...'
    add_files_status = git_commit_add_all_files(server, home_dir, port, branch, user, key_filename, comments)
    print 'add files status: ',add_files_status
    print 'pushing files'
    status = git_push(server, home_dir, port, branch, user, key_filename)
    print 'git done', status
    return True

def restores_wordpress_git():
    """
    Copies and restores remote wordpress
    """
    home_dir = '/home/infosync/public_html'
    print 'doing status'
    status = git_status(testing_server, home_dir, port=22, branch='master', user = 'infosync', key_filename = '/home/infosync/.ssh/id_rsa')
    if status.find('nothing to commit') > 0 or status.find('up-to-date') > 0:
        print 'Nothing to commit, everything is up to date', status
    else:
        print 'making backups with git...'
        git_wordpress_backup()
        home_dir = '/srv/wordpress/linkaform.com/'
        for server in front_servers:
            env.host_string = server
            env.user = 'infosync'
            env.key_filename = '/home/infosync/.ssh/id_rsa'
            print 'making pull on ', server
            git_pull(server, home_dir, port=22, branch='master', sys_user = 'infosync', key_filename = '/home/infosync/.ssh/id_rsa')
            print 'pull done'
    restores_remote_db()
    restores_remote_db_tetengo()
    return True

def restores_remote_wordpress():
    """
    Copies and restores remote wordpress
    """
    restores_remote_db()
    backup_name = backup_public_html()
    print 'coping files...'
    env.host_string = 'localhost' #production_server
    env.user = 'josepato'
    env.key_filename = '/home/infosync/.ssh/id_rsa'
    run_local("scp -i /home/infosync/.ssh/id_rsa_goddady infosync@%s:%s /var/backups/"%(testing_server, backup_name))
    print 'Restoring ',backup_name
    with mode_local():
        with mode_sudo():
            dir_attribs("/srv/wordpress/linkaform.com", mode=777, owner='www-data', group='www-data', recursive=True)
    with mode_local():
        with cd('/var/backups/'):
            run_local("tar xfz /var/backups/%s "%(backup_name))
        with mode_sudo():
            run_local('rm -rf /srv/wordpress/linkaform/*')
            run_local('mv /var/backups/public_html/* /srv/wordpress/linkaform.com/')
            run_local('cp /home/josepato/wp-config.php /srv/wordpress/linkaform.com/')
            dir_attribs("/srv/wordpress/linkaform.com", mode=774, owner='www-data', group='www-data', recursive=True)
    print 'restores_remote_wordpress = Done'

def restores_remote_wordpress_tetengo():
    """
    Copies and restores remote wordpress
    """
    restores_remote_db_tetengo('/home/josepato/.ssh/id_rsa_goddady')
    backup_name = backup_public_html_tetengo('/home/josepato/.ssh/id_rsa_goddady')
    print 'coping files...'
    env.host_string = 'localhost' #production_server
    env.user = 'josepato'
    env.key_filename = '/home/infosync/.ssh/id_rsa'
    #run_local("scp -i /home/josepato/.ssh/id_rsa_goddady infosync@%s:%s /var/backups/"%(testing_server, backup_name))
    #run_local("scp -i /home/infosync/.ssh/id_rsa_goddady infosync@%s:%s /var/backups/"%(testing_server, backup_name))
    print 'Restoring ',backup_name
    with mode_local():
        with mode_sudo():
            dir_attribs("/srv/wordpress/linkaform.com", mode=777, owner='www-data', group='www-data', recursive=True)
    with mode_local():
        with cd('/var/backups/'):
            run_local("tar xfz /var/backups/%s "%(backup_name))
        with mode_sudo():
            run_local('rm -rf /srv/wordpress/linkaform/*')
            run_local('mv /var/backups/public_html/* /srv/wordpress/linkaform.com/')
            run_local('cp /home/josepato/wp-config-tetengo.php /srv/wordpress/linkaform.com/test.tetengo.com.mx/wp-config.php')
            dir_attribs("/srv/wordpress/linkaform.com", mode=774, owner='www-data', group='www-data', recursive=True)
    print 'restores_remote_wordpress = Done'

def make_oscar_build(branch):
    server = 'oscar.info-sync.com'
    port = 2221
    home_dir ='/home/infosync/infosync-webapp/app'
    user = 'infosync'
    key_filename = '/home/josepato/.ssh/id_rsa'
    git_pull(server, home_dir, branch, user, key_filename)
    run('grunt build --force')
    return True

def commiting_build(branch='master', server = 'oscar.info-sync.com', home_dir ='/home/infosync/infosync-webapp/app/dist' ,key_filename = '/home/josepato/.ssh/id_rsa', port=2221, user='infosync' ):
    git_commit_delete_files(server, home_dir, port, branch, user, key_filename)
    git_commit_add_all_files(server, home_dir, port, branch, user, key_filename, comments)
    git_push(server, home_dir, port, branch, user, key_filename)
    return True

def restore_build(branch='master'):
    server = 'oscar.info-sync.com'
    port = 2221
    home_dir ='/srv/infosync-webapp/dist'
    user = 'infosync'
    key_filename = '/home/josepato/.ssh/id_rsa'
    git_pull(server, home_dir, port, branch, user, key_filename)
    return True

if __name__ == "__main__":
    if argv[1] == 'all':
        print 'the hole echilada'
        execute(restores_remote_wordpress)
    #elif argv[1] == 'commit':
    elif argv[1] == 'make_build':
        print 'Starting to make build'
        branch = argv[2]
        restores_oscar_build(branch)
    elif argv[1] == 'commit':
        print 'Restore build'
        try:
            branch = argv[2]
            comments = argv[3]
        except:
            branch = 'master'
        commiting_build(branch)
        restore_build(branch)
    elif argv[1] == 'wordpress':
        print ' olny db'
        execute(restores_wordpress_git)
    elif argv[1] == 'tetengo':
        print ' olny db'
        execute(backup_public_html_tetengo)
    else:
        print 'Sorry no option selected, pleas use all, make_build, commit, restore_build, wordpress '
