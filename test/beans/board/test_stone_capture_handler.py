import unittest

from src.beans.board.board import Board
from src.beans.board.stone import Stone, Color


class TestStoneCaptureHandler(unittest.TestCase):

    def test_group_capture(self):
        positions = [(0, 0), (0, 4), (0, 5)]
        stones = [Stone(Color.WHITE, pos) for pos in positions]

        board = Board(stones)
        black_pos1 = [(0, 1), (1, 0)]
        board.place_stones([Stone(Color.BLACK, pos) for pos in black_pos1])
        self.assertTrue(board.grid[(0, 0)].is_empty())

        black_pos2 = [(0, 3), (1, 4), (1, 5)]
        board.place_stones([Stone(Color.BLACK, pos) for pos in black_pos2])
        self.assertFalse(board.grid[(0, 4)].is_empty())

        board.place_stone(Stone(Color.BLACK, (0, 6)))
        self.assertTrue(board.grid[(0, 4)].is_empty())
