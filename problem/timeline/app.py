#! /usr/bin/env python

from flask_api import FlaskAPI

from problem.timeline.presidents import get_us_presidents


app = FlaskAPI(__name__)
df = get_us_presidents()


@app.route('/president')
def president():
    row = df.loc[43]
    for i, row in df.iterrows():
        print('\n'.join(dir(row)))
    print(row)
    return {'result': row.to_dict()}


if __name__ == '__main__':
    app.run(debug=True)
