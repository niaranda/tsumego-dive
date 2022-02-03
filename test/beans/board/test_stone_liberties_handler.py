import unittest
from typing import Tuple

from src.beans.board.board import Board
from src.beans.board.stone import Stone, Color

Pos = Tuple[int, int]


class TestStoneLibertiesHandler(unittest.TestCase):

    def test_liberties_update(self):
        stones = [Stone(Color.BLACK, pos) for pos in [(0, 0), (0, 5), (10, 10)]]
        board = Board(stones)

        self.assertEqual(stones[0].liberties, 2)
        self.assertEqual(stones[1].liberties, 3)
        self.assertEqual(stones[2].liberties, 4)

        board.place_stone(Stone(Color.BLACK, (0, 1)))
        self.assertEqual(stones[0].liberties, 1)

        board.place_stone(Stone(Color.WHITE, (0, 6)))
        self.assertEqual(stones[1].liberties, 2)
