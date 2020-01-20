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
import subprocess

import pkg_resources as pkg


def get_pkg_names():
    for line in subprocess.check_output('conda list'.split()).decode().splitlines():
        if not line.startswith('#'):
            # columns are: Name Version Build Channel
            pkg_name = line.split()[0]
            yield pkg_name


def report():
    for name in get_pkg_names():
        report_on(name)


def report_on(name):
    try:
        meta = pkg.get_distribution(name)
    except pkg.DistributionNotFound:
        return  # Skips binaries e.g. arrow-cpp, boost-cpp, brotli, bzip2, c-ares.
    folder = Path(meta.egg_info)
    try:
        import_name = get_imports(folder / 'top_level.txt')[0].rstrip()
    except FileNotFoundError:
        return  # Skips the entrypoints-0.3 package
    if meta.project_name != import_name:
        print(meta.project_name.ljust(18), import_name.ljust(18), meta.version)


def get_imports(fspec):
    with open(fspec) as fin:
        lines = fin.readlines()
        return sorted(lines, key=_underscores_to_the_end)


def _underscores_to_the_end(s):
    # The '_' character is between 'Z' & 'a'. This helper moves it past 'z',
    # so names starting with a letter will sort earlier than underscore names.
    return s.replace('_', '~')


if __name__ == '__main__':
    report()
