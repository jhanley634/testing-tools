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

import datetime as dt
import re

import bs4
import pandas as pd
import requests


def get_us_presidents(
        url='https://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States'):
    current_year = dt.date.today().year
    mdy_re = re.compile(r'.*?\w+ \d+, (?P<year>\d{4})(?P<rest>.*)')
    born_died_re = re.compile(r'(?P<born>\d{4}).?(?P<died>\d{4})?')
    html = requests.get(url).text
    soup = bs4.BeautifulSoup(html, features='lxml')
    pres_tbl = soup.find_all('table')[1]
    rows = []
    for i, row in enumerate(pres_tbl.find_all('tr')):
        if i <= 1:
            continue
        tds = row.find_all('td')
        if len(tds) < 8:
            continue
        id = int(tds[0].text)
        assert 1 <= id <= 45, id
        term = tds[1].text.replace('Incumbent', f'January 20, {current_year}')
        # date_spans = term.find_all('span', class_='date')
        # for span in date_spans:
        years = []
        for _ in range(2):
            m = mdy_re.search(term)
            years.append(int(m.groupdict()['year']))
            term = m.groupdict()['rest'] or ''
        life = tds[3]
        a = life.find_next('big').find_next('a')
        name = a.text
        born, died = born_died_re.search(life.text).groups()
        died = died or current_year
        born, died = map(int, (born, died))
        rows.append(dict(id=id,
                         born=born,
                         died=died,
                         start=years[0],
                         end=years[1],
                         name=name))
    df = pd.DataFrame(rows, columns=rows[0].keys())
    df.to_csv('/tmp/presidents.csv', index=False)
    return df


if __name__ == '__main__':
    get_us_presidents()
