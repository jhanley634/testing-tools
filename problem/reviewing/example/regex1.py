#! /usr/bin/env python

import re
import sys


def grep(fin):
    for line in fin:
        m = re.search(
            r'^(\d{4}:\d{2}:\d{2}) ([\w\.-]+)',
            line)
        if m:
            print(reversed(m.groups()))


if __name__ == '__main__':
    grep(sys.stdin)
