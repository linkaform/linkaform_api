try:
    from cuisine import *
    from fabric.context_managers import cd, hide, settings
    from fabric.api import env, execute, task
    from fabric.operations import sudo
    from fabric.utils import puts
    __fabric_available = True
except ImportError:
    __fabric_available = False

from datetime import datetime


__version__ = '0.11.0'
__maintainer__ = u'JosePatricio Villarreal Martinez'
__email__ = 'josepato@linkaform.com'
__all__ = []


def require_fabric(f):
    """
    Raises ``RuntimeError`` if the wrapped method is called but ``fabric``
    cannot be imported for some reason.
    """
    global __fabric_available
    if __fabric_available:
        return f
    else:
        def _f(*args, **kwargs):
            error_message = 'To use function "{0}", you must have ' \
                            'fabric in the import path'.format(f.func_name)
            raise RuntimeError(error_message)
        return _f


def set_enviorment(ssh_args):
    if ssh_args.has_key('server'):
        env.host_string = ssh_args['server']
    if ssh_args.has_key('username'):
        env.user = ssh_args['username']
    if ssh_args.has_key('key_filename'):
        env.key_filename = ssh_args['key_filename']
    if ssh_args.has_key('port'):
        env.port = ssh_args['port']


@require_fabric
def mongodb_database_create(database_name,
                               dbhost=None,
                               dbport=None,
                               **ssh_args):
    return True

@require_fabric
def mongodb_backup(database_name, dbhost='127.0.0.1', dbport=27017, **ssh_args):
    """
    Creates a remote backup tar for the database
    """
    print 'entra a mongodb_backup=================================='
    if ssh_args and ssh_args['ssh_args'].has_key('server'):
            set_enviorment(ssh_args['ssh_args'])
    date = datetime.now()
    date = date.strftime("%Y%m%d-%H%M")
    backup_dir = '/backup/%s/devlop/'%database_name
    dir_ensure(backup_dir)
    dbbackup_name = '%s_bakup_%s'%(database_name,date)
    cmd = "mongodump -d %s --host %s:%s --out %s%s"%(database_name, dbhost, dbport, backup_dir, dbbackup_name)
    print cmd
    run(cmd)
    print 'Backup done....',cmd
    return backup_dir + dbbackup_name


@require_fabric
def mongodb_dropdb(database_name,
                    username=None,
                    dbhost='127.0.0.1',
                    dbport=5432,
                    password=None,
                    **ssh_args):
    """
    Drops the database
    """
    if ssh_args and ssh_args['ssh_args'].has_key('server'):
        set_enviorment(ssh_args['ssh_args'])

    opts = [
        database_name and '{0}'.format(database_name),
        username and '--username={0}'.format(username),
        dbhost and '--host={0}'.format(dbhost),
        dbport and '--port={0}'.format(dbport),
        password and '--password={0}'.format(password),
    ]

    cmd ='mongo {opts} --eval "db.dropDatabase()"'.format(
        opts=' '.join(opt for opt in opts if opt is not None)
        )
    print 'DROP DB cmd', cmd
    run(cmd)


@require_fabric
def mongodb_restoredb(restore_location,
                      username=None,
                      dbhost='127.0.0.1',
                      dbport=27017,
                      password=None,
                      collection=None,
                      **ssh_args):
    """
    Restores a database from a tar file sotred on disk
    """
    if ssh_args and ssh_args['ssh_args'].has_key('server'):
            set_enviorment(ssh_args['ssh_args'])
    opts = [
        username and '--username={0}'.format(username),
        dbhost and '--host={0}'.format(dbhost),
        dbport and '--port={0}'.format(dbport),
        password and '--password={0}'.format(password),
        collection and '--collection={0}'.format(collection),
    ]
    cmd = 'mongorestore {opts} {restore_location}'.format(
        opts=' '.join(opt for opt in opts if opt is not None),
        restore_location=restore_location
    )
    run(cmd)
    #return dbbackup_name
    return True

@require_fabric
def run_as_postgres_hidden(cmd):
    with settings(hide('everything'), warn_only=True):
        return run_as_postgres(cmd)


@require_fabric
def run_as_postgres(cmd):
    """
    Run given command as postgres user.
    """
    # The cd below is needed to avoid the following warning:
    #
    #     could not change directory to "/root"
    #
    with cd('/'):
        return sudo(cmd, user='postgres')
