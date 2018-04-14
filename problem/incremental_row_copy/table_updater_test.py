#! /usr/bin/env python3

# Copyright 2018 John Hanley.
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

from pathlib import Path
import datetime as dt
import os
import unittest

import sqlalchemy as sa
import sqlalchemy.orm as orm

from problem.incremental_row_copy.tbl_event_log import EventLog


def gen_events(engine: sa.engine.Engine, n):
    sess = orm.sessionmaker(bind=engine)()
    for i in range(int(n)):
        event = EventLog(
            stamp=dt.datetime.now(),
            id=i % 10,
            event='foo %7d' % i)
        sess.add(event)
    sess.commit()


def num_rows(engine, table_name):
    query = f'select count(*) from {table_name}'
    return engine.execute(query).fetchone()[0]


class TableUpdaterTest(unittest.TestCase):

    def setUp(self, unlink=True):
        db_file = Path(os.environ.get('EVENT_DB_FILE', '/tmp/event_log.db'))
        if unlink and db_file.exists():
            db_file.unlink()  # We start afresh each time.
        self.db_url = f'sqlite:///{db_file}'
        self.engine = sa.create_engine(self.db_url)
        meta = sa.MetaData(bind=self.engine)
        meta.create_all(tables=[EventLog.__table__])

    def test_update(self):
        tbl = EventLog.__tablename__
        self.assertEqual(0, num_rows(self.engine, tbl))
        gen_events(self.engine, 7)
        self.assertEqual(7, num_rows(self.engine, tbl))


if __name__ == '__main__':
    unittest.main()
