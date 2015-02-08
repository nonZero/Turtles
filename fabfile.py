import datetime

from fabric.api import *

from fab_tools.server import *
from fab_tools.project import *
from fab_tools import dev
import os.path

PROJ_DIR = os.path.abspath(os.path.dirname(__file__))
CONF_DIR = os.path.abspath(os.path.join(PROJ_DIR, 'conf'))

env.project = "turtles"
env.user = "turtles"
env.gunicorn_port = 9091
env.clone_url = "git@github.com:nonZero/Turtles.git"
env.webuser = "webturtles"
env.code_dir = '/home/%s/Turtles/' % env.user
env.log_dir = '%slogs/' % env.code_dir
env.venv_dir = '/home/%s/.virtualenvs/turtles' % env.user
env.venv_command = '.  %s/bin/activate' % env.venv_dir
env.py = '.  %s/bin/python' % env.venv_dir
env.pidfile = '/home/%s/app.pid' % env.webuser
env.backup_dir = '/home/%s/backups' % env.user


@task
def qa():
    env.vhost = '192.168.20.100'
    env.hosts = [env.vhost]
    env.port = 9022
    env.redirect_host = 'www.%s' % env.vhost


@task
def prod():
    env.vhost = 'turtles.10x.org.il'
    env.hosts = [env.vhost]
    env.redirect_host = 'www.%s' % env.vhost


@task
def initial_project_setup():
    create_webuser_and_db()
    clone_project()
    create_venv()
    project_setup()


@task
def project_setup():
    project_mkdirs()
    create_local_settings()
    deploy(restart=False)
    gunicorn_setup()
    supervisor_setup()
    nginx_setup()
