#! /usr/bin/env python

import re
import sys


def grep(fin):
    stamp_pod_re = re.compile(
        r'^(\d{4}:\d{2}:\d{2}) ([\w\.-]+)')

    for line in fin:
        m = stamp_pod_re.search(line)
        if m:
            print(reversed(m.groups()))


if __name__ == '__main__':
    grep(sys.stdin)
