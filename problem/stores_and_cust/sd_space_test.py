
import unittest

from problem.stores_and_cust.sd_space import SdSpace


class SdSpaceTest(unittest.TestCase):

    def setUp(self):
        self.san_diego = SdSpace(32.715, -117.163)

    def test_sd_space(self):
        san_diego = self.san_diego
        self.assertEqual(32.715, san_diego.lat())
        self.assertEqual(-117.163, san_diego.lng())

        self.assertAlmostEqual(7.837, san_diego.x)
        self.assertAlmostEqual(8.715, san_diego.y)

    def test_distance(self):
        miami = SdSpace(25.775, -80.209)
        self.assertAlmostEqual(44.791, miami.x)
        self.assertAlmostEqual(1.775, miami.y)

        self.assertEqual(4_164_722, int(self.san_diego.distance(miami)))

        phoenix = SdSpace(33.450, -112.067)
        self.assertAlmostEqual(12.933, phoenix.x)
        self.assertAlmostEqual(9.450, phoenix.y)

        self.assertEqual(566_077, int(self.san_diego.distance(phoenix)))

        seattle = SdSpace(47.610, -122.333)
        self.assertAlmostEqual(2.667, seattle.x)
        self.assertAlmostEqual(23.610, seattle.y)

        self.assertEqual(1_738_003, int(self.san_diego.distance(seattle)))

        augusta = SdSpace(44.310, -69.780)
        self.assertAlmostEqual(55.220, augusta.x)
        self.assertAlmostEqual(20.310, augusta.y)

        self.assertEqual(5_246_329, int(self.san_diego.distance(augusta)))
