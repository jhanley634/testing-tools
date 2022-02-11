#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
from pathlib import Path
import csv
import datetime as dt

import click
import pandas as pd


def _get_rows(fin):
    sheet = csv.DictReader(fin)
    for row in sheet:
        date, time = row['Date'], row['Time']
        stamp = dt.datetime.strptime(f'{date} {time}', '%d %b %Y %I:%M %p')
        yield dict(timestamp=stamp,
                   systolic=int(row['Systolic (mmHg)']),
                   diastolic=int(row['Diastolic (mmHg)']),
                   pulse=int(row['Pulse (bpm)']))


@click.command()
@click.argument('in_file', type=Path)
def main(in_file):
    with open(in_file) as fin:
        df = pd.DataFrame(_get_rows(fin))

    df.to_csv(f'/tmp/{in_file.name}', index=False)


if __name__ == '__main__':
    main()
