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

import csv
import datetime as dt
import re
import sys


def parse_date(d):
    return dt.datetime.strptime(d, '%d/%b/%Y:%H:%M:%S +0000')


def convert(fin, sheet):
    sheet.writerow('ip stamp_utc url status length referer ua'.split())
    log_re = re.compile(r'([\d\.]+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"')
    stamp_idx = 1
    for line in fin:
        m = log_re.search(line)
        if m:
            row = list(m.groups())
            row[stamp_idx] = parse_date(row[stamp_idx])
            sheet.writerow(row)
        else:
            print(line.rstrip())


def main(in_filespec):
    assert in_filespec.endswith('.txt')
    out_filespec = re.sub(r'\.txt$', '.csv', in_filespec)
    with open(in_filespec) as fin:
        with open(out_filespec, 'w') as fout:
            sheet = csv.writer(fout)
            convert(fin, sheet)


if __name__ == '__main__':
    main(sys.argv[1])
