#! /usr/bin/env python

import unittest

import pandas as pd


def constant_columns(df):
    """Returns uninformative boring column names of a dataframe."""
    first = df.iloc[1]
    cols = set(df.columns)
    for i, row in df.iteritems():
        print(row)
        for col in cols:
            print(col)

    return ''


class ConstantColumnsTest(unittest.TestCase):

    @staticmethod
    def get_example_df(num_boring_cols=2, num_rows=12):
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
        self.assertEqual('', constant_columns(df))


if __name__ == '__main__':
    unittest.main()
