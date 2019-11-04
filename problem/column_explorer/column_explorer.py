#! /usr/bin/env python3

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

"""Systematically finds aggregate stats for a table's columns."""

import sqlalchemy as sa


class ColumnExplorer:

    def __init__(self, cs_or_engine):
        self.engine = sa.create_engine(cs_or_engine)

    def report(self, table_name):
        for column in self._get_col_names(table):
            print('\n' + column)
            for agg in ['min', 'avg', 'max']:
                for row in self.engine.execute(
                        f'select {agg}({column}) from {table_name}'):
                    print(row[0])


if __name__ == '__main__':
    ColumnExplorer().report('example')
