#! /usr/bin/env python

from pathlib import Path
import datetime as dt


def _get_headings(infile=Path('start_with_a_test.md')):
    with open(infile) as fin:
        for line in fin:
            if line.startswith('# '):
                yield line


def report(minutes_per_slide=3):
    i = 1
    stamp = dt.datetime.strptime('2021-05-11 12:35', '%Y-%m-%d %H:%M')
    for heading in _get_headings():
        i += 1
        hh_mm = stamp.strftime('%H:%M')
        print(f'<p>{i:02d} &nbsp; {hh_mm}  {heading}'.replace('>0', '>&nbsp;'))
        stamp += dt.timedelta(minutes=minutes_per_slide)


if __name__ == '__main__':
    print('&nbsp;')
    report()
