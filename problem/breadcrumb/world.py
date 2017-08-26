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

# This code is based on
# https://github.com/mapnik/mapnik/wiki/GettingStartedInPython


def get_style():
    s = mapnik.Style()
    r = mapnik.Rule()
    polygon_symbolizer = mapnik.PolygonSymbolizer()
    polygon_symbolizer.fill = mapnik.Color('#f2eff9')
    r.symbols.append(polygon_symbolizer)
    # to add outlines to a polygon we create a LineSymbolizer
    line_symbolizer = mapnik.LineSymbolizer()
    line_symbolizer.stroke = mapnik.Color('rgb(50%,50%,50%)')
    line_symbolizer.stroke_width = 0.1
    r.symbols.append(line_symbolizer)
    s.rules.append(r)
    return s


def make_world_map():  # Well, hello, world! Pleased to meet you.
    m = mapnik.Map(1200, 600)
    m.background = mapnik.Color('steelblue')
    m.append_style('my-style', get_style())
    ds = mapnik.Shapefile(file='ne_110m_admin_0_countries.shp')
    layer = mapnik.Layer('world')
    layer.datasource = ds
    layer.styles.append('my-style')
    m.layers.append(layer)
    m.zoom_all()
    mapnik.render_to_file(m, 'world.png', 'png')


if __name__ == '__main__':
    # DatasourceCache plugins:
    #   csv gdal geojson ogr pgraster postgis raster shape sqlite topojson
    os.chdir('/tmp')
    make_world_map()
