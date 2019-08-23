#!/root/.virtualenvs/venv/bin/python2
# -*- coding: utf-8 -*-

import os
import sys
from shutil import copyfile

ORIGIN_SUFFIX = '.origin'


def replace(source, target):
    assert os.path.isabs(source) and os.path.isdir(source)
    assert os.path.isabs(target) and os.path.isdir(target)
    for root, dirs, files in os.walk(source, topdown=False):
        for f in files:
            source_file_path = '%s/%s' % (root, f)
            target_file_path = source_file_path.replace(source, target, 1)
            target_origin_file_path = '%s%s' % (target_file_path, ORIGIN_SUFFIX)
            # 如果不存在target_file 跳过
            if not os.path.exists(target_file_path):
                continue
            # 没有.origin文件才创建.origin文件
            if not os.path.exists(target_origin_file_path):
                copyfile(target_file_path, target_origin_file_path)
            copyfile(source_file_path, target_file_path)
            print "%s replaced" % target_file_path
    print "origin file rename to xxx%s" % ORIGIN_SUFFIX


def recover(target):
    assert os.path.isabs(target) and os.path.isdir(target)
    for root, dirs, files in os.walk(target, topdown=False):
        for f in files:
            if not f.endswith(ORIGIN_SUFFIX):
                continue
            target_origin_file_path = '%s/%s' % (root, f)
            target_file_path = target_origin_file_path.replace(ORIGIN_SUFFIX, '')
            copyfile(target_origin_file_path, target_file_path)
            print "%s recoverd" % target_file_path
            os.remove(target_origin_file_path)


if __name__ == '__main__':
    if sys.argv[1].lower() == 'replace':
        replace(sys.argv[2], sys.argv[3])
    elif sys.argv[1].lower() == 'recover':
        recover(sys.argv[2])
    else:
        print 'replace | recover'

