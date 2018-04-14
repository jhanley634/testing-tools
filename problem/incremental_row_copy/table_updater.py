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


class TableUpdater:
    """Performs incremental dest updates as src rows are updated / inserted.

    Dest table will have same columns as src, plus `active` & `epoch` columns.
    """

    def __init__(self,
                 engine: sa.engine.Engine,
                 src_table: schema.Table,
                 dest_table: schema.Table):
        self.engine = engine
        self.src_table = src_table
        self.dest_table = dest_table

    def update(self):
        self.copy()

    def copy(self):
        sess = self._get_session()

        delete = str(self.dest_table.__table__.delete())
        sess.execute(delete)

        for row in sess.query(self.src_table):
            sess.add(self._dest_table_row_copy(row))

        sess.commit()

    def _get_session(self):
        return orm.sessionmaker(bind=self.engine)()

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
