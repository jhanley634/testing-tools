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

from decimal import Decimal

import pandas as pd
import pydeck as pdk
import streamlit as st
import uszipcode

from problem.pop_map.grid.degree_size import step_size


def _get_rows(pop_thresh=30_000):
    select = f"""
        SELECT    lat, lng AS lon, population, major_city
        FROM      simple_zipcode
        WHERE     lat > 0
                  AND zipcode_type = 'Standard'
                  AND state NOT IN ('AK', 'HI', 'PR')
                  AND population >= {pop_thresh}
        ORDER BY  zipcode
    """
    search = uszipcode.SearchEngine()
    return list(map(dict, search.ses.execute(select)))


class GridCell:
    """Models 1 dimension of a geographic grid.

    Consider a chessboard. Then a grid cell is one of 64 squares.
    As we scan a raster of 8 cells, left to right,
    a grid cell models the left and right boundaries of a cell.

    We use repeated addition, rather than base + i * step.
    This motivates adding Decimals, scaled integers,
    to avoid annoying roundoff effects.
    """

    @staticmethod
    def _dec(n):
        """Converts to scaled integer, to avoid IEEE-754 roundoff nonsense."""
        # Repeatedly applying this function won't change n.
        return Decimal(str(n))  # We use str() because
        # python 3.1 and later will choose the shortest decimal
        # using David Gay's algorithm.
        # https://docs.python.org/3/tutorial/floatingpoint.html
        # https://docs.python.org/3/whatsnew/3.1.html#other-language-changes
        # https://web.archive.org/web/2006/http://ftp.ccs.neu.edu/pub/people/will/retrospective.pdf
        # round-trip: https://people.csail.mit.edu/jaffer/r5rs/Numerical-input-and-output.html

    def __init__(self, west, lng_step):
        self.west = self._dec(west)
        self.lng_step = self._dec(lng_step)

    def contains(self, lng):
        """Predicate."""
        lng = self._dec(lng)
        assert self.west <= lng  # Caller must play nice, e.g. Honolulu is west of WA.
        return lng < self.west + self.lng_step

    def advance_to(self, lng):
        """Moves western boundary by one or more grids."""
        assert not self.contains(lng)
        while not self.contains(lng):
            self.west += self.lng_step
        assert self.contains(lng)


class GridMap:

    def __init__(self, pop_thresh=30_000):
        self.pop_thresh = pop_thresh
        self.ses = uszipcode.SearchEngine().ses

    def _get_select(self, bottom, top):
        return f"""
        SELECT    lat, lng AS lon, population, major_city
        FROM      simple_zipcode
        WHERE     lat > 0
                  AND zipcode_type = 'Standard'
                  AND state NOT IN ('AK', 'HI', 'PR')
                  AND population >= {self.pop_thresh}
                  AND {bottom} <= lat AND lat < {top}
        ORDER BY  lng
    """

    def get_grid_counts(self):
        rows = []
        lat_step, lng_step = step_size()
        oak_island_mn = 49.3  # N lat
        key_west_fl = Decimal('24.6')
        lat = key_west_fl
        while lat <= oak_island_mn:
            select = self._get_select(lat, lat + lat_step)
            rows += self._get_raster_counts(select, lng_step)
            lat += lat_step
        return rows

    def _get_raster_counts(self, select, lng_step):

        def _get_dict():
            return dict(count=count,
                        total_pop=total_pop,
                        lat=b_lat,
                        lon=b_lng)

        neah_bay_wa = -125  # degrees W lng, approximately
        grid = GridCell(neah_bay_wa, lng_step)
        count = total_pop = 0
        b_lat = b_lng = b_pop = 0  # Biggest city within a grid.

        for lat, lng, pop, city in self.ses.execute(select):
            if not grid.contains(lng):
                if count:
                    yield _get_dict()
                grid.advance_to(lng)
                count = total_pop = 0
                b_lat = b_lng = b_pop = 0
            assert grid.contains(lng)
            count += 1
            total_pop += pop
            if b_pop < pop:  # new max?
                b_pop = pop
                b_lat = lat
                b_lng = lng
        if count:  # final, most eastern grid in a raster
            yield _get_dict()


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
    # df = pd.DataFrame(_get_rows())
    df = pd.DataFrame(GridMap().get_grid_counts())
    print(df)
    st.map(df)


if __name__ == '__main__':
    main()
