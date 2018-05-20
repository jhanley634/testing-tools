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

import matplotlib.pyplot as plt
import numpy as np
import sklearn.linear_model
import sqlalchemy.ext.declarative
from sqlalchemy import Table
from sqlalchemy.orm import scoped_session, sessionmaker

import problem.retain.etl as etl


Base = sqlalchemy.ext.declarative.declarative_base()
Session = scoped_session(sessionmaker())


def get_table(name='s_customer_value'):
    '''Given the name of a relation (table or view), return its ORM object.'''
    return Table(name, META, autoload=True, autoload_with=ENGINE)


def model(table):
    model1(table, table.c.order_size, table.c.retained)
    # model1(table, table.c.units, table.c.retained)


def model1(table, feature, target):
    q = (Session.query(feature, target)
         .filter(feature < 60)
         .order_by(feature))
    pairs = [(float(feat), targ)
             for feat, targ in q]
    x = np.array([feat for feat, targ in pairs])[np.newaxis].T
    y = np.array([targ for feat, targ in pairs])[np.newaxis].T
    fit(x, y)


def fit(x, y):
    regr = sklearn.linear_model.LinearRegression()
    regr.fit(x, y)
    print(regr)
    print('coefficient: ', regr.coef_)
    print('mean squared error: %.2f'
          % np.mean((regr.predict(x) - y) ** 2))
    print('Variance score: %.2f'
          % regr.score(x, y))
    ax = plt.gca()
    ax.set_ylabel('units in initial order')
    ax.set_ylabel('customer retention (0 for not retained)')
    plt.title('units vs. retention')
    plt.scatter(x, y, color='black')
    plt.plot(x, regr.predict(x), color='blue', linewidth=3)
    plt.yticks(())
    plt.savefig('model.pdf')


if __name__ == '__main__':
    DB, ENGINE, META = etl.get_db_connection()
    Session.configure(bind=ENGINE)
    model(get_table('t_customer'))
