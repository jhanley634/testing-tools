
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

from pathlib import Path
import pandas as pd

"""Reads morbidity stats from https://github.com/nytimes/covid-19-data.git"""


def _get_nyt_covid_repo():
    top = Path(f'{__file__}/../../../..')  # git rev-parse --show-toplevel
    return (top / '../covid-19-data').resolve()


def get_state_stats():
    df = pd.read_csv(_get_nyt_covid_repo() / 'us-states.csv')
    df['date'] = pd.to_datetime(df.date)
    return df


def get_county_stats():
    df = pd.read_csv(_get_nyt_covid_repo() / 'us-counties.csv')
    # df = df[~df.county.isin(['Unknown', 'New York City', 'Kansas City'])]
    df = df[~df.fips.isna()]
    df['fips'] = df.fips.astype('int32')
    df['date'] = pd.to_datetime(df.date)
    return df
