import unittest

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Stone


class TestStoneLibertiesHandler(unittest.TestCase):

    def test_liberties_update(self):
        positions = [(0, 0), (0, 5), (10, 10)]
        stones = [Stone(pos, Color.BLACK) for pos in positions]
        board = Board(stones)

        self.assertEqual(board.stone_liberties[positions[0]], 2)
        self.assertEqual(board.stone_liberties[positions[1]], 3)
        self.assertEqual(board.stone_liberties[positions[2]], 4)

        board.place_stone(Stone((0, 1), Color.BLACK))
        self.assertEqual(board.stone_liberties[positions[0]], 1)

        board.place_stone(Stone((0, 6), Color.WHITE))
        self.assertEqual(board.stone_liberties[positions[1]], 2)
