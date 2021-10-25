#! /usr/bin/env python
from collections import defaultdict
from pathlib import Path
import csv
import datetime as dt

import matplotlib
matplotlib.use('Agg')  # noqa E402
import matplotlib.pyplot as plt  # noqa E402
import pandas as pd  # noqa E402


def group_by_month(infile='/tmp/us_sales.csv'):
    with open(infile) as fin:
        csvfile = csv.DictReader(fin)
        for row in csvfile:
            date = row['saledate']
            y_m = date[:7]
            yield y_m, row['saleprice']


def report():
    total = defaultdict(float)  # maps year_month to total sales
    count = defaultdict(int)
    for y_m, price in group_by_month():
        total[y_m] += float(price)
        count[y_m] += 1

    rows = []
    for y_m in sorted(total.keys()):
        mean = total[y_m] / count[y_m]
        day = dt.datetime.strptime(y_m, '%Y-%m')
        print(f"{y_m}   {mean:0.2f}")
        rows.append(dict(y_m=day, mean=mean))

    df = pd.DataFrame(rows)
    print(df)

    plt.scatter(df.y_m, df['mean'])
    plt.xticks(rotation=45, ha='right')
    plt.savefig(Path('~/Desktop/plot.png').expanduser())


if __name__ == '__main__':
    report()
