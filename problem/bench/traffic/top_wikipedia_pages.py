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

from collections import namedtuple
from operator import attrgetter
import pprint

import pandas as pd
import requests

Pageviews = namedtuple('pageviews', 'article rank views'.split())


def csv_from_json(date='2020/01/22', out_fspec='/tmp/pv.csv', verbose=False):
    base = ('https://wikimedia.org/api/rest_v1/metrics'
            '/pageviews/top/en.wikipedia.org/all-access')
    url = f'{base}/{date}'
    print(url)
    req = requests.get(url)
    req.raise_for_status()
    articles = req.json()['items'][0]['articles']
    articles = [Pageviews(**article)
                for article in articles]
    if verbose:
        pprint.pprint(sorted(articles, key=attrgetter('views')))
    df = pd.DataFrame(articles)
    print(df)
    df.to_csv(out_fspec, index=False)


if __name__ == '__main__':
    csv_from_json()
