import unittest

from src.beans.board.stone import Stone, Color


class TestStone(unittest.TestCase):

    def test_color_get_other(self):
        self.assertEqual(Color.WHITE, Color.BLACK.get_other())
        self.assertEqual(Color.BLACK, Color.WHITE.get_other())

    def test_invalid_position(self):
        with self.assertRaises(Exception):
            Stone(Color.BLACK, (-1, 8))
        with self.assertRaises(Exception):
            Stone(Color.BLACK, (4, 19))
        with self.assertRaises(Exception):
            Stone(Color.WHITE, (19, 8))
        with self.assertRaises(Exception):
            Stone(Color.WHITE, (2, -1))

    def test_invalid_liberties_access(self):
        stone = Stone(Color.BLACK, (2, 1))
        with self.assertRaises(Exception):
            stone.has_liberties()

    def test_is_neighbor(self):
        stone = Stone(Color.BLACK, (2, 1))
        stone1 = Stone(Color.BLACK, (1, 1))
        stone2 = Stone(Color.BLACK, (3, 2))

        self.assertTrue(stone.is_neighbor(stone1))
        self.assertFalse(stone.is_neighbor(stone2))

    def test_get_neighbor_positions(self):
        corner1 = Stone(Color.BLACK, (0, 0))
        corner2 = Stone(Color.BLACK, (18, 0))

        side1 = Stone(Color.BLACK, (0, 4))
        side2 = Stone(Color.BLACK, (6, 18))

        normal = Stone(Color.BLACK, (5, 4))

        self.assertEqual(len(corner1.get_neighbor_positions()), 2)
        self.assertEqual(len(corner2.get_neighbor_positions()), 2)
        self.assertEqual(len(side1.get_neighbor_positions()), 3)
        self.assertEqual(len(side2.get_neighbor_positions()), 3)
        self.assertEqual(len(normal.get_neighbor_positions()), 4)

        self.assertIn((17, 0), corner2.get_neighbor_positions())
        self.assertIn((18, 1), corner2.get_neighbor_positions())

    def test_has_liberties(self):
        stone = Stone(Color.BLACK, (2, 1))
        stone.liberties = 4
        self.assertTrue(stone.has_liberties())

        stone.liberties = 0
        self.assertFalse(stone.has_liberties())
