#! /usr/bin/env python

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

import unittest

import pandas as pd


def constant_columns(df):
    """Returns uninformative boring column names of a dataframe."""
    first = df.iloc[0]
    cols = set(df.columns)  # potentially boring columns
    for i, row in df.iterrows():
        for informative_col in {col
                                for col in cols
                                if row[col] != first[col]}:
            cols.remove(informative_col)

    return sorted(cols)


def interesting_columns(df):
    """Returns non-constant column names of a dataframe."""
    return sorted(set(df.columns) - set(constant_columns(df)))


class ConstantColumnsTest(unittest.TestCase):

    @staticmethod
    def get_example_df(num_boring_cols=4, num_rows=1000):
        """Produces three 'informative' columns, plus some boring ones."""
        boring_vals = {chr(ord('c') + i): 0
                       for i in range(num_boring_cols)}
        rows = []
        for i in range(num_rows):
            vals = dict(a=i, b=2 * i, z=i)
            rows.append({**vals, **boring_vals})

        columns = sorted(rows[0].keys())
        return pd.DataFrame(rows, columns=columns)

    def test_constant_columns(self):
        df = self.get_example_df()
        self.assertEqual('c d e f'.split(), constant_columns(df))
        self.assertEqual('a b z'.split(), interesting_columns(df))


if __name__ == '__main__':
    unittest.main()
