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

import uszipcode

search = uszipcode.SearchEngine()


def _rows_to_file(select, out_fspec):
    with open(out_fspec, "w") as fout:
        sheet = csv.writer(fout)
        for row in search.ses.execute(select):
            sheet.writerow(row)


def get_good_zips(out_fspec="/tmp/census.csv"):
    """Finds ZIPS for which Census reports home values."""
    # zipcode_type is {PO Box, Standard, Unique},
    # and each type may list home values.
    select = """
        SELECT  zipcode
        FROM    simple_zipcode
        WHERE   median_home_value IS NOT NULL
    """
    _rows_to_file(select, out_fspec)


def get_prospect_zips(out_fspec="/tmp/prospects.csv"):
    select = """
        SELECT  zipcode
        FROM    simple_zipcode
        WHERE   major_city = 'Los Angeles'
                AND state = 'CA'
    """
    _rows_to_file(select, out_fspec)


if __name__ == '__main__':
    get_good_zips()
    get_prospect_zips()
