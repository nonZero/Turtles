import datetime

from fabric import operations
from fabric.api import *


@task
def backup_db():
    now = datetime.datetime.now()
    filename = now.strftime("lms10x-%Y-%m-%d-%H-%M.sql.gz")
    fullpath = env.backup_dir + '/' + filename
    run('sudo -u postgres pg_dump {} | gzip > {}'.format(env.webuser,
                                                         fullpath))
    operations.get(fullpath)
