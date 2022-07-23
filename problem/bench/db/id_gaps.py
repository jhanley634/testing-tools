#! /usr/bin/env python

# Copyright 2021 John Hanley.
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
from sqlalchemy import text
from sqlalchemy.engine.base import Engine
from uszipcode import SearchEngine


class GapFinder:

    def __init__(self, engine: Engine):
        self.engine = engine

    def _get_ids(self):
        select = 'SELECT zipcode  FROM simple_zipcode  ORDER BY 1'
        with self.engine.connect() as conn:
            for id_, in conn.execute(text(select)):
                yield int(id_)

    def _get_filtered_ids(self, k=100):
        """We discard most input rows, yielding every K-th ID."""
        # The final ID typically is suppressed, for random number of input rows.
        countdown = 0
        for id_ in self._get_ids():
            if countdown == 0:
                yield id_
                countdown = k
            countdown -= 1

    def measure_gaps(self):
        prev = 0
        for id_ in self._get_filtered_ids():
            delta = id_ - prev
            print(delta, id_)
            prev = id_


if __name__ == '__main__':
    """example usage:

    $ ./id_gaps.py | cat -n | sort -nk2
    """
    GapFinder(SearchEngine().engine).measure_gaps()
