
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
import math
import unittest

from problem.eda.stores_and_cust.sd_space import SdSpace


class SdSpaceTest(unittest.TestCase):

    @staticmethod
    def euclidean_distance(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    @staticmethod
    def coords(p):
        return p.x, p.y

    def setUp(self):
        self.san_diego = SdSpace(32.715, -117.163)

    def test_sd_space(self):
        san_diego = self.san_diego
        self.assertAlmostEqual(32.715, san_diego.lat(), places=4)
        self.assertAlmostEqual(-117.163, san_diego.lng(), places=4)

        self.assertEqual(726_074, san_diego.x)
        self.assertEqual(631_400, san_diego.y)

    def test_distance(self):
        miami = SdSpace(25.775, -80.209)
        self.assertEqual(4_149_754, miami.x)
        self.assertEqual(128_598, miami.y)

        self.assertEqual(3_654_467, int(self.san_diego.distance(miami)))

        phoenix = SdSpace(33.450, -112.067)
        self.assertEqual(1_198_204, phoenix.x)
        self.assertEqual(684_650, phoenix.y)

        self.assertEqual(482_673, int(self.san_diego.distance(phoenix)))
        self.assertEqual(472_130, phoenix.x - self.san_diego.x)

        seattle = SdSpace(47.610, -122.333)
        self.assertEqual(247_089, seattle.x)
        self.assertEqual(1_710_539, seattle.y)

        self.assertEqual(1_710_539, int(self.san_diego.distance(seattle)))
        self.assertEqual(1_079_139, seattle.y - self.san_diego.y)

        augusta = SdSpace(44.310, -69.780)
        self.assertEqual(5_115_970, augusta.x)
        self.assertEqual(1_471_455, augusta.y)

        self.assertEqual(4_263_237, int(self.san_diego.distance(augusta)))
        self.assertEqual(4_469_550, int(self.euclidean_distance(
            self.coords(self.san_diego),
            self.coords(augusta))))

    def test_euclidean_distance(self):
        self.assertEqual(5, self.euclidean_distance((0, 3), (4, 0)))
        self.assertEqual(13, self.euclidean_distance((0, 5), (12, 0)))
