import os.path

from fabric.api import *
from fabric.contrib.console import confirm


@task
def load_db_from_file(filename):
    if not os.path.isfile(filename):
        abort("Unknown file {}".format(filename))

    if not confirm(
            "DELETE local db and load from backup file {}?".format(filename)):
        abort("Aborted.")

    drop_command = "drop schema public cascade; create schema public;"
    local('''python -c "print '{}'" | python manage.py dbshell'''.format(
        drop_command, filename))

    cmd = "gunzip -c" if filename.endswith('.gz') else "cat"
    local('{} {} | python manage.py dbshell'.format(cmd, filename))


@task
def create_db_user():
    local("createuser {}".format(env.user))


@task
def create_db():
    local("createdb -O {0} {0}}".format(env.user))
    postgis()


@task
def postgis():
    sql = "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;"
    local('psql -c "{0}" -U {1} {1}'.format(sql, env.user))

