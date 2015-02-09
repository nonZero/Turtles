import os.path

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.utils import apply_lcwd
from fab_tools.project import get_secret_key


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
    local("createuser -s {}".format(env.user))


@task
def create_db():
    local("createdb -O {0} {0}".format(env.user))
    postgis()


@task
def postgis():
    sql = "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;"
    local('psql -c "{0}" -U {1} {1}'.format(sql, env.user))


def local_template(filename, destination, context=None, use_jinja=True,
                   template_dir=None, override=False):
    """
    Render a template text file locally.

    ``filename`` should be the path to a text file, which may contain `Python
    string interpolation formatting
    <http://docs.python.org/library/stdtypes.html#string-formatting>`_ and will
    be rendered with the given context dictionary ``context`` (if given.)

    Alternately, if ``use_jinja`` is set to True and you have the Jinja2
    templating library available, Jinja will be used to render the template
    instead. Templates will be loaded from the invoking user's current working
    directory by default, or from ``template_dir`` if given.

    The resulting rendered file will be copied to  ``destination``.

    """
    if os.path.exists(destination) and not override:
        raise Exception("File already exists: {}".format(destination))

    # Process template
    text = None
    if use_jinja:
        try:
            template_dir = template_dir or os.getcwd()
            template_dir = apply_lcwd(template_dir, env)
            from jinja2 import Environment, FileSystemLoader

            jenv = Environment(loader=FileSystemLoader(template_dir))
            text = jenv.get_template(filename).render(**context or {})
            # Force to a byte representation of Unicode, or str()ification
            # within Paramiko's SFTP machinery may cause decode issues for
            # truly non-ASCII characters.
            text = text.encode('utf-8')
        except ImportError:
            import traceback

            tb = traceback.format_exc()
            abort(tb + "\nUnable to import Jinja2 -- see above.")
    else:
        if template_dir:
            filename = os.path.join(template_dir, filename)
        filename = apply_lcwd(filename, env)
        with open(os.path.expanduser(filename)) as inputfile:
            text = inputfile.read()
        if context:
            text = text % context

    # Save file.
    with open(destination, 'w') as f:
        f.write(text)

    return text


@task
def create_dev_settings():
    local_template('conf/dev_settings_template.py',
                   '{}/local_settings.py'.format(env.project),
                   {
                       'secret_key': get_secret_key()
                   },
                   use_jinja=True)
