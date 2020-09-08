#! /usr/bin/env python

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

import folium
import sqlalchemy as sa
import unyt
import uszipcode


class NearbyZips:

    def __init__(self):
        self.search = uszipcode.SearchEngine()

    def _get_zipcode_table(self):
        con = self.search.ses.connection()
        meta = sa.MetaData(bind=con)
        return sa.Table('simple_zipcode', meta, autoload=True)

    def zips_near(self, zipcode):
        zipcode = f'{int(zipcode):05d}'
        r = self.search.by_zipcode(zipcode)
        lng_bounds = r.bounds_west, r.bounds_east
        lat_bounds = r.bounds_south, r.bounds_north
        zips = self._get_zipcode_table()
        q = (self.search.ses
             .query(zips.c.zipcode)
             .filter(zips.c.zipcode_type == 'Standard')
             # NW, NE, SE, SW
             .filter((zips.c.bounds_north.between(*lat_bounds)
                      & zips.c.bounds_west.between(*lng_bounds))
                     | (zips.c.bounds_north.between(*lat_bounds)
                        & zips.c.bounds_east.between(*lng_bounds))
                     | (zips.c.bounds_south.between(*lat_bounds)
                        & zips.c.bounds_east.between(*lng_bounds))
                     | (zips.c.bounds_south.between(*lat_bounds)
                        & zips.c.bounds_west.between(*lng_bounds)))
             .order_by(zips.c.zipcode)
             )
        return list({zipcode for zipcode, in q})

    def plot_zips(self, zipcodes, fspec='~/Desktop/map.html'):
        r = self.search.by_zipcode(zipcodes[0])
        map_ = folium.Map(
            location=(r.lat, r.lng),
            tiles='Stamen Terrain',
        )
        for zipcode in zipcodes:
            self._plot_zip(zipcode, map_)

        map_.save(os.path.expanduser(fspec))

    def _plot_zip(self, zipcode, map_):
        r = self.search.by_zipcode(zipcode)
        radius = r.radius_in_miles * unyt.mile
        nw = r.bounds_north, r.bounds_west
        se = r.bounds_south, r.bounds_east
        sp = '&nbsp;'

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
            fill_opacity=.7,
        ).add_to(map_)
        folium.Rectangle(
            bounds=(nw, se),
            tooltip=msg,
            color='DarkBlue',
        ).add_to(map_)


if __name__ == '__main__':
    nz = NearbyZips()
    nz.plot_zips(nz.zips_near(90210))
