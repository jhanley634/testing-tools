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

import pandas as pd
import pydeck as pdk
import streamlit as st
import uszipcode


def _get_rows(pop_thresh=30_000):
    select = f"""
        SELECT    zipcode_type, zipcode, lat, lng AS lon, population, major_city
        FROM      simple_zipcode
        WHERE     lat > 0
                  AND state NOT IN ('AK', 'HI', 'PR')
                  AND population >= {pop_thresh}
        ORDER BY  1, 2
    """
    search = uszipcode.SearchEngine()
    return list(map(dict, search.ses.execute(select)))


def foo(df):
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=df,
                get_position='[lon, lat]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))


def main():
    df = pd.DataFrame(_get_rows())
    # st.map(df)
    foo(df)
    print(len(df), len(_get_rows(60_000)))


if __name__ == '__main__':
    main()
