#! /usr/bin/env python

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
