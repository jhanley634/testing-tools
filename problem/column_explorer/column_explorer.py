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

import click
import sqlalchemy as sa
import sqlalchemy.sql.sqltypes as sqltypes
import sqlalchemy.dialects.postgresql.base as pg_base
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

    def _get_table(self, table_name):
        kwargs = dict(autoload=True)
        table_short_name = table_name
        if '.' in table_name:
            schema, table_short_name = table_name.split('.')
            kwargs['schema'] = schema
        meta = sa.MetaData(bind=self.engine)
        return sa.Table(table_short_name, meta, **kwargs)

    def show_informative_columns(self, table_name):
        """A column is uninformative if it has a constant value, e.g. always NULL."""
        tbl = self._get_table(table_name)
        cnt, = self.engine.execute(f'select count(*) from {table_name}').fetchone()
        if cnt <= 1:
            return  # Nothing to see here, by definition there are no informative columns.
        for column, _ in self._get_cols(tbl):
            select = f'select count(distinct {column}) from {table_name}'
            cnt, = self.engine.execute(select).fetchone()
            # print(f'{cnt:8d}  {column}')
            if cnt > 1:
                print(column + ',')

    def report(self, table_name, round_digits=3):

        tbl = self._get_table(table_name)
        stat = None
        non_numeric = set([
            sqltypes.BLOB,
            sqltypes.BOOLEAN,
            sqltypes.CHAR,
            sqltypes.DATE,
            sqltypes.TEXT,
            sqltypes.VARCHAR,
            pg_base.CIDR,
            pg_base.ENUM,
            pg_base.INET,
            pg_base.INTERVAL,
            pg_base.TIME,
            pg_base.TIMESTAMP,
        ])

        cnt, = self.engine.execute(f'select count(*) from {table_name}').fetchone()
        print(f'# {table_name}\n{cnt} rows, {len(tbl.c)} columns\n')

        for column, typ in self._get_cols(tbl):
            print('\n## ' + column)
            for agg in ['min(', 'avg(', 'max(', 'mode',
                        'mode count', 'nulls', 'count(distinct ']:
                params = {}
                select = f'select {agg}{column}) from {table_name}'
                if agg == 'avg(' and typ in non_numeric:
                    continue
                if agg == 'mode':
                    select = (f'select {column}  from {table_name}'
                              f' group by {column}  order by count(*) desc  limit 1')
                    if cnt == 0:
                        continue
                if agg == 'mode count':
                    params = dict(val=stat)
                    select = f'select count(*) from {table_name} where {column} = :val'
                if ((agg == 'nulls')
                        or (agg == 'mode count' and stat is None)):
                    select = f'select count(*) from {table_name} where {column} is null'

                stat, = self.engine.execute(sa.text(select), params).fetchone()

                if agg == 'avg(' and stat is not None:
                    stat = round(stat, round_digits)
                if agg == 'nulls':
                    pct = round(100 * stat / cnt, round_digits)
                    stat = f'{stat} ({pct} %)'
                print('-', agg.replace('(', ' '), stat)

        print(f'\n{cnt} rows in {table_name}')

    def _get_cols(self, table):
        for col in table.columns:
            if type(col.type) != sqltypes.BOOLEAN:  # Can't take max(B) of boolean B.
                yield str(col).split('.')[-1], type(col.type)


@click.command()
@click.option('--uri-getter', default='get_zipcode_cs')
@click.option('--table', default='simple_zipcode')
def main(uri_getter, table):
    callable = globals()[uri_getter]
    ce = ColumnExplorer(callable())
    # ce.show_informative_columns(table)
    ce.report(table)


if __name__ == '__main__':
    main()
