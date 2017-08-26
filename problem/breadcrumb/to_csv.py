#! /usr/bin/env python3

# Copyright 2017 John Hanley.
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

import argparse
import csv
import os

from sqlalchemy import Table

import dbcred


def to_csv(table_name, out_fspec):
    table = Table(table_name, META, autoload=True, autoload_with=ENGINE)
    with open(out_fspec, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        for row in CONN.execute(table.select()):
            wr.writerow(row)


def arg_parser():
    p = argparse.ArgumentParser()
    p.add_argument('--db', default='breadcrumb', help='INI file section name')
    p.add_argument('--table', default='trip_point', help='MySQL table name')
    p.add_argument('--out-file', default='trip_point.csv', help='output CSV')
    p.add_argument('--out-dir', default='/tmp',
                   help='directory for unqualified output filename')
    return p


if __name__ == '__main__':
    args = arg_parser().parse_args()
    CONN, ENGINE, META = dbcred.get_cem(args.db)
    os.chdir(args.out_dir)
    to_csv(args.table, args.out_file)
