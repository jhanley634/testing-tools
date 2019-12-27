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

from pathlib import Path

import pandas as pd


def _to_dollars(s: str):
    s = s.replace(' USD per Hour', '')
    return float(s)


def _cols_to_delete():
    return [
        'Instance family',
        'Instance size',
        'Availability zones',
        'Free-Tier eligible',
        'Bare metal',
        'Hypervisor',
        'Dedicated Host support',
        'On-Demand Hibernation support',
        'Burstable Performance support',
        'Valid cores',
        'Local instance storage',
        'Storage type',
        'Storage disk count',
        'EBS encryption support',
        'EBS optimization support',
        'Network performance',
        'ENA support',
        'Maximum number of network interfaces',
        'IPv4 addresses per interface',
        'IPv6 addresses per interface',
        'IPv6 support',
        'Supported placement group strategies',
        'Auto Recovery support',
        'Supported root devices',
        'Current generation',
    ]


def report():
    in_fspec = Path(f'{__file__}/../instancetypes.csv').resolve()
    df = pd.read_csv(in_fspec)
    del df['On-Demand Windows pricing']
    df['On-Demand Linux pricing'] = (
        df['On-Demand Linux pricing'].apply(_to_dollars))
    df = df.rename(columns={'On-Demand Linux pricing': 'price',
                            'Threads per core': 'tpc',
                            'Valid threads per core': 'vtpc',
                            'Sustained clock speed (GHz)': 'GHz'})
    df = df[df['Current generation']]
    df = df[df.vCPUs > 8]
    for col_name in _cols_to_delete():
        if col_name:
            del df[col_name]
    df['price/core'] = df['price'] / df['vCPUs']
    df.sort_values(by=['price/core', 'vCPUs'], inplace=True)
    df.to_csv('/tmp/t.csv', index=False)

    print(df.head(40))


if __name__ == '__main__':
    report()
