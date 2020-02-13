#! /usr/bin/env python

# Copyright 2020 John Hanley.
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
import importlib
import pprint
import subprocess
import sys

import pkg_resources as pkg


class ImportToPkg:

    def __init__(self):
        self.import_to_pkg = dict(self.get_import_to_pkg())

    def get_pkg_names(self):
        for line in subprocess.check_output('conda list'.split()).decode().splitlines():
            if not line.startswith('#'):
                # columns are: Name Version Build Channel
                pkg_name = line.split()[0]
                yield pkg_name

    def get_import_to_pkg(self):
        for name in self.get_pkg_names():
            try:
                meta = pkg.get_distribution(name)
            except pkg.DistributionNotFound:
                continue  # Skips binaries: arrow-cpp, boost-cpp, brotli, bzip2, c-ares.
            folder = Path(meta.egg_info)
            try:
                import_name = self._get_imports(folder / 'top_level.txt')[0].rstrip()
            except FileNotFoundError:
                continue  # Skips the entrypoints-0.3 package
            try:
                importlib.import_module(import_name)
                sys.modules[import_name]  # Verify that it actually _was_ imported.
            except ModuleNotFoundError:
                continue  # Skips 'amd' from cvxopt.

            yield import_name, meta.project_name

    @classmethod
    def _get_imports(cls, fspec):
        with open(fspec) as fin:
            lines = fin.readlines()
            return sorted(lines, key=cls._underscores_to_the_end)

    @staticmethod
    def _underscores_to_the_end(s):
        # The '_' character is between 'Z' & 'a'. This helper moves it past 'z',
        # so names starting with a letter will sort earlier than underscore names.
        return s.replace('_', '~')


if __name__ == '__main__':
    pprint.pprint(ImportToPkg().import_to_pkg)
