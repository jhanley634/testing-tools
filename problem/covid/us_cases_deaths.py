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
    return df


def main():
    df = get_cases_and_deaths()
    scale = alt.Scale(type='log')
    st.altair_chart(alt.Chart(df)
                    .mark_circle()
                    .encode(x=alt.X('date'),
                            y=alt.Y('cases', scale=scale)))
    print(_now())


if __name__ == '__main__':
    main()
