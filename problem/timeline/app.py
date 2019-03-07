#! /usr/bin/env python

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
