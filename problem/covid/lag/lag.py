#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
from pathlib import Path

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.svm import LinearSVR
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import typer

from problem.covid.us_cases_deaths import get_cases_and_deaths


def _get_daily_cases_and_deaths():
    df = get_cases_and_deaths()
    df.cases = df.cases.diff().shift(-1)
    df.deaths = df.deaths.diff().shift(-1)
    df = df.dropna()
    df.cases = df.cases.astype(np.int32)
    df.deaths = df.deaths.astype(np.int32)

    # clip a March 2022 negative deaths figure
    df.cases = df.cases.clip(lower=0)
    df.deaths = df.deaths.clip(lower=0)

    df = df.set_index('date')
    return df


def predict(out_file=Path('~/Desktop/lag.png')):
    out_file = Path(out_file).expanduser()

    df = _get_daily_cases_and_deaths()
    train, test = _split(df)
    assert len(train) >= 224

    # dates = df.index.get_level_values(0)
    # from sklearn.preprocessing import StandardScaler
    # x_train = np.array(StandardScaler().fit_transform(train.cases))
    x_train = np.array(train.cases)
    y_train = np.array(train.deaths)

    model = RandomForestRegressor()
    model.fit(x_train.reshape(-1, 1), y_train)

    x_test = np.array(test.cases)
    y_test = np.array(test.deaths)
    y_pred = model.predict(x_test.reshape(-1, 1))

    _, axs = plt.subplots(1, 2)
    plt.sca(axs[0])
    train['cases'] /= 1e2
    sns.scatterplot(data=train)
    plt.xticks(rotation=45)
    y_limit = 6_000
    plt.gca().set_ylim((0, y_limit))

    plt.sca(axs[1])
    test['cases'] /= 1e2
    test['pred_deaths'] = y_pred
    sns.scatterplot(data=test)
    plt.xticks(rotation=45)
    plt.gca().set_ylim((0, y_limit))
    plt.savefig(out_file)

    print(f'R2: {model.score(x_test.reshape(-1, 1), y_test):.3f}')
    print(f'MSE: {np.mean((y_test - y_pred)**2):.3f}')
    print(f'MAE: {np.mean(np.abs(y_test - y_pred)):.3f}')


def _split(df: pd.DataFrame, split_date='2020-09-01'):
    train = df.query(f'date < "{split_date}"')
    test = df.query(f'date >= "{split_date}"')
    assert len(df) == len(train) + len(test)  # no rows left behind
    return (train.copy(),
            test.copy())


if __name__ == '__main__':
    typer.run(predict)
