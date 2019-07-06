#! /usr/bin/env python

# Copyright 2019 John Hanley.
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

import unittest

from numeric.sqrt import sqrt_newton_raphson as sqrt


class SqrtTest(unittest.TestCase):

    def test_big_sqrt(self):
        self.assertAlmostEqual(3, sqrt(9), 4)
        self.assertAlmostEqual(3.1464, sqrt(9.9), 4)

    def test_small_sqrt(self):
        self.assertAlmostEqual(.5, sqrt(.25), 4)
        self.assertAlmostEqual(.7071, sqrt(.5), 4)
        self.assertAlmostEqual(.001, sqrt(0), 4)

    def test_not_i(self):
        with self.assertRaises(AssertionError) as _:
            sqrt(-1)


if __name__ == '__main__':
    unittest.main()
