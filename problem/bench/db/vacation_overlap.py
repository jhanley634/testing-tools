#! /usr/bin/env python

"""Al and Ben will each take vacations, with overlap.
How short staffed will the office be, on a daily basis?
"""

import datetime as dt

import sqlalchemy as sa


class Vacation:

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


if __name__ == '__main__':
    Vacation().report()
