
import unittest

from problem.pop_map.hexagon.hex_terrain import Direction


class TestHexTerrain(unittest.TestCase):

    def test_tautology(self):
        direction = Direction.NORTH
        dirs = list(Direction)
        self.assertEqual(direction, dirs[dirs.index(direction)])
