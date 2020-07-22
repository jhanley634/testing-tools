#! /usr/bin/env python

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
