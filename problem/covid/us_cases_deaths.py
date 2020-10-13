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


def get_cases_and_deaths():
    #            date    cases  deaths
    # 0    2020-01-21        1       0
    # ..          ...      ...     ...
    # 263  2020-10-10  7748030  214184

    df = pd.read_csv(_get_nyt_covid19_top_dir() / 'us.csv')
    df.date = pd.to_datetime(df.date)

    rows = []
    for i, row in df.iterrows():
        rows.append(dict(date=row.date, stat='cases', val=row.cases + 1))
        rows.append(dict(date=row.date, stat='deaths', val=row.deaths + 1))
    return pd.DataFrame(rows)


def _get_chart(df, scale_type='linear'):
    return (alt.Chart(df)
            .mark_line()
            .encode(x=alt.X('date'),
                    y=alt.Y('val', scale=alt.Scale(type=scale_type)),
                    color='stat',
                    strokeDash='stat'))


def main():
    df = get_cases_and_deaths()
    st.altair_chart(_get_chart(df))
    st.altair_chart(_get_chart(df, 'log'))
    print(_now())


if __name__ == '__main__':
    main()
