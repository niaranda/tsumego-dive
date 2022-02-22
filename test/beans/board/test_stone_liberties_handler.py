import unittest
from typing import Tuple

from src.beans.board.board import Board
from src.beans.board.color import  Color

Pos = Tuple[int, int]
Stone = Tuple[Pos, Color]


class TestStoneLibertiesHandler(unittest.TestCase):

    def test_liberties_update(self):
        positions = [(0, 0), (0, 5), (10, 10)]
        stones = [(pos, Color.BLACK) for pos in positions]
        board = Board(stones)

        self.assertEqual(board.stone_liberties[positions[0]], 2)
        self.assertEqual(board.stone_liberties[positions[1]], 3)
        self.assertEqual(board.stone_liberties[positions[2]], 4)

        board.place_stone(((0, 1), Color.BLACK))
        self.assertEqual(board.stone_liberties[positions[0]], 1)

        board.place_stone(((0, 6), Color.WHITE))
        self.assertEqual(board.stone_liberties[positions[1]], 2)
