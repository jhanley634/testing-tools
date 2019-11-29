#! /usr/bin/env python

# Copyright 2019 John Hanley.
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

import glob
import os
import re
import subprocess

from ruamel.yaml import YAML


def _get_packages_with_versions(fin):
    d = YAML().load(fin)
    for dep in d['dependencies']:
        if isinstance(dep, dict):
            yield from dep['pip']
        else:
            yield dep  # e.g. 'seaborn >= 0.9.0'


def _get_package_names_and_versions(fin):
    name_ver_re = re.compile(r'^([\w\.-]+).* ([\d\.]+)$')  # ignores >=, ==
    for pkg_with_ver in _get_packages_with_versions(fin):
        m = name_ver_re.search(pkg_with_ver)
        if m:
            yield m.groups()


def _find_file(file):
    for pfx in ['', '../', '../../']:
        if os.path.exists(pfx + file):
            return pfx + file
    matches = glob.glob('*/' + file)
    if matches:
        return matches[0]
    return file  # Failure case, file does not exist, report diagnostic.


def report(file='environment.yml'):
    file = _find_file(file)
    with open(file) as fin:
        name_to_ver = dict(_get_package_names_and_versions(fin))

    name_ver_re = re.compile(r'^([\w\.-]+)\s+([\d\.]+)$')
    cmd = f'(conda list; pip list)'
    lines = subprocess.check_output(cmd, shell=True).decode().split('\n')
    for line in lines:
        m = name_ver_re.search(line.rstrip())
        if m:
            name, ver = m.groups()
            if (name in name_to_ver
                    and ver != name_to_ver[name]):
                print(f'  - {name} >= {ver}')


if __name__ == '__main__':
    report()
