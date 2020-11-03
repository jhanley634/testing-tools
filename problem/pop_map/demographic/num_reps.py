#! /usr/bin/env python

# Copyright 2020 John Hanley.
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

import pandas as pd


# https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/IG0UN2
# https://dataverse.harvard.edu/api/access/datafile/3814252?format=original&gbrecs=true

def _get_num_districts(in_file='/tmp/1976-2018-house2.csv'):
    df = pd.read_csv(in_file, encoding='latin-1')
    df = df[(df.year == 2018) & (df.district >= 0) & ~df.writein]
    df = df[['state_po', 'district', 'candidate', 'party', 'candidatevotes']]
    df = df.rename(columns={'state_po': 'state'})
    df = df[['state', 'district']]
    df = df.drop_duplicates(['state', 'district'])
    return df.append([dict(state='DC', district=42)])


def main():
    df = _get_num_districts().groupby('state').agg('count').rename(columns={
        'district': 'electors'})
    df.electors += 2
    print(df)


if __name__ == '__main__':
    main()
