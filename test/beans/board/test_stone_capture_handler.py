import unittest

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Stone


class TestStoneCaptureHandler(unittest.TestCase):

    def test_group_capture(self):
        positions = [(0, 0), (0, 4), (0, 5)]
        stones = [Stone(pos, Color.WHITE) for pos in positions]

        board = Board(stones)
        black_pos1 = [(0, 1), (1, 0)]
        board.place_stones([Stone(pos, Color.BLACK) for pos in black_pos1])
        self.assertFalse((0, 0) in board.placed_stones)

        black_pos2 = [(0, 3), (1, 4), (1, 5)]
        board.place_stones([Stone(pos, Color.BLACK) for pos in black_pos2])
        self.assertTrue((0, 4) in board.placed_stones)

        board.place_stone(Stone((0, 6), Color.BLACK))
        self.assertFalse((0, 4) in board.placed_stones)
