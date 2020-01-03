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
import datetime as dt
import re

from pandas.plotting import register_matplotlib_converters
import matplotlib
matplotlib.use('Agg')  # noqa E402
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot(df):
    register_matplotlib_converters()
    sns.set()

    fig, (ax1, ax2) = plt.subplots(2)
    ax1.scatter(df.stamp, df.range)
    ax2.scatter(df.stamp, df.odometer)
    fig.autofmt_xdate()

    # g = sns.relplot(x='stamp', y='range', kind='line', data=df)
    # g = sns.relplot(x='odometer', y='range', kind='line', data=df)
    # g.fig.autofmt_xdate()

    folder = Path('~/Desktop').expanduser()
    plt.savefig(folder / 'charge.png')


def read_csv():
    stamp_miles_re = re.compile(
        r'^<(\d{4}-\d+-\d+ \w{3} \d+:\d+)>\s*(\d+)\s+(\d+)')
    fspec = (Path(__file__) / '../charge.txt').resolve()
    rows = []
    with open(fspec) as fin:
        for line in fin:
            m = stamp_miles_re.search(line)
            if m:
                stamp, odometer, range = m.groups()
                stamp = dt.datetime.strptime(stamp, '%Y-%m-%d %a %H:%M')
                rows.append(dict(stamp=stamp,
                                 odometer=int(odometer),
                                 range=int(range)))
    folder = Path('~/Desktop').expanduser()
    out_file = str(folder / 'charge.csv')
    columns = list(rows[0].keys())
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(out_file, columns=columns, index=False)
    return df


if __name__ == '__main__':
    plot(read_csv())
