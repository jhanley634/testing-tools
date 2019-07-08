#! /usr/bin/env python3

# Copyright 2018 John Hanley.
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

import os
import pprint

from unyt import m, mile
import folium
import uszipcode


class NearbyZips:

    def __init__(self):
        self.search = uszipcode.SearchEngine()

    def plot_zip(self, zipcode, fspec='~/Desktop/map.html'):
        r = self.search.by_zipcode(zipcode)
        radius = r.radius_in_miles * mile
        nw = r.bounds_north, r.bounds_west
        se = r.bounds_south, r.bounds_east
        sp = '&nbsp;'

        map_ = folium.Map(
            location=(r.lat, r.lng),
            tiles='Stamen Terrain',
        )
        msg = f'{zipcode}, radius{sp}={sp}{radius}'
        folium.Circle(
            location=[r.lat, r.lng],
            radius=radius.to_value('m'),
            tooltip=msg,
            color='purple',
        ).add_to(map_)
        folium.CircleMarker(
            location=[r.lat, r.lng],
            radius=6,  # px
            popup=msg,
            color='purple',
            fill=True,
            fill_opacity=.8,
        ).add_to(map_)
        folium.Rectangle(
            bounds=(nw, se),
            tooltip=msg,
            color='DarkBlue',
        ).add_to(map_)

        map_.save(os.path.expanduser(fspec))


if __name__ == '__main__':
    NearbyZips().plot_zip(90210)
