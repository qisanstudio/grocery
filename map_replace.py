# -*- coding: utf-8 -*-

import os
import click
from shutil import copyfile

ORIGIN_SUFFIX = '.origin'


@click.group()
def cli():
    pass


@click.command()
@click.option('--source', default='source dir')
@click.option('--target', default='target dir')
def replace(source, target):
    assert os.path.isabs(source) and os.path.isdir(source)
    assert os.path.isabs(target) and os.path.isdir(target)
    for root, dirs, files in os.walk(source, topdown=False):
        for f in files:
            if f.startswith('.'):
                continue
            source_file_path = '%s/%s' % (root, f)
            target_file_path = source_file_path.replace(source, target, 1)
            target_origin_file_path = '%s%s' % (target_file_path, ORIGIN_SUFFIX)
            if not os.path.exists(target_origin_file_path):
                copyfile(target_file_path, target_origin_file_path)
            copyfile(source_file_path, target_file_path)
            print "%s replaced" % target_file_path
    print "origin file rename to xxx%s" % ORIGIN_SUFFIX


@click.command()
@click.option('--target', default='target dir')
def recover(target):
    assert os.path.isabs(target) and os.path.isdir(target)
    for root, dirs, files in os.walk(target, topdown=False):
        for f in files:
            if not f.endswith(ORIGIN_SUFFIX):
                continue
            target_origin_file_path = '%s/%s' % (root, f)
            target_file_path = target_origin_file_path.replace(ORIGIN_SUFFIX, '')
            copyfile(target_origin_file_path, target_file_path)
            os.remove(target_origin_file_path)


@click.command()
@click.option('--p', default='target dir')
def t(p):
    print os.path.isabs(p)
    print os.path.isdir(p)



cli.add_command(replace)
cli.add_command(recover)
cli.add_command(t)


if __name__ == '__main__':
    cli()
