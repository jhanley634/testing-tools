#! /usr/bin/env streamlit run

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
        rows.append(dict(date=row.date, stat='cases', val=row.cases))
        rows.append(dict(date=row.date, stat='deaths', val=row.deaths))
    return pd.DataFrame(rows)


def main():
    df = get_cases_and_deaths()
    scale = alt.Scale(type='log')
    scale = alt.Scale()
    st.altair_chart(alt.Chart(df)
                    .mark_line()
                    .encode(x=alt.X('date'),
                            y=alt.Y('val', scale=scale),
                            color='stat',
                            strokeDash='stat'))

    # from vega_datasets import data
    # source = data.stocks()
    # source = data.jobs.url
    # df = pd.read_json(data.jobs.url).set_index('year')

    print(_now())


if __name__ == '__main__':
    main()
