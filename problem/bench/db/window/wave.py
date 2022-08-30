#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
"""Produces a saw-tooth waveform.
"""
import datetime as dt


def _create_table(name):
    return f"""
    DROP TABLE  IF EXISTS  {name};

    CREATE TABLE  IF NOT EXISTS  {name} (
      id          INTEGER  PRIMARY KEY  AUTOINCREMENT,
      -- symbol   TEXT,
      stamp       DATETIME,
      price       REAL
    );
    """


def populate_and_query(table_name='price'):
    print(_create_table(table_name))
    day = dt.date(2022, 1, 1)
    for i in range(40):
        print(f'INSERT INTO {table_name}'
              f' VALUES (NULL, "{day}", {i % 10});')
        day += dt.timedelta(days=1)

    print(_query(table_name))


def _query(name):
    return f""".echo on

        SELECT
            stamp,
            price,
            ROUND(AVG(price) OVER (
                ORDER BY stamp
                ROWS BETWEEN 2 PRECEDING AND 0 FOLLOWING
            ), 3) AS mov_avg
        FROM {name}
        WHERE stamp BETWEEN '2022-01-01' AND '2022-01-21'
;
    """


if __name__ == '__main__':
    populate_and_query()
