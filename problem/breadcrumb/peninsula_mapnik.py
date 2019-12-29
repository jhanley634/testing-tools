#! /usr/bin/env python3

# Copyright 2017 John Hanley.
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

import mapnik
import problem.breadcrumb.world as world  # for styling


def make_sf_bay_area_map(out_file='peninsula.png'):  # quality of map is low
    bb = mapnik.Box2d(-122.7, 37.2, -121.5, 37.6)  # bb.center() -122.1, 37.4
    m = mapnik.Map(900, 900)
    m.background = mapnik.Color('lightblue')
    m.append_style('my-style', world.get_style())
    # mapnik.PostGIS(dbname='osm', table='planet_osm_point')
    ds = mapnik.GeoJSON(file='san-francisco-bay_california_osm_line.geojson')
    layer = mapnik.Layer('world')
    layer.datasource = ds
    layer.styles.append('my-style')
    m.layers.append(layer)
    m.zoom_to_box(bb)  # m.zoom_all()
    mapnik.render_to_file(m, out_file, 'png')


if __name__ == '__main__':
    os.chdir('/tmp')
    make_sf_bay_area_map()
