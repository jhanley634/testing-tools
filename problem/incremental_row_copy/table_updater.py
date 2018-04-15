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

import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.schema as schema
import sqlalchemy.sql as sql


class TableUpdater:
    """Performs incremental dest updates as src rows are updated / inserted.

    Dest table will have same columns as src, plus `active` & `epoch` columns.
    """

    def __init__(self,
                 engine: sa.engine.Engine,
                 src_table: schema.Table,
                 dest_table: schema.Table):
        self.sess = self._get_session(engine)
        self.src_table = src_table
        self.dest_table = dest_table
        self.prev_stamp = None  # We know dest rows <= prev_stamp are current.

    def update(self):
        self.prev_stamp = list(self.sess.query(
            sa.func.max(self.dest_table.stamp)))[0][0]

        if self.prev_stamp is None:  # zero rows in dest table
            self._copy_all_rows()
        else:
            self._update_recently_modified_rows()
            self._copy_new_rows()

        self.sess.commit()

    def _update_recently_modified_rows(self):
        """Inserts copies of recent rows, with epoch in PK bumped by +1."""
        prev_epoch = list(self.sess.query(
            sa.func.max(self.dest_table.epoch)))[0][0]

        src_rows = list(self.sess.query(self.src_table).filter(
            self.src_table.stamp > self.prev_stamp))
        pk_to_src_row = {src_row: (src_row.stamp, src_row.id)
                         for src_row in src_rows}

        dst_rows = list(self.sess.query(self.dest_table).filter(
            self.dest_table.stamp > self.prev_stamp))
        pk_to_dst_row = {dst_row: (dst_row.stamp, dst_row.id)
                         for dst_row in dst_rows}
        dst_rows_modified = []
        for (stamp, id), src_row in pk_to_src_row.items():
            dst_row = pk_to_dst_row.get((stamp, id))
            if dst_row:
                dst_row.is_active = False
                dst_row.epoch = prev_epoch + 1
                dst_rows_modified.append(dst_row)

    def _copy_new_rows(self):
        for row in self.sess.query(self.src_table).filter(
                self.src_table.stamp > self.prev_stamp):
            self.sess.add(self._dest_table_row_copy(row))

    def _copy_all_rows(self):
        """Copies src into an empty dest table."""
        # self.sess.execute(str(self.dest_table.__table__.delete()))
        sql.delete(self.dest_table)

        for row in self.sess.query(self.src_table):
            self.sess.add(self._dest_table_row_copy(row))

    def _get_session(self, engine) -> orm.session.Session:
        """
        Returns a DB session, with the advantage of explicit type annotation.
        """
        return orm.sessionmaker(bind=engine)()

    def _dest_table_row_copy(self, row, is_active=True, epoch=1):
        """Adds two columns to a source row: is_active & epoch."""
        def col_name(col):
            t_name, sep, c_name = str(col).partition('.')
            return c_name

        d = {col_name(col): getattr(row, col_name(col))
             for col in row.__table__.columns}
        d = dict(d, is_active=is_active, epoch=epoch)
        return self.dest_table(**d)


# if __name__ == '__main__':
#     main()
