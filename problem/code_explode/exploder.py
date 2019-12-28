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

from importlib.resources import contents
from importlib.util import find_spec
from pathlib import Path
import ast
import inspect
import os
import pkgutil
import shutil

import click


class SourceCodeExploder:

    def __init__(self, out_dir=Path('/tmp/code')):
        if out_dir.exists():
            shutil.rmtree(out_dir)
        os.mkdir(out_dir)
        self.out_dir = out_dir
        self._ignore_dirs = {'.git'}
        self._ignore_names_in_module = {
            '__builtins__',
            '__cached__',
            '__doc__',
            '__file__',
            '__loader__',
            '__name__',
            '__package__',
            '__path__',
            '__spec__',
        }

    def _is_directory_to_scan(self, dir: str):
        return dir not in self._ignore_dirs

    def explode_tree(self, top_dir):
        assert top_dir.is_dir(), f'Need a directory, but got: {top_dir}'
        for root, dirs, files in os.walk(top_dir):
            # We modify dirs in-place, to influence what walk() will visit.
            dirs[:] = list(filter(self._is_directory_to_scan, dirs))
            root = Path(root)
            for file in files:
                if file.endswith('.py'):
                    self.explode_file(root / file)

    def explode_file(self, fspec):
        ''

    def explode_packages(self, top_dir):
        for x in pkgutil.walk_packages([top_dir]):
            print(x)
            print('')

        # https://stackoverflow.com/questions/16852811/import-modules-in-a-dir
        for loader, name, is_pkg in pkgutil.walk_packages([str(top_dir)]):
            print(1, name, is_pkg, loader)

            module = loader.find_module(name).load_module(name)
            print(2, module)

            for name, value in inspect.getmembers(module):
                if name in self._ignore_names_in_module:
                    continue
                str_value = str(value)
                # e.g. <module 'collections'
                # from '/.../miniconda3/envs/.../lib/python3.7/collections/__init__.py'>
                if (str_value.endswith(' (built-in)>')
                        or '/miniconda3/envs/' in str_value):
                    continue
                print(3, name, value)


@click.command()
@click.argument('top_dir')
def main(top_dir):
    """
Usage: exploder.py TOP_DIR

You may want to invoke in this way:

    $ code_explode/exploder.py `git rev-parse --show-toplevel`
    """
    SourceCodeExploder().explode_packages(Path(top_dir))


if __name__ == '__main__':
    main()
