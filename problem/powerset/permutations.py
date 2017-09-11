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


import collections
import functools
import unittest


class PermutationsTest(unittest.TestCase):

    # python3 /usr/bin/nosetests --with-doctest permutations.py

    def test_size(self):
        word = 'abcdefghij'
        word = 'abcdef'
        for i in range(1, len(word)):
            self.assertEqual(factorial(i), len(list(permutations(word[:i]))))
            self.assertEqual(2 ** i, len(powerset(word[:i])))

    def test_kth_permutation(self, word='01234567', verbose=False):
        s = set()
        uniques = factorial(len(word))
        for k in range(uniques):
            perm = ' '.join(kth_permutation(k, word))
            s.add(perm)
            if verbose:
                print('%3d: ' % k, perm)
        self.assertEqual(uniques, len(s))  # Verify there were no dups.


@functools.lru_cache()
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def factorial_iterative(n):
    acc = 1
    for i in range(2, n + 1):
        acc *= i
    return acc


def all_but(i, word):
    '''
    Return all but the i-th character.
    >>> all_but(0, 'abc')
    'bc'
    >>> all_but(1, 'abc')
    'ac'
    >>> all_but(2, 'abc')
    'ab'
    >>> all_but(9, 'abc')
    'abc'
    '''
    return word[:i] + word[i+1:]


def kth_permutation(k, word):
    for i in kth_permutation_indexes(k, len(word)):
        yield word[i]


def kth_permutation_indexes(k, n):

    place_values = [factorial(i) for i in range(n - 1, 0, -1)]
    indexes = collections.deque(range(n))

    ret = []
    for val in place_values:
        j = int(k / val)
        k -= j * val
        ret.append(indexes[j])
        del indexes[j]
    return tuple(ret + list(indexes))


def permutations(word):
    '''
    Naive generator, gives all permutations of word, in lexicographic order.
    >>> ' '.join(list(permutations('abc')))
    'abc acb bac bca cab cba'
    '''
    if len(word) == 1:
        yield word

    for i in range(len(word)):
        for perm in permutations(all_but(i, word)):
            yield word[i] + perm


def powerset(word):
    return sorted(set(_powerset(word)))


def _powerset(word):
    yield word

    for i in range(len(word)):
        yield from powerset(all_but(i, word))


def main(verbose=False):
    # null = '\u2205'  # symbol for empty set
    word = '3012'
    if verbose:
        print(' '.join(permutations(''.join(sorted(word)))))  # '0123'
        print('')
        print(', '.join(powerset(word)))  # This shows the '' member.


if __name__ == '__main__':
    main()
    unittest.main()
