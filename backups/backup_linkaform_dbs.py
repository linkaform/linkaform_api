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
from cuisinemongodb import cuisine_mongodb as cm


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
        env.port = ssh_args['port']


#@task
def backup_postgres_linkaform(server_args, db_args):
    """production_server
    Crear un archivo tar de directorio remoto
    """
    production_server = server_args['server']
    production_db_server = db_args['dbhost']
    USERNAME = os.popen('whoami').readline()[:-1]
    key_filename = '/home/%s/.ssh/id_rsa'%(USERNAME)
    dbname_dev='infosync_prod'
    development_server ='slimey.linkaform.com'
    development_db_server ='10.1.66.19' 
    dbname_dev='infosync'
    dbport_dev ='5432'
    ## Va a hacer el respaldo de produccion
    dbbackup_name = cp.postgres_backup(db_args['dbname'], db_args['dbhost'], db_args['dbport'], ssh_args=server_args)
    file_name = dbbackup_name.split('/')[-1]
    file_path = dbbackup_name.strip(file_name)

    # Va a develop copia base de datos, borra la actual y restaura con la nueva
    print "****************************************************************"
    print "Know let me ask you the destination of the information."
    development_server = assing(raw_input("Whats the domain or ip address of the destination server? (*%s)"%development_server), development_server)
    username = assing(raw_input("Server username ? (*%s)"%USERNAME), USERNAME)
    server_port = assing(raw_input("Server ssh port ? (*%s)"%server_args['port']), server_args['port'])
    key_filename = assing(raw_input("And lastly key_filename? (*%s)"%server_args['key_filename']), server_args['key_filename'])
    print "Sorry for all the questions but is my jos :S, let me start doing the work"
    print '--------------------------------------------------------------------------------------'
    dbname_dev = assing(raw_input("Now tell me, what do you like for the new databse?(*%s)"%dbname_dev), dbname_dev)
    dbhost_dev = assing(raw_input("On what host does it %s resides?(*%s)"%(dbname_dev, development_db_server)), development_db_server)
    dbport_dev = assing(raw_input("And last but not the least, what port number?(*%s)"%dbport_dev), dbport_dev)
    raw_input("Just push the red botton when you want me to start...")
    server_args = {'server':development_server, 'username':username, 'key_filename':key_filename, 'port':server_port}
    set_enviorment(server_args)
    dir_ensure(file_path)
    run("scp  %s@%s:%s %s"%(username, production_server, dbbackup_name, file_path))
    try:
        cp.postgres_dropdb(dbname_dev, username, dbhost=development_server, dbport=dbport_dev, ssh_args=server_args)
    except:
        'no db with that name :S'

    cp.postgresql_database_create(dbname_dev, encoding='UNICODE' , owner=username, dbhost=dbhost_dev, dbport=dbport_dev, ssh_args=server_args )
    cp.postgres_restoredb(dbname_dev, dbbackup_name , username=username, dbhost='10.1.66.19', ssh_args=server_args)
    query="update user_customuser set password =''"
    #cp.postgresql_database_create(dbname, development_server, key_filename,
    #                              username, encoding='UNICODE', owner=username)
    #cp.postgres_restoredb(development_server, key_filename, username, dbname, dbhost='10.1.66.19', dbport='5434')
    return True


#@task
def backup_mongodb_linkaform(server_args, db_args):
    """
    Genera un resplado de una base de datos remota y la restablece en otro servidor
    """
    ## Va a hacer el respaldo de produccion

    dbbackup_name = cm.mongodb_backup(db_args['dbname'], db_args['dbhost'], db_args['dbport'], ssh_args=server_args)
    file_name = dbbackup_name.split('/')[-1]
    file_path = dbbackup_name.strip(file_name)
    dbname = file_name.split('_')[0]
    set_enviorment(server_args)
    with cd(file_path):
        cmd = "tar -zcvf %s.tar.gz %s"%(dbbackup_name, file_name)
        print 'cmd', cmd
        run(cmd)
        cmd_rm = "rm -rf %s"%dbbackup_name
        print 'rd', cmd_rm
        run(cmd_rm)
    dbbackup_name = dbbackup_name + '.tar.gz'
    #run(cmd)
    return dbbackup_name


def mongodb_restoredb_linkaform(destserver_args, db_args, server_args={}):
    """
    Restarua al base de datos a partir de un tar y la restablece en el servidor
    """
    ## Va a hacer el respaldo de produccion
    dbbackup_name = db_args['dbname']
    file_name = dbbackup_name.split('/')[-1]
    file_path = dbbackup_name.strip(file_name)
    dbname = file_name.split('_')[0]
    set_enviorment(destserver_args)
    dir_ensure(file_path)
    if server_args.has_key('server'):
        server = server_args['server']
        cmd = "scp %s:%s %s"%(server, dbbackup_name, file_path)
        run(cmd)
    with cd(file_path):
        cmd = "tar -zxvf %s "%(dbbackup_name)
        run(cmd)
    restore_location = dbbackup_name.strip('.tar.gz')
    try:
        cm.mongodb_dropdb(dbname, dbhost=db_args['dbhost'], dbport=db_args['dbport'], ssh_args=destserver_args)
    except:
        print 'could not drop the database %s at %s'%(db_args['dbname'], db_args['dbname'] + ':' + db_args['dbport'])
    try:
        cm.mongodb_restoredb(restore_location, dbhost=db_args['dbhost'], dbport=db_args['dbport'], ssh_args=destserver_args)
    except:
        print 'could not restore the database %s at %s'%(db_args['dbname'], db_args['dbname'] + ':' + db_args['dbport'])



def assing(new_val, default_val):
    if not new_val:
        return default_val
    return new_val

def starting_menu(args):
        """
        The default menu for the restore vote
        """
        #default values
        development_server = 'slimey.linkaform.com'
        development_db_server = '10.1.66.14'
        production_server = 'backend.linkaform.com'
        production_db_server = 'db4.linkaform.com'
        USERNAME = os.popen('whoami').readline()[:-1]
        key_filename = '/home/%s/.ssh/id_rsa'%(USERNAME)
        db_type = 'mongdb'
        port  = 22
        print '==== Welcome to the Linkaform Database Restore Vote ===='
        print 'The options maked with a * are consider default options'
        db_type = assing(raw_input("Please select which db you what to restore (postgres, *mongodb): "),db_type)
        print 'Ok, nice selection, you choosed:', db_type
        if not db_type:
            db_type = 'mongdb'
        if db_type == 'postgres':
            print "Greate, so you want me to help you with a postgres restore, "
            print "Piece of cake.... But first let me ask you some questions"
            dbname = 'infosync'
            dbport=5434
            production_server = assing(raw_input("Whats the domain or ip address of the server? (*%s)"%production_server), production_server)
            username = assing(raw_input("Server username to access the server ? (*%s)"%USERNAME), USERNAME)
            server_port = assing(raw_input("On what port does the ssh Server is configure? (*%s)"%port), port)
            key_filename = assing(raw_input("And lastly key_filename I'll use? (*%s)"%key_filename), key_filename)
            print '\n\n'
            print '------------------------- About the Database ------------------------------------'
            dbname = assing(raw_input("Now tell me, what is the name of the databse?(*%s)"%dbname), dbname)
            dbhost = assing(raw_input("On what host does %s resides?(*%s)"%(dbname, production_db_server)), production_db_server)
            dbport = assing(raw_input("And last but not the least, what port number?(*%s)"%dbport), dbport)
            server_args = {'server':production_server, 'username':username, 'key_filename':key_filename, 'port':server_port }
            db_args = {'dbname':dbname, 'dbhost':dbhost, 'dbport':dbport }
            backup_name = backup_postgres_linkaform(server_args, db_args)
        if db_type =='mongdb':
            ### TODO send this code to a function
            dbport = 27017
            dbname = 'infosync'
            print "Greate, so you want me to help you with a mongodb restore, "
            print "Piece of cake.... But first let me ask you some questions"
            production_server = assing(raw_input("Whats the domain or ip address of the server? (*%s)"%production_server), production_server)
            username = assing(raw_input("Server username ? (*%s)"%USERNAME), USERNAME)
            server_port = assing(raw_input("Server ssh port ? (*%s)"%port), port)
            key_filename = assing(raw_input("And lastly key_filename? (*%s)"%key_filename), key_filename)

            print '\n\n'
            print '------------------------- About the Database ------------------------------------'
            dbname = assing(raw_input("Now tell me, what is the name of the databse?(*%s)"%dbname), dbname)
            dbhost = assing(raw_input("On what host does %s resides?(*%s)"%(dbname, production_db_server)), production_db_server)
            dbport = assing(raw_input("And last but not the least, what port number?(*%s)"%dbport), dbport)
            server_args = {'server':production_server, 'username':username, 'key_filename':key_filename, 'port':server_port }
            db_args = {'dbname':dbname, 'dbhost':dbhost, 'dbport':dbport }

            print '\n\n'
            print "****************************************************************"
            print "Know let me ask you the destination of the information."

            development_server = assing(raw_input("Whats the domain or ip address of the destination server? (*%s)"%development_server), development_server)
            username = assing(raw_input("Server username ? (*%s)"%USERNAME), USERNAME)
            server_port = assing(raw_input("Server ssh port ? (*%s)"%port), port)
            key_filename = assing(raw_input("And lastly key_filename? (*%s)"%key_filename), key_filename)

            print "Sorry for all the questions but is my jos :S, let me start doing the work"
            print '--------------------------------------------------------------------------------------'
            dbname = assing(raw_input("Now tell me, what do you like for the new databse?(*%s)"%dbname), dbname)
            dbhost = assing(raw_input("On what host does %s resides?(*%s)"%(dbname, development_db_server)), development_db_server)
            dbport = assing(raw_input("And last but not the least, what port number?(*%s)"%dbport), dbport)
            raw_input("Just push the red botton when you want me to start...")
            backup_tar_name = backup_mongodb_linkaform(server_args, db_args)
            destserver_args = {'server':development_server, 'username':username, 'key_filename':key_filename, 'port':server_port}
            db_args = {'dbname':backup_tar_name, 'dbhost':dbhost, 'dbport':dbport }
            mongodb_restoredb_linkaform(destserver_args, db_args, server_args)




if __name__ == "__main__":
    if True:
        starting_menu(argv)
    else:
        print 'Sorry no option selected, pleas use all, make_build, commit, restore_build, wordpress '
21
