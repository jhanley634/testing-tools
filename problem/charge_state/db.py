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

import sqlalchemy as sa

from problem.charge_state.charge import read_csv
from problem.charge_state.model import Base


def get_url():
    return 'sqlite:////tmp/charge.db'


def insert(uri='sqlite:////tmp/charge.db'):
    df = read_csv()
    assert len(df) > 0

    engine = sa.create_engine(get_url())
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    insert()
