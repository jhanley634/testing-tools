#! /usr/bin/env python

import csv

def get_rows(fspec_csv):
    with open(fspec_csv) as fin:
        sheet = csv.reader(fin)
        yield from sheet


def count_matches(census_csv, los_angeles_prospects_csv):
    census = sorted(get_rows(census_csv))
    for
