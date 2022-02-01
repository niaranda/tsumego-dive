import unittest

from src.beans.board.board_point import BoardPoint
from src.beans.board.stone import Stone, Color


class TestBoardPoint(unittest.TestCase):

    def test_is_empty(self):
        point: BoardPoint = BoardPoint((2, 1))
        self.assertTrue(point.is_empty())

        point.stone = Stone(Color.BLACK, (2, 1))
        self.assertFalse(point.is_empty())

    def test_remove_stone(self):
        point: BoardPoint = BoardPoint((2, 1))
        point.stone = Stone(Color.BLACK, (2, 1))
        point.remove_stone()
        self.assertTrue(point.is_empty())

    def test_replace_stone(self):
        point: BoardPoint = BoardPoint((2, 1))
        point.stone = Stone(Color.BLACK, (2, 1))
        point.remove_stone()

        point.stone = Stone(Color.WHITE, (2, 1))
        self.assertEqual(point.stone.color, Color.WHITE)

    def test_wrong_stone_position_placing(self):
        point: BoardPoint = BoardPoint((2, 1))

        with self.assertRaises(Exception):
            point.stone = Stone(Color.BLACK, (3, 1))

    def test_wrong_placing_second_stone(self):
        point: BoardPoint = BoardPoint((2, 1))
        point.stone = Stone(Color.BLACK, (2, 1))

        with self.assertRaises(Exception):
            point.stone = Stone(Color.BLACK, (2, 1))
