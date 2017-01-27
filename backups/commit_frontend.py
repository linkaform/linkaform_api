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
    else:
        print 'Sorry no option selected, pleas use all, make_build, commit, restore_build, wordpress '
