# -*- coding: utf-8 -*-
import click
import subprocess
from datetime import datetime

ISOFORMAT = '%Y-%m-%d'


@click.group()
def cli():
    pass


def _docker_run(command, docker):
    print command
    return subprocess.call(['docker', 'exec', docker, 'bash', '-c', command])


@click.command()
@click.option('--proxy', help='proxy server eg:username@server')
@click.option('--pghost')
@click.option('--pgport', default=5432)
@click.option('--dbname')
@click.option('--extnames', multiple=True, help='exclude talbes')
@click.option('--dbuser')
@click.option('--docker', default='bragi_db_1')
def sync(proxy, pghost, pgport, dbname, extnames, dbuser, docker):
    fname = '%s_%s.sql' % (dbname, datetime.now().strftime(ISOFORMAT))
    cmd_l = ['pg_dump', '-U', dbuser, '-h', pghost, dbname]
    for extname in extnames:
        cmd_l.extend(['--exclude-table-data', extname])
    cmd_l.extend(['>', fname])
    command = ' '.join(cmd_l)
    subprocess.call(['ssh', proxy, command])
    subprocess.call(['scp', '%s:~/%s' % (proxy, fname), fname])
    _docker_run('su postgres -c "dropdb %s"' % dbname, docker)
    _docker_run('su postgres -c "createdb %s -O %s"' % (dbname, dbuser),
                docker)
    subprocess.call(['docker', 'cp', fname, '%s:%s' % (docker, fname)])
    _docker_run('su postgres -c "psql -d %s -f %s"' % (dbname, fname), docker)
    _docker_run('rm %s' % fname, docker)
    subprocess.call(['ssh', proxy, 'rm %s' % fname])


cli.add_command(sync)


if __name__ == '__main__':
    cli()
