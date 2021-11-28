#! /usr/bin/env python
#
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
#
from pathlib import Path

from pandas_profiling import ProfileReport
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import matplotlib
import matplotlib.pyplot as plt

from problem.numeric.us_home_sales.synthetic import gen_synthetic_dataset


def main(out_folder=Path('~/Desktop').expanduser()):

    data = gen_synthetic_dataset(permute=False)

    fspec = out_folder / 'synth_profile.html'
    if not fspec.exists():
        profile = ProfileReport(data, title='Pandas Profiling Report')
        profile.to_file(fspec)

    x, y = data.iloc[:, :-1], data.iloc[:, -1]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    regr = DecisionTreeRegressor(max_depth=4)
    regr.fit(x_train, y_train)

    y_pred = regr.predict(x_test)

    matplotlib.use('MacOSX')
    plt.scatter(x_test.attr000, y_pred, color='cornflowerblue', label='predicted', linewidth=2)
    plt.xlabel('data')
    plt.ylabel('target')
    plt.title('Decision Tree Regression')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
