#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
import typer

from problem.covid.us_cases_deaths import get_cases_and_deaths, tidy


def predict():
    df = tidy(get_cases_and_deaths())
    print(df)


if __name__ == '__main__':
    typer.run(predict)
