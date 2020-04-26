
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


class Extract:

    @staticmethod
    def _get_nyt_covid19_repo():
        top = Path(f'{__file__}/../../../..')  # git rev-parse --show-toplevel
        return (top / '../covid-19-data').resolve()

    def __init__(self):
        covid = self._get_nyt_covid19_repo()
        self.us_stat = pd.read_csv(covid / 'us.csv')
        self.state_stat = pd.read_csv(covid / 'us-states.csv')
        self.county_stat = pd.read_csv(covid / 'us-counties.csv')


class Transform(Extract):

    def __init__(self):
        super().__init__()

        df = self.county_stat
        df = df[~df.fips.isna()].copy()
        df['fips'] = df.fips.astype('int32')
        self.county_stat = df

        for df in [self.us_stat,
                   self.state_stat,
                   self.county_stat]:
            df['date'] = pd.to_datetime(df.date)


class Load:
    """Empty -- we don't upload to a server such as RDBMS or S3."""
