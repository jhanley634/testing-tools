#! /usr/bin/env python3

# Copyright 2017 John Hanley.
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


import itertools


def filter(target, all_vals):
    '''Discard values that obviously won't help us get to the target sum.'''

    # pre-condition: positive integers
    for val in all_vals:
        assert val > 0, val

    return [val
            for val in all_vals
            if val <= target]


def find_addends(target, all_vals):
    '''Given a list of positive integers,
    compute all subsets that exactly add up to some target value.
    There can be multiple instances of a given integer, so
    the list essentially is a multi-set.
    '''
    return [
        list(vals)
        for vals in powerset(filter(target, all_vals))
        if target == sum(vals)
    ]


def _get_test_data():
    return [
        (9, [1, 2, 3], []),
        (9, [10, 11], []),
        (9, [10, 11, 1], []),
        (9, [8, 6, 7], []),
        (8, [5, 3], [[5, 3]]),
        (8, [5, 3, 1], [[5, 3]]),
        (8, [9, 6, 1, 1], [[6, 1, 1]]),
        (8, [6, 1, 1], [[6, 1, 1]]),
        (8, [6, 1, 1, 1], [[6, 1, 1], [6, 1, 1], [6, 1, 1]]),
        (8, [5, 2, 2, 1], [[5, 2, 1], [5, 2, 1]]),
        (8, [5, 2, 2, 1, 9], [[5, 2, 1], [5, 2, 1]]),
    ]


def test1():
    for target, vals, expected in _get_test_data():
        print('')
        print(target, vals)
        answer = find_addends(target, vals)
        assert expected == answer, answer
        # Verify the post-condition:
        for vals in answer:
            s = sum(vals)
            assert target == s, (s, vals)


# from https://docs.python.org/3/library/itertools.html
def powerset(s):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1))


if __name__ == '__main__':
    test1()
