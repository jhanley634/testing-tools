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

import unittest

import bs4
import pandas as pd
import requests


class HtmlTableParser:
    """An HTML -> BeautifulSoup -> DataFrame pipeline.
    """

    def __init__(self, url):
        req = requests.get(url)
        soup = bs4.BeautifulSoup(req.text, 'html5lib')

        # It may prove convenient to expose more bs4 selectors to the caller.
        self._tables = soup.find_all('table')

    def num_tables(self):
        return len(self._tables)

    def to_tabular(self, table_number=0):
        """Returns a list of rows, each a list of K columns.
        """
        rows = []
        tbl = self._tables[table_number]
        if tbl.find('th'):
            rows.append([th.text.replace(' ', '_')
                         for th in tbl.find_all('th')])
        for tr in tbl.find_all('tr'):
            row = [td.text
                   for td in tr.find_all('td')]
            if row:
                rows.append(row)

        return rows

    def to_df_with_col_hdrs(self, table_number=0):
        rows = self.to_tabular(table_number)
        assert len(rows) > 1, rows
        return pd.DataFrame(rows[1:], columns=rows[0])

    def to_csv(self, table_number=0):
        return self.to_df_with_col_hdrs(table_number).to_csv()


class ParseHtmlTableTest(unittest.TestCase):

    def test_parse_coreutils(self):
        url = 'https://www.gnu.org/software/coreutils/filesystems.html'
        tp = HtmlTableParser(url)
        self.assertEqual(1, len(tp._tables))
        df = tp.to_df_with_col_hdrs()
        csv = tp.to_csv()
        self.assertEqual(0, len(csv.split('\n')[-1]))  # Last line is blank.
        extra = 2  # 1st extra line: column headers, 2nd: trailing newline.
        self.assertEqual(extra + len(df), len(csv.split('\n')))
        self.assertGreaterEqual(len(df), 120)
        self.assertEqual(
            'Identifier  File_System  Minimal_Version  Revision  Remarks',
            '  '.join(df.columns))
        # print(' '.join(sorted(df.File_System)))


if __name__ == '__main__':
    unittest.main()
