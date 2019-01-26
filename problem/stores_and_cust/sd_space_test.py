
import unittest

from problem.stores_and_cust.sd_space import SdSpace


class SdSpaceTest(unittest.TestCase):

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

        seattle = SdSpace(47.610, -122.333)
        self.assertEqual(247_089, seattle.x)
        self.assertEqual(1_710_539, seattle.y)

        self.assertEqual(1_710_539, int(self.san_diego.distance(seattle)))

        augusta = SdSpace(44.310, -69.780)
        self.assertEqual(5_115_970, augusta.x)
        self.assertEqual(1_471_455, augusta.y)

        self.assertEqual(4_263_237, int(self.san_diego.distance(augusta)))
