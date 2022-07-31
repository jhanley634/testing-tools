#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
import pandas as pd
import typer

from problem.covid.us_cases_deaths import get_cases_and_deaths, tidy


def predict():
    train, test = _split(tidy(get_cases_and_deaths()))
    print(train.shape)
    print(test.shape)


def _split(df: pd.DataFrame, split_date='2020-09-01'):
    train = df.query(f'date < "{split_date}"')
    test = df.query(f'date >= "{split_date}"')
    assert len(df) == len(train) + len(test)  # no rows left behind
    return train, test


if __name__ == '__main__':
    typer.run(predict)
