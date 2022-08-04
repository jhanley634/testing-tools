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
import datetime as dt

from altair import Chart, datum
import streamlit as st

from problem.covid.us_cases_deaths import (
    delta,
    get_chart,
    get_filtered_cases_and_deaths,
    smooth,
)


def _get_annotation(df):
    # https://en.wikipedia.org/wiki/Sturgis_Motorcycle_Rally
    rally = 1e3 * dt.datetime.strptime('2020-08-07', '%Y-%m-%d').timestamp()
    ten_days = 10 * 1e3 * 86400
    annotation = Chart(df).mark_text(
        align='left',
        baseline='middle',
        fontSize=20,
        dx=7
    ).encode(
        x='date',
        y='val',
        text='label'
    ).transform_filter(
        (rally <= datum.date) & (datum.date < rally + ten_days)
    )
    return annotation


def main():
    df = get_filtered_cases_and_deaths('us-states.csv', 'South Dakota')
    df['label'] = '.'
    st.altair_chart(get_chart(df) + _get_annotation(df))
    st.altair_chart(get_chart(df, 'log') + _get_annotation(df))
    delta(df)
    smooth(df, span=7)
    st.altair_chart(get_chart(df) + _get_annotation(df))


if __name__ == '__main__':
    main()
