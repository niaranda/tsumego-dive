import unittest

from src.beans.board.stone import Stone, Color
from src.beans.board.stone_group import StoneGroup


class TestStoneGroup(unittest.TestCase):

    def test_create_invalid_group(self):
        # empty group
        with self.assertRaises(Exception):
            StoneGroup([])
        # repeated stones
        with self.assertRaises(Exception):
            StoneGroup([Stone(Color.BLACK, (2, 1)), Stone(Color.BLACK, (2, 1))])
        # stones of different colors
        with self.assertRaises(Exception):
            StoneGroup([Stone(Color.BLACK, (2, 1)), Stone(Color.WHITE, (3, 2))])

    def test_add_stone(self):
        group = StoneGroup([Stone(Color.BLACK, (2, 1))])
        added_stone = Stone(Color.BLACK, (3, 2))
        group.add_stone(added_stone)

        self.assertIn(added_stone, group.stones)

    def test_add_wrong_stone(self):
        group = StoneGroup([Stone(Color.BLACK, (2, 1))])

        with self.assertRaises(Exception):
            group.add_stone(Stone(Color.WHITE, (3, 2)))
        with self.assertRaises(Exception):
            group.add_stone(Stone(Color.BLACK, (2, 1)))

    def test_get_color(self):
        group = StoneGroup([Stone(Color.WHITE, (2, 1))])
        self.assertEqual(group.get_color(), Color.WHITE)

    def test_get_positions(self):
        positions = [(3, 2), (3, 3), (4, 3)]
        stones = [Stone(Color.BLACK, pos) for pos in positions]
        group = StoneGroup(stones)

        self.assertEqual(len(group.get_positions()), len(positions))

        group.add_stone(Stone(Color.BLACK, (3, 4)))
        self.assertEqual(len(group.get_positions()), len(positions) + 1)

    def test_is_attached(self):
        positions = [(3, 2), (3, 3), (4, 3)]
        stones = [Stone(Color.BLACK, pos) for pos in positions]
        group = StoneGroup(stones)

        self.assertTrue(group.is_attached(Stone(Color.WHITE, (2, 2))))
        self.assertFalse(group.is_attached(Stone(Color.BLACK, (4, 5))))
        self.assertFalse(group.is_attached(Stone(Color.BLACK, (5, 4))))

    def test_has_liberties(self):
        positions = [(3, 2), (3, 3)]
        stones = [Stone(Color.BLACK, pos) for pos in positions]
        for stone in stones:
            stone.liberties = 3
        group = StoneGroup(stones)

        self.assertTrue(group.has_liberties())

        for stone in stones:
            stone.liberties = 0
        self.assertFalse(group.has_liberties())
