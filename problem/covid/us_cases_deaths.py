#! /usr/bin/env streamlit run

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
from collections import defaultdict
from pathlib import Path
import datetime as dt

import altair as alt
import pandas as pd
import streamlit as st


def _now():
    return dt.datetime.now().replace(microsecond=0)


def _get_nyt_covid19_top_dir():
    repo_top = Path(__file__ + '/../../..').resolve()
    sibling_repo = repo_top / '../covid-19-data'  # NY Times repo
    return sibling_repo.resolve()


def get_cases_and_deaths(in_file='us.csv', state=''):
    #            date    cases  deaths
    # 0    2020-01-21        1       0
    # ..          ...      ...     ...
    # 263  2020-10-10  7748030  214184

    df = pd.read_csv(_get_nyt_covid19_top_dir() / in_file)
    df.date = pd.to_datetime(df.date)

    rows = []
    for i, row in df.iterrows():
        if state and row.state != state:
            continue
        rows.append(dict(date=row.date, stat='cases', val=max(row.cases, 1)))
        rows.append(dict(date=row.date, stat='deaths', val=max(row.deaths, 1)))
    return pd.DataFrame(rows)


def _tidy_slow(df):
    rows = defaultdict(dict)
    for i, row in df.iterrows():
        rows[row.date][row.stat] = row.val
    df = pd.DataFrame(rows).T
    assert sorted(df.columns) == ['cases', 'deaths']
    assert df.dropna().shape == df.shape
    return df


def tidy(df: pd.DataFrame):
    df.to_csv('/tmp/covid-messy.csv', index=False)
    df = df.pivot(index='date', columns='stat', values='val')
    df.columns.name = None  # was 'stat'
    df['date'] = pd.to_datetime(df.date)
    df = df.set_index('date')
    # d = np.datetime64(dt.datetime(2020, 1, 25)); print(df.loc[d])
    assert 3 == df.loc['2020-01-25']['cases']
    df.to_csv('/tmp/covid-tidy.csv')
    assert sorted(df.columns) == ['cases', 'deaths']
    assert df.dropna().shape == df.shape
    return df


def smooth(df, span=7):
    cases = df[df.stat == 'cases'].val.ewm(span=span).mean()
    deaths = df[df.stat == 'deaths'].val.ewm(span=span).mean()
    for i in range(0, len(df), 2):
        assert df.stat.iloc[i] == 'cases'
        assert df.stat.iloc[i + 1] == 'deaths'
        df.loc[i, 'val'] = cases.iloc[i // 2]
        df.loc[i + 1, 'val'] = deaths.iloc[i // 2]


def delta(df):
    """Computes delta values, in place (e.g. daily new cases)."""
    prev_cases = 0
    prev_deaths = 0
    for i, row in df.iterrows():
        if row.stat == 'cases':
            d = row.val - prev_cases
            prev_cases = row.val
        elif row.stat == 'deaths':
            d = row.val - prev_deaths
            prev_deaths = row.val
        else:
            assert None, row
        df.loc[i, 'val'] = d


def get_chart(df, scale_type='linear'):
    return (alt.Chart(df)
            .mark_line()
            .encode(x=alt.X('date'),
                    y=alt.Y('val', scale=alt.Scale(type=scale_type)),
                    color='stat',
                    strokeDash='stat'))


def main():
    df = get_cases_and_deaths()
    st.altair_chart(get_chart(df))
    st.altair_chart(get_chart(df, 'log'))
    delta(df)
    smooth(df)
    st.altair_chart(get_chart(df))
    print(_now())


if __name__ == '__main__':
    main()
