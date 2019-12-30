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

from pathlib import Path
import ast
import collections
import hashlib
import inspect
import os
import pkgutil
import re
import shutil

from dill.source import getsource
from sqlalchemy.exc import InvalidRequestError as SAInvalidRequestError
from yapf.yapflib.yapf_api import FormatCode
import _pickle
import astor
import click


class SourceCodeExploder:

    def __init__(self, out_dir='/tmp/code', verbose=False):
        out_dir = Path(out_dir)
        if out_dir.exists():
            shutil.rmtree(out_dir)
        os.mkdir(out_dir)
        self.out_dir = out_dir
        self.verbose = verbose
        self.hash_cnt = collections.defaultdict(list)
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

    def explode_fs_tree(self, top_dir):
        assert top_dir.is_dir(), f'Need a directory, but got: {top_dir}'
        for root, dirs, files in os.walk(top_dir):
            # We modify dirs in-place, to influence what walk() will visit.
            dirs[:] = list(filter(self._is_directory_to_scan, dirs))
            root = Path(root)
            for file in files:
                if file.endswith('.py'):
                    fspec = root / file
                    with open(root / file) as fin:
                        self.explode_file(fin.read(), fspec)

    def explode_file(self, prog_text, fspec):
        tree = ast.parse(prog_text)
        assert () == tree._attributes, tree
        assert ('body', ) == tree._fields, tree
        assert isinstance(tree, ast.Module), tree
        setattr(tree, 'name', os.path.basename(fspec))
        self._dump_recursive(tree, '', [])

    def _dump_recursive(self, node, indent, path):
        path.append(getattr(node, 'name', ''))
        # print(indent, path, ast.dump(node, annotate_fields=True))
        if isinstance(node, ast.FunctionDef):
            self._elide_docstring(node.body)
            code, _ = FormatCode(astor.to_source(node))
            code = self._apply_indent(indent, code)
            out_path = '/'.join(path)
            self._write_file(self.out_dir / out_path, code)
            if self.verbose:
                print(f'\n{indent}{out_path}\n{code}')

        for child in getattr(node, 'body', []):
            self._dump_recursive(child, indent + '    ', path)
            path.pop()

    def _write_file(self, fspec, text):
        hex = self._digest(text)
        dir_, base = os.path.split(fspec)
        os.makedirs(dir_, exist_ok=True)
        with open(f'{dir_}/{base}_{hex}', 'w') as fout:
            fout.write(text)

        matches = self.hash_cnt[hex]
        matches.append(str(fspec))
        if len(matches) > 1:
            print('dup:', hex, '  '.join(matches))

    @staticmethod
    def _digest(text: str):
        """Finds sha224 hash of input, with indent elided."""
        text = '\n'.join([line.strip()
                          for line in text.splitlines()])
        return hashlib.sha224(text.encode()).hexdigest()[:5]

    @staticmethod
    def _elide_docstring(body):
        """Simplifies function definition by removing its docstring, if it has one."""
        if (len(body) > 1  # docstring plus at least one other stmt
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Str)):
            # print('docstring:', body[0].value.s)
            body.pop(0)

    @staticmethod
    def _apply_indent(indent, str_with_newlines):
        return '\n'.join([indent + line
                          for line in str_with_newlines.splitlines()])

    _at_hex_addr_re = re.compile(r' at 0x[\da-f]+>$')

    @classmethod
    def _elide_addr(cls, name):
        """Elides the address at which an object was allocated,
        as it is uninteresting and will change from run to run."""
        return cls._at_hex_addr_re.sub('>', name)

    def explode_packages(self, top_dir, verbose=False):
        # https://stackoverflow.com/questions/16852811/import-modules-in-a-dir
        for loader, name, is_pkg in pkgutil.walk_packages([str(top_dir)]):

            source_file_loader = loader.find_module(name)
            try:
                module = source_file_loader.load_module(name)
            except SAInvalidRequestError:
                # Table is already defined for this MetaData, use extend_existing=True.
                continue
            # At this point, we could obtain a list of package files
            # by calling importlib.resources.contents(module).
            print(f'\n{is_pkg}  {module.__file__}')

            for name, value in inspect.getmembers(module):
                if name in self._ignore_names_in_module:
                    continue
                source = ''
                try:
                    str_value = self._elide_addr(str(value))
                    # e.g. <module 'collections'
                    # from '/.../miniconda3/envs/.../lib/python3.7/collections/__init__.py'>
                    if (str_value.endswith(' (built-in)>')
                            or '/miniconda3/envs/' in str_value):
                        continue
                    print(module.__name__, name, str_value[:100])
                    source = getsource(value)
                except (_pickle.PicklingError,
                        RuntimeError,
                        TypeError):
                    # flask_sqlalchemy may want to pickle a DB connection.
                    # FlaskAPI may report: Working outside of request context.
                    # None is not a module, function, or code object.
                    pass
                if verbose:
                    print(source)


@click.command()
@click.argument('top_dir')
def main(top_dir):
    """
Usage: exploder.py TOP_DIR

You may want to invoke in this way:

    $ code_explode/exploder.py `git rev-parse --show-toplevel`
    """
    top_dir = Path(top_dir)
    expl = SourceCodeExploder()
    expl.explode_packages(top_dir)
    expl.explode_fs_tree(top_dir)


if __name__ == '__main__':
    main()
