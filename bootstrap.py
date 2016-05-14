"""
Derek Merck <derek_merck@brown.edu>
Spring 2016

The Medical Image Informatics Platform Bootstrapper

Utility scripts for cleaning and setting up config for docker-compose defined MIIP services.
"""

import logging
import argparse
import yaml
from jinja2 import Environment, FileSystemLoader
import pprint
import subprocess
import os

__version__ = "0.1"
__description__ = "Utility scripts for cleaning and setting up config for docker-compose defined MIIP services."

# TODO: If forward in orthanc env, modify and copy the autorouter lua
# TODO: Better setup of Docker env vars or use Docker python API


def parse_args():
    parser = argparse.ArgumentParser(prog='MIIP Bootstrapper', description=__description__)

    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s (version ' + __version__ + ')')

    parser.add_argument('--clean', action='store_true')
    parser.add_argument('services', nargs="+",
                        choices=['orthanc', 'orthanc-receiver', 'xnat'])

    _opts = parser.parse_args()
    return _opts


def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                pass
                # raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def parse_template(template_file, out_file, env):
    jinja = Environment(loader=FileSystemLoader('.'))
    template = jinja.get_template(template_file)
    env['globals'] = global_env
    output_from_parsed_template = template.render(env)
    # logging.debug(output_from_parsed_template)

    with open(out_file, "wb") as fh:
        fh.write(output_from_parsed_template)


def exec_sql(sql):
    p = ['docker-compose', '-f', 'docker-compose.yml', '-f', 'docker-compose.shadow.yml', 'exec', 'postgres', 'psql', '-c', sql, '-U', 'postgres']
    subprocess.call(p)


def add_postgres_database(env):

    sql = "CREATE DATABASE {DB_NAME} WITH OWNER {DB_USER}".format(
        DB_USER=env['environment']['DB_USER'],
        DB_NAME=env['environment']['DB_NAME'])
    exec_sql(sql)
    exec_sql("\l")


def drop_postgres_database(env):
    sql = "DROP DATABASE {DB_NAME}".format(
        DB_NAME=env['environment']['DB_NAME'])
    exec_sql(sql)
    exec_sql("\l")


def drop_postgres_user(env):

    # # List roles in DB
    # exec_sql("\du")
    #
    sql = "DROP USER {DB_USER}".format(
        DB_USER=env['environment']['DB_USER'])
    exec_sql(sql)
    #
    # # List revised roles in DB
    # exec_sql("\du")


def add_postgres_user(env):

    # # List roles in DB
    # exec_sql("\du")

    sql = "CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}'".format(
        DB_USER=env['environment']['DB_USER'],
        DB_PASSWORD=env['environment']['DB_PASSWORD'])
    exec_sql(sql)

    sql = "ALTER USER {DB_USER} WITH CREATEDB".format(
        DB_USER=env['environment']['DB_USER'])
    exec_sql(sql)

    # List revised roles in DB
    exec_sql("\du")


def setup_orthanc(env, **kwargs):

    add_postgres_user(env)
    add_postgres_database(env)

    # Create the config file

    # Figure out where the data dir belongs
    for f in env['volumes']:
        if 'db' in f:
            env['DATA_DIR'] = f.split(":")[1]

    # Figure out where to output the config file
    for f in env['volumes']:
        if 'shadow' in f:
            out_file = f.split(":")[0]

    # Create it
    parse_template('orthanc.template.json', out_file, env)


def setup_xnat(env, **kwargs):

    add_postgres_user(env)
    # No need to create the database itself; the xnat builder insists on creating it

    # Create the config file
    parse_template('xnat-docker/xnat.config.template', 'xnat-docker/xnat.shadow.config', env)

    # TODO: Build and tag the xnat template image for docker-compose if it doesn't exist
    # TODO: Allow build even if the database already exists


def clean_db(env):
    drop_postgres_database(env)
    drop_postgres_user(env)

if __name__ == "__main__":

    print "hi"

    logging.basicConfig(level=logging.DEBUG)
    logging.debug("MIIP Bootstrapper v{version}".format(version=__version__))

    opts = parse_args()

    with open("docker-compose.yml", 'r') as f:
        env = yaml.load(f)

    # Deal with shadow overrides
    try:
        with open("docker-compose.shadow.yml", 'r') as f:
            shadow = yaml.load(f)
            env = merge(shadow, env)
    except:
        logging.debug("No shadow file to merge")
        pass

    # Deal with extensions
    for s, d in env['services'].iteritems():
        base_service = d.get('extends', None)
        if base_service:
            env['services'][s] = merge(d, env['services'][base_service])

    logging.info(pprint.pformat(env))

    # Get the DB host and port
    global_env = {}
    global_env['DB_HOST'] = 'postgres'
    global_env['DB_PORT'] = env['services']['postgres']['ports'][0].split(":")[0]

    # Improve your Docker env
    os.environ['DOCKER_TLS_VERIFY'] = "1"
    os.environ['DOCKER_HOST'] = "tcp://192.168.99.100:2376"
    os.environ['DOCKER_CERT_PATH'] = "/Users/derek/.docker/machine/machines/default"
    os.environ['DOCKER_MACHINE_NAME'] = "default"

    if opts.clean:
        if 'orthanc' in opts.services:
            clean_db(env['services']['orthanc'])
        if 'orthanc-receiver' in opts.services:
            clean_db(env['services']['orthanc-receiver'])
        if 'xnat' in opts.services:
            clean_db(env['services']['xnat'])

    if 'orthanc' in opts.services:
        setup_orthanc(env['services']['orthanc'])

    if 'orthanc-receiver' in opts.services:
        setup_orthanc(env['services']['orthanc-receiver'])

    if 'xnat' in opts.services:
        setup_xnat(env['services']['xnat'])