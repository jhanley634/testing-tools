#! /usr/bin/env python

# Copyright 2019 John Hanley.
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

from flask_api import FlaskAPI
import numpy as np

from problem.timeline.presidents import get_us_presidents


app = FlaskAPI(__name__)
df = get_us_presidents()


def _make_serializable(x):
    """Returns a JSON-serializable version of the input x."""
    if isinstance(x, np.int64):
        return int(x)
    return x


def as_dict(row):
    return {k: _make_serializable(v)
            for k, v in row.to_dict().items()}


# e.g. http://localhost:5000/president/42

@app.route('/president/<int:id>')
def president(id):
    """Returns the record for a single person."""
    row = df.iloc[id - 1]
    return {'result': as_dict(row)}


# e.g. http://localhost:5000/time/2007

@app.route('/time/<int:year>')
def time(year):
    """Returns list of presidents alive in a given year."""
    rows = [as_dict(row)
            for _, row in df.iterrows()
            if row.born <= year <= row.died]
    return {'result': rows}


if __name__ == '__main__':
    app.run(debug=True)
