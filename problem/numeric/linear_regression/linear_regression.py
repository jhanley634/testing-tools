#! /usr/bin/env python

# Copyright 2021 John Hanley.
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
from random import gauss

from scipy.optimize import minimize
import pandas as pd


def noisy_line(x: float, m=2, b=3, mu=0, sigma=.1) -> float:
    return m * x + b + gauss(mu, sigma)

def gen_random_dataset(k=12):
    df = pd.DataFrame([
        dict(x=10 * x, y=noisy_line(x))
        for x in range(k)
    ])
    print(minimize(loss, (0, df.mean().y), args=(df,)))


def loss(params, df):
    m, b = params
    se = 0
    for i, row in df.iterrows():
        se += (m * row.x + b - row.y) ** 2
    mse = se / len(df)
    return mse


if __name__ == '__main__':
    gen_random_dataset()
