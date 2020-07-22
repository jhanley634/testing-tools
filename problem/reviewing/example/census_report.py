#! /usr/bin/env python

import csv

import uszipcode


def get_good_zips(out_fspec="/tmp/census.csv"):
    """Finds ZIPS for which Census reports home values."""
    search = uszipcode.SearchEngine()
    # zipcode_type is {PO Box, Standard, Unique},
    # and each type may list home values.
    select = """
        SELECT zipcode
        FROM   simple_zipcode
        WHERE  median_home_value IS NOT NULL
    """
    with open(out_fspec, "w") as fout:
        sheet = csv.writer(fout)
        for row in search.ses.execute(select):
            sheet.writerow(row)


if __name__ == '__main__':
    get_good_zips()
