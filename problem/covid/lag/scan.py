#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
from pprint import pp

from problem.covid.lag.lag import predict


def scan():
    mae = []
    for i, lag in enumerate(range(60)):
        print(f'\nlag {i}')
        mae.append((round(predict(i), 3), i))

    pp(mae)
    print('')
    pp(sorted(mae))


if __name__ == '__main__':
    scan()
