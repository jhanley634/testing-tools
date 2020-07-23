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

def get_rows(fspec_csv):
    with open(fspec_csv) as fin:
        sheet = csv.reader(fin)
        yield from sheet


def count_matches(
        census_csv="/tmp/census.csv",
        los_angeles_prospects_csv="/tmp/prospects.csv"):
    count = 0
    for zipcode in get_rows(los_angeles_prospects_csv):
        census = sorted(get_rows(census_csv))
        if zipcode in census:
            count += 1

    return count


if __name__ == '__main__':
    assert 60 == count_matches()
