#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.

import pandas as pd


def report():
    print(read_event_table())
    print(read_event_table().dtypes)


def read_event_table(year=2022):
    base = 'https://en.wikipedia.org/wiki'
    url = f'{base}/List_of_mass_shootings_in_the_United_States_in_{year}'
    events, by_month, _ = pd.read_html(url)
    assert 14 == len(by_month)
    assert len(events) >= 570

    # strip trailing citations
    events['City'] = events['City'].str.replace(r' \(\d+\)$', '', regex=True)

    # coerce to numeric
    for col in ['Dead', 'Injured']:
        events = _parse_numeric_column(events, col)

    # parse dates -- note that there may be a few rows with same date
    fmt = '%B %d %Y'  # full month names
    events['date'] = pd.to_datetime(events[f'{year} date'] + f' {year}', format=fmt)
    events.drop(columns=['Description', f'{year} date'], inplace=True)

    return events


def _parse_numeric_column(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Downcases a column name, and coerces it from str to (positive) int."""
    assert col == col.title()  # .title & .lower give us distinct column names
    df[col.lower()] = pd.to_numeric(df[col].str.replace(r'^(\d+).*', r'\1', regex=True))
    return df.drop(columns=[col])


if __name__ == '__main__':
    report()
