#! /usr/bin/env python

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

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

from . import covid19_stats as c19


def modify_doc(doc):
    """Add a plotted function to the document.

    Arguments:
        doc: A bokeh document to which elements can be added.
    """
    ds = c19.Transform()
    x_values = ds.us_stat.date
    y_values = ds.us_stat.cases
    data_source = ColumnDataSource(data=dict(x=x_values, y=y_values))
    plot = figure(title="covid cases",
                  tools="crosshair,pan,reset,save,wheel_zoom", )
    plot.line('x', 'y', source=data_source, line_width=3, line_alpha=0.6)
    doc.add_root(plot)
    doc.title = "covid19 cases"


def main():
    modify_doc(curdoc())


main()
