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
import uszipcode


def get_zipcode_session():
    return uszipcode.SearchEngine().ses


def get_zipcode_cs():
    """Returns a JDBC connect string for the zipcode database."""
    # typical value: sqlite:////Users/foo/.uszipcode/simple_db.sqlite
    return get_zipcode_session().connection().engine.url


class ColumnExplorer:

    def __init__(self, cs_or_engine):
        self.engine = sa.create_engine(cs_or_engine)

    def report(self, table_name):
        for column in self._get_col_names(table_name):
            print('\n## ' + column)
            for agg in ['min', 'avg', 'max', 'count(distinct ']:
                if '(' not in agg:
                    agg += '('
                select = f'select {agg}{column}) from {table_name}'
                stat, = self.engine.execute(select).fetchone()
                print('-', agg.replace('(', ' '), stat)

        cnt, = self.engine.execute(f'select count(*) from {table_name}').fetchone()
        print(f'\n{cnt} rows in {table_name}')

    def _get_col_names(self, table_name):
        meta = sa.MetaData(bind=self.engine)
        tbl = sa.Table(table_name, meta, autoload=True)
        return map(str, tbl.columns)


if __name__ == '__main__':

    ColumnExplorer(get_zipcode_cs()).report('simple_zipcode')
