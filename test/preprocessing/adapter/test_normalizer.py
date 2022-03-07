import unittest
from typing import List

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Stone
from src.beans.board.stone_group import StoneGroup
from src.preprocessing.adapter.normalizer import Normalizer


class TestNormalizer(unittest.TestCase):

    def test_normalize_color_change(self):
        stones = [Stone((0, 3), Color.BLACK), Stone((1, 2), Color.WHITE), Stone((1, 3), Color.BLACK)]
        board = Board(stones)
        stone = Stone((4, 1), Color.WHITE)

        normalizer = Normalizer(board, stone)

        normalizer.normalize_board(board)
        self.assertEqual(board.placed_stones[(0, 3)], Color.WHITE)

        self.assertEqual(normalizer.normalize_stone(stone), Stone((4, 1), Color.BLACK))

        white_groups: List[StoneGroup] = list(filter(lambda group: group.color == Color.WHITE, board.stone_groups))
        self.assertEqual(len(white_groups), 1)
        self.assertEqual(len(white_groups[0].positions), 2)
        self.assertTrue((0, 3) in white_groups[0].positions)

    def test_normalize_board_rotation(self):
        stones = [Stone((18, 15), Color.BLACK), Stone((17, 15), Color.WHITE), Stone((17, 16), Color.WHITE)]
        board = Board(stones)
        stone = Stone((14, 17), Color.BLACK)

        normalizer = Normalizer(board, stone)

        normalizer.normalize_board(board)
        self.assertFalse((18, 15) in board.placed_stones)
        self.assertFalse((18, 15) in board.stone_liberties)

        group_positions = [pos for group in board.stone_groups for pos in group.positions]
        self.assertFalse((18, 15) in group_positions)
        self.assertTrue((0, 3) in group_positions)

        self.assertEqual(board.placed_stones[(0, 3)], Color.BLACK)
        self.assertEqual(board.placed_stones[(1, 3)], Color.WHITE)
        self.assertEqual(board.placed_stones[(1, 2)], Color.WHITE)

        self.assertTrue(board.stone_liberties[(1, 3)], 2)

        self.assertEqual(normalizer.normalize_stone(stone), Stone((4, 1), Color.BLACK))

    def test_normalize_reflection(self):
        stones = [Stone((3, 0), Color.BLACK), Stone((2, 1), Color.WHITE), Stone((3, 1), Color.WHITE)]
        board = Board(stones)
        stone = Stone((1, 4), Color.BLACK)

        normalizer = Normalizer(board, stone)

        normalizer.normalize_board(board)
        self.assertFalse((3, 0) in board.placed_stones)
        self.assertTrue((0, 3) in board.placed_stones)

        self.assertFalse((2, 1) in board.stone_liberties)
        self.assertTrue((1, 2) in board.stone_liberties)

        group_positions = [pos for group in board.stone_groups for pos in group.positions]
        self.assertFalse((3, 1) in group_positions)
        self.assertTrue((1, 3) in group_positions)
