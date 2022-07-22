#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
"""
Write a function, def solution(A):
that, given an array A of N integers, returns the smallest positive integer
(greater than 0) that does not occur in A.

For example, given A = [1, 3, 6, 4, 1, 2], the function should return 5.

Given A = [1, 2, 3], the function should return 4.

Given A = [−1, −3], the function should return 1.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [1..100,000];
        each element of array A is an integer within the range [−1,000,000..1,000,000].
"""
import unittest

from hypothesis import given
import hypothesis.strategies as st


class TestDemo(unittest.TestCase):

    def test_demo(self):
        self.assertEqual(5, solution([1, 3, 6, 4, 1, 2]))
        self.assertEqual(1, solution([-1, -3]))
        self.assertEqual(1, solution([-839912, -570792]))


@given(a=st.lists(st.integers(min_value=-1_000_000, max_value=1_000_000),
                  min_size=1, max_size=10))
def hypo_demo(a):
    assert 0 < len(a) <= 10

    n = solution(a)
    assert n not in a
    assert n > 0


def solution(a):
    s = set(a)
    small = max(1, min(s))
    large = max(1, 1 + max(s))
    for i in range(small, large + 1):
        if i not in s:
            return i


if __name__ == '__main__':
    hypo_demo()
    unittest.main(exit=False)
    print(solution([1, 3, 6, 4, 1, 2]))
