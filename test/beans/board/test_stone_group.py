import unittest

from src.beans.board.color import Color
from src.beans.board.stone_group import StoneGroup


class TestStoneGroup(unittest.TestCase):

    def test_create_invalid_group(self):
        # empty group
        with self.assertRaises(Exception):
            StoneGroup([], Color.BLACK)
        # repeated stones
        with self.assertRaises(Exception):
            StoneGroup([(2, 1), (2, 1)], Color.WHITE)

    def test_add_position(self):
        group = StoneGroup([(2, 1)], Color.BLACK)
        group.add_position((3, 1))

        self.assertIn((3, 1), group.positions)

    def test_color(self):
        group = StoneGroup([(2, 1)], Color.WHITE)
        self.assertEqual(group.color, Color.WHITE)

    def test_is_attached(self):
        positions = [(3, 2), (3, 3), (4, 3)]
        group = StoneGroup(positions, Color.BLACK)

        self.assertTrue(group.is_attached((2, 2)))
        self.assertFalse(group.is_attached((4, 5)))
        self.assertFalse(group.is_attached((5, 4)))
