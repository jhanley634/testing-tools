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

from problem.incremental_row_copy.table_updater import TableUpdater
from problem.incremental_row_copy.tbl_event_log import EventLog
from problem.incremental_row_copy.tbl_event_log_copy import EventLogCopy


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
        tables = (
            EventLog.__table__,
            EventLogCopy.__table__,
        )
        meta = sa.MetaData(bind=self.engine)
        meta.create_all(tables=tables)

    def test_update(self):
        dest_name = EventLogCopy.__tablename__
        src_name = EventLog.__tablename__
        self.assertEqual(0, num_rows(self.engine, dest_name))
        self.assertEqual(0, num_rows(self.engine, src_name))
        upd = TableUpdater(self.engine, EventLog, EventLogCopy)

        gen_events(self.engine, 7)
        upd.update()
        self.assertEqual(7, num_rows(self.engine, src_name))
        self.assertEqual(7, num_rows(self.engine, dest_name))

        gen_events(self.engine, 2)
        upd.update()
        self.assertEqual(9, num_rows(self.engine, src_name))
        self.assertEqual(9, num_rows(self.engine, dest_name))

        # Now update a src event log message, and verify it appears in dest.
        msg = 'six'
        self.assertEqual(0, len(list(upd.sess.query(EventLog).filter(
            EventLog.event == 'msg'))))

        six = list(upd.sess.query(EventLog).filter(EventLog.id == 6))[0]
        six.stamp = dt.datetime.now()
        six.event = msg
        upd.sess.commit()
        upd.update()
        self.assertEqual(1, len(list(upd.sess.query(EventLog).filter(
            EventLog.event == 'msg'))))


if __name__ == '__main__':
    unittest.main()
