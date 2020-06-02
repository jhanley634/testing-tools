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

import datetime as dt

import sqlalchemy as sa


class Vacation:
    """Al and Ben will each take vacations, with overlap.
    How short staffed will the office be, on a daily basis?
    """

    def __init__(self):
        self.engine = sa.create_engine('sqlite:////tmp/vacation.db')

    def _create_tables(self):
        create_emp = """
            CREATE TABLE emp (
              name        TEXT  PRIMARY KEY,
              vac_start   DATE  NOT NULL,
              vac_end     DATE  NOT NULL
            )
        """
        self.engine.execute(create_emp)

        create_calendar = """
            CREATE TABLE calendar (
              day        DATE  PRIMARY KEY
            )
        """
        self.engine.execute(create_calendar)

    def _populate_tables(self):
        for ins in [
            "INSERT INTO emp  VALUES ('Al', '2020-02-03', '2020-02-16')",
            "INSERT INTO emp  VALUES ('Ben', '2020-02-10', '2020-02-23')",
        ]:
            self.engine.execute(ins)

        day = dt.date(2020, 2, 1)
        for _ in range(28):
            ins = sa.text("INSERT INTO calendar  VALUES (:day)")
            self.engine.execute(ins, dict(day=day))
            day += dt.timedelta(days=1)

    def report(self):
        self._create_tables()
        self._populate_tables()
        select = """
            SELECT   day, COUNT(*) as cnt
            FROM     calendar c
            JOIN     emp es  ON es.vac_start <= c.day
            JOIN     emp ee  ON ee.vac_end   >= c.day
                             AND es.name = ee.name
            GROUP BY day
            ORDER BY day
        """
        print(select)
        for row in self.engine.execute(select):
            print(row)


if __name__ == '__main__':
    Vacation().report()
