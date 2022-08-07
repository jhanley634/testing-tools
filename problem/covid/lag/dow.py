#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
from pprint import pp

from problem.covid.lag.lag import get_daily_cases_and_deaths


def day_of_week():
    """Each training example is 15 normalized `cases` values,
    centered on "current day" which is always 1.0,
    plus target value 0-6 for day-of-week.
    ML task is to predict that target.
    """
    df = get_daily_cases_and_deaths(0)
    df = df[['cases']]
    df = df.reset_index()
    print(df)


if __name__ == '__main__':
    day_of_week()
