#! /usr/bin/env python3

# Copyright 2017 John Hanley.
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

from sqlalchemy import Table
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.functions import sum as sum1
import matplotlib.pyplot as plt
import numpy as np
import sqlalchemy.ext.declarative

import problem.retain.etl as etl

Base = sqlalchemy.ext.declarative.declarative_base()
Session = scoped_session(sessionmaker())


# class ByCust(Base):
#     __tablename__ = 's_customer_value'
#     total_revenue = Column(DECIMAL(precision=31, scale=2))
#     num_units = Column(INTEGER())
#     num_orders = Column(INTEGER())
#     num_order_seqs = Column(INTEGER())
#     active_days = Column(INTEGER())
#     customer_id = Column(INTEGER(), primary_key=True)


def get_table(name='s_customer_value'):
    '''Given the name of a relation (table or view), return its ORM object.'''
    return Table(name, META, autoload=True, autoload_with=ENGINE)


def get_revenue_grand_total():
    q = Session.query(sum1(etl.Order.revenue))
    return DB.execute(str(q)).fetchall()[0][0]  # a single-row 1-tuple


def explore_by_customer(table):
    '''What does revenue look like as a function of customer stickiness?'''
    q = (Session.query(table.c.revenue)
         .filter(table.c.num_order_seqs <= 40)
         .order_by(table.c.num_order_seqs))
    rev = [float(r) / 1e3 for (r,) in q]
    n = len(rev)
    plt.step(range(n), np.cumsum(rev))
    plt.title("cumulative revenue per max order_seq")
    ax = plt.gca()
    ax.set_xlabel("customer max order_seq")
    ax.set_ylabel("cumulative revenue, in $1K's")
    # ax.invert_xaxis()
    # plt.show()
    plt.savefig('rev_by_max_order_seq.pdf')


if __name__ == '__main__':
    DB, ENGINE, META = etl.get_db_connection()
    Session.configure(bind=ENGINE)
    explore_by_customer(get_table('s_customer_value_by_order_seqs'))
