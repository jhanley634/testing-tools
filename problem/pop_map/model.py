#! /usr/bin/env python

# Copyright 2019 John Hanley.
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
import pprint

import matplotlib
import pandas as pd
import sklearn.linear_model
import uszipcode
import uszipcode.db
import uszipcode.model

matplotlib.use('Agg')  # noqa E402
import matplotlib.pyplot as plt  # noqa E402


def _query_by_zip(zipcode=94025):
    zse = uszipcode.SearchEngine()
    r = zse.by_zipcode(zipcode)
    # print('\n'.join(dir(r)))
    pprint.pprint(dict(r.to_OrderedDict()))
    density, income = (
        r.population_density,      # people / sq. mi.
        r.median_household_income  # USD
    )
    return density, income


def query_by_state(state='CA'):
    sess = uszipcode.SearchEngine().ses
    tbl = uszipcode.model.SimpleZipcode
    return (sess.query(tbl.zipcode,
                       tbl.population_density,
                       tbl.median_household_income.label('income'),
                       tbl.median_home_value.label('home_value'),
                       )
            .filter(tbl.zipcode_type == 'Standard')
            .filter(tbl.population_density > 0)
            .filter(tbl.median_household_income > 0)
            .filter(tbl.median_home_value > 0)
            .filter(tbl.state == state))


def main():
    dest_dir = Path('~/Desktop/').expanduser()

    tbl = uszipcode.model.SimpleZipcode
    q = query_by_state('CA').filter(tbl.zipcode >= 95100)
    df = pd.DataFrame(list(q)).set_index('zipcode')

    # sns.pairplot(df)

    x, y = (df.income.values.reshape(-1, 1),
            df.home_value)
    regr = sklearn.linear_model.LinearRegression()
    regr.fit(x, y)
    plt.scatter(x, regr.predict(x), c='k')
    plt.scatter(x, y, c='b')

    ax = plt.gca()
    ax.set_xlabel('income')
    ax.set_ylabel('home price')
    plt.savefig(dest_dir / 'plot.png')


if __name__ == '__main__':
    main()
