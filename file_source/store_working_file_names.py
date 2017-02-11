#! /usr/bin/env python3

# Copyright 2017 John Hanley.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# The software is provided "AS IS", without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability,
# fitness for a particular purpose and noninfringement. In no event shall
# the authors or copyright holders be liable for any claim, damages or
# other liability, whether in an action of contract, tort or otherwise,
# arising from, out of or in connection with the software or the use or
# other dealings in the software.


# usage:
#     src/store_working_file_names.py db_dir repo_dir


import argparse
import os
import re
import sqlite3
import subprocess


def store(conn, repo):
    ins = "insert into file_source (pathname, src, pkg) values (?,'git',?)"
    curs = conn.cursor()
    if repo == '[clean]':
        curs.execute("delete from file_source where src = 'git'")
        return
    os.chdir(os.path.join(repo, '.git'))  # We verify it exists.
    os.chdir(repo)

    for path in backed_up_files(repo, paths_not_in_repo(repo)):
        curs.execute(ins, (path, repo))


def backed_up_files(repo, unsafe):
    for root, dirs, files in os.walk(repo):
        for file in files:
            path = os.path.join(root, file)
            if path not in unsafe:
                yield path


def paths_not_in_repo(prefix_dir):
    '''Returns files not yet safely backed up.'''
    strip_slash_re = re.compile(r'/$')  # e.g. 'bin/'
    stdout = subprocess.check_output('git status --porcelain'.split())
    lines = [os.path.join(prefix_dir, strip_slash_re.sub('', line[3:]))
             for line in stdout.decode('utf8').split('\n')
             if len(line) > 0 and line[2] == ' ']
    return set(lines)


def arg_parser():
    p = argparse.ArgumentParser(description='Store backed-up filenames.')
    p.add_argument('db_directory', help='location of sqlite database')
    p.add_argument('repo_directory', nargs='?', default='[clean]',
                   help='working dir of a git repository')
    return p


if __name__ == '__main__':
    args = arg_parser().parse_args()
    db_file = os.path.join(args.db_directory, 'pkg_contents.sqlite')
    with sqlite3.connect(db_file) as conn:
        store(conn, args.repo_directory)
