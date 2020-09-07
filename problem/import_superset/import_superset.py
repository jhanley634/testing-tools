#! /usr/bin/env python3

# Copyright 2018 John Hanley.
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

import enum
import os
import re
import sys

import click
import distlib.database


class DependencyType(enum.IntEnum):
    CONDA = 1
    PIP = 2


class EnvironmentYmlParser:

    def __init__(self, in_fspec):
        self.name_re = re.compile(r'^-? *(\w+)')
        with open(in_fspec) as fin:
            self.deps = set(self.parse_dependencies(fin))

    def parse_dependencies(self, fin):
        dep_type = None
        for line in fin:
            line = line.strip()
            if line == '- pip:':
                dep_type = DependencyType.PIP
                continue
            elif line == 'dependencies:':
                dep_type = DependencyType.CONDA
                continue
            if dep_type:
                yield dep_type, self._just_name(line)

    def _just_name(self, line):
        """Suppresses trailing >=2 or ==3 version specification."""
        m = self.name_re.search(line)
        assert m, line
        return m.group(1)


class PySourceParser:

    def __init__(self):
        pass


class EnvDeps:

    def __init__(self, files=None, src_dir='.'):
        files = files or sorted(self.get_env_files(src_dir))
        self.deps = set()
        for file in files:
            self.deps = self.deps.union(EnvironmentYmlParser(file).deps)

    @classmethod
    def get_env_files(cls, src_dir, env='environment.yml'):
        for root, dirs, files in os.walk(src_dir):
            if env in files:
                yield os.path.join(root, env)

    def write_environment_yml(self, env_name, fout):
        boiler = """name: {}
channels:
- defaults
- conda-forge
dependencies:
"""
        fout.write(boiler.format(env_name))
        prefix = '- '
        prev = DependencyType.CONDA
        for dep_type, name in sorted(self.deps):
            if prev != dep_type:
                prev = dep_type
                fout.write(prefix + 'pip:\n')
                prefix = '  ' + prefix
            fout.write(prefix + name + '\n')


@click.command()
@click.option('--src-dir', default='.')
def main(src_dir):

    dp = distlib.database.DistributionPath()
    for dist in dp.get_distributions():
        print(dist)

    sys.exit(0)
    ss = EnvDeps(src_dir=src_dir)
    ss.write_environment_yml('foo', sys.stdout)


if __name__ == '__main__':
    main()
