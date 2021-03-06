
---
author: John Hanley
title: Where did the cycles go?
date: 23\textsuperscript{rd} July 2020 [17 slides]
copyright: 2020, see below
---

# Where did the cycles go?

Where did the _time_ go?

(elapsed time, wallclock time)

\blank
Why is this code so _slow_?
\blank

These are age old questions
that arise in every environment.
Today we shall focus on python.

# simple measurement

    import time


    t0 = time.time()
    do_stuff()
    ...
    elapsed = time.time() - t0

\blank
This function wrapper would make a nice python @decorator.

# scenario

The USPS delivers letters,
giving each post office a zipcode.

The Census Bureau offers statistics
for several region sizes, including zipcodes.

We gathered information, including address,
from many prospective customers in southern California.

\blank
We would like to extract the subset of prospects
who live in places where Census demographic data
is available.

# generator, 1 of 1

    #! /usr/bin/env python

    def get_good_zips(out_fspec="/tmp/census.csv"):
        """Finds ZIPS for which Census reports home values."""
        select = """
            SELECT  zipcode
            FROM    simple_zipcode
            WHERE   median_home_value IS NOT NULL
        """
        _rows_to_file(select, out_fspec)

# example code, 1 of 4

    #! /usr/bin/env python

    import csv


    def get_rows(fspec_csv):
        with open(fspec_csv) as fin:
            sheet = csv.reader(fin)
            yield from sheet

    ...

    if __name__ == '__main__':
        assert 60 == count_matches()

# example code, 2 of 4

    def count_matches(
            census_csv="/tmp/census.csv",
            los_angeles_prospects_csv="/tmp/prospects.csv"):
        count = 0
        for zipcode in get_rows(los_angeles_prospects_csv):
            census = sorted(get_rows(census_csv))
            if zipcode in census:
                count += 1

        return count

# where did the time go?

Let's ask the machine.

https://docs.python.org/3/library/profile.html#module-cProfile
\blank

    $ python -m cProfile fm_zips.py | awk '$2 > .001'
       3025848 function calls (3025842 primitive calls) in 2.021 seconds
       Ordered by: standard name
       ncalls tottime percall cumtime  filename:lineno(function)
         2690   0.004   0.000   0.010  codecs.py:319(decode)
            1   0.227   0.227   2.017  fm_zips.py:11(count_matches)
            1   0.002   0.002   2.021  fm_zips.py:3(<module>)
      3019201   1.301   0.000   1.323  fm_zips.py:5(get_rows)
         2690   0.006   0.000   0.006  {_codecs.utf_8_decode}
           96   0.468   0.005   1.790  {builtins.sorted}
           97   0.010   0.000   0.011  {io.open}

# example code, 3 of 4

## hoist constant out of loop

\blank
The zipcodes in `census` do not change.
\blank

    def count_matches( ... ):
        count = 0
        census = sorted(get_rows(census_csv))

        for zipcode in get_rows(los_angeles_prospects_csv):
            if zipcode in census:
                count += 1

        return count

# results, 2 of 4

       32208 function calls (32202 primitive calls) in 0.145 seconds
       Ordered by: standard name
       ncalls tottime percall cumtime  filename:lineno(function)
            1   0.002   0.002   0.003  <frozen importlib._bootstrap_external>:914(get_data)
            1   0.096   0.096   0.134  fm_zips.py:11(count_matches)
            1   0.002   0.002   0.145  fm_zips.py:3(<module>)
        31546   0.030   0.000   0.031  fm_zips.py:5(get_rows)
            1   0.005   0.005   0.005  {_imp.create_dynamic}
            1   0.007   0.007   0.035  {builtins.sorted}

# example code, 4 of 4

## accidentally changed complexity

\blank
The `in` test is O(1) time for a `set`, but O(n) for a `list`.
\blank

    def count_matches( ... ):
        count = 0
        census = set(zipcode
                     for zipcode, in get_rows(census_csv))

        for zipcode in get_rows(los_angeles_prospects_csv):
            if zipcode in census:
                count += 1

        return count

# results, 3 of 4

       for zipcode in get_rows(los_angeles_prospects_csv):
           if zipcode in census:
               count += 1

       63656 function calls (63650 primitive calls) in 0.026 seconds
       Ordered by: standard name
       ncalls tottime percall cumtime  filename:lineno(function)
            1   0.006   0.006   0.023  fm_zips.py:11(count_matches)
        31449   0.006   0.000   0.017  fm_zips.py:15(<genexpr>)
        31546   0.011   0.000   0.011  fm_zips.py:5(get_rows)

# results, 4 of 4

## set intersection
\blank

    def count_matches( ... ):

        return len(set(get_rows(census_csv))
                 & set(get_rows(los_angeles_prospects_csv)))

\blank

    32211 function calls (32205 primitive calls) in 0.027 seconds
       Ordered by: standard name
       ncalls tottime percall cumtime  filename:lineno(function)
            1   0.009   0.009   0.026  fm_zips.py:11(count_matches)
        31546   0.017   0.000   0.017  fm_zips.py:5(get_rows)

# refactor

## returned list -> tuple
\blank

    def get_rows(fspec_csv):
        with open(fspec_csv) as fin:
            sheet = csv.reader(fin)
            yield from map(tuple, sheet)


    def count_matches( ... ):

        return len(set(get_rows(census_csv))
                 & set(get_rows(los_angeles_prospects_csv)))


# regex, 1 of 2

    def grep(fin):
        for line in fin:
            m = re.search(
                r'^(\d{4}:\d{2}:\d{2}) ([\w\.-]+)',
                line)
            if m:
                print(reversed(m.groups()))

\blank

    $ time ./regex1.py  < /tmp/million.txt
    real    0m0.987s

# regex, 2 of 2

## constant hoisting
\blank

    def grep2(fin):
        stamp_pod_re = re.compile(
            r'^(\d{4}:\d{2}:\d{2}) ([\w\.-]+)')

        for line in fin:
            m = stamp_pod_re.search(line)
            if m:
                print(reversed(m.groups()))

\blank

    $ time ./regex2.py  < /tmp/million.txt
    real    0m0.270s

# questions

Questions?

\blank
Experiences?


<!---
Copyright 2020 John Hanley.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
The software is provided "AS IS", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose and noninfringement. In no event shall
the authors or copyright holders be liable for any claim, damages or
other liability, whether in an action of contract, tort or otherwise,
arising from, out of or in connection with the software or the use or
other dealings in the software.
--->
