#! /usr/bin/env python

# Copyright 2021 John Hanley.
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
from subprocess import check_output
import re
import sys


class FileReporter:

    def __init__(self, infile):
        self.infile = Path(infile)

    def report_on_source(self):
        with open(self.infile) as fin:
            self._shortlog()
            lines = fin.readlines()
            self._restate_imports(lines)
            self._show_file_contents(lines)

    def _shortlog(self):
        cmd = f'git shortlog -s {self.infile}'
        log = check_output(cmd.split()).decode()
        print(f'*** {log} ***.')

        for line in log.splitlines():
            print(f'{self.infile}:0:  {line}')

    def _restate_imports(self, lines):
        """Duplicates some import lines so it's easy to: grep ': import FavePkg'.
        """
        from_re = re.compile(r'^from\s+(\w+) import ')
        for line in lines:
            m = from_re.search(line)
            if m:
                pkg = m.group(1)
                print(f'{self.infile}:0: import {pkg}')

    def _show_file_contents(self, lines):
        for i, line in enumerate(lines):
            print(f'{self.infile}:{i + 1}: {line.rstrip()}')


def main(files):
    for file in files:
        if ' ' not in file:  # Quoting? Meh!
            FileReporter(file).report_on_source()


if __name__ == '__main__':
    assert len(sys.argv) > 1
    main(sys.argv[1:])
