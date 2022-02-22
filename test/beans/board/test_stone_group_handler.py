import unittest
from typing import Tuple, List

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone_group import StoneGroup

Pos = Tuple[int, int]
Stone = Tuple[Pos, Color]


class TestStoneGroupHandler(unittest.TestCase):

    def test_groups_creation(self):
        black_pos = [(1, 2), (2, 5), (2, 6)]  # 2 black groups
        white_pos = [(1, 1), (0, 1), (1, 3), (8, 3), (8, 4), (9, 3), (9, 2)]  # 3 white groups

        black_stones: List[Stone] = [(pos, Color.BLACK) for pos in black_pos]
        white_stones: List[Stone] = [(pos, Color.WHITE) for pos in white_pos]

        board = Board(black_stones + white_stones)

        self.assertEqual(len(board.stone_groups), 5)
        black_groups: List[StoneGroup] = list(
            filter(lambda group: group.color == Color.BLACK, board.stone_groups)
        )
        white_groups: List[StoneGroup] = list(
            filter(lambda group: group.color == Color.WHITE, board.stone_groups)
        )

        self.assertEqual(len(black_groups), 2)
        self.assertEqual(len(white_groups), 3)

    def test_group_fusion(self):
        board = Board()
        board.place_stone(((0, 0), Color.BLACK))
        board.place_stone(((0, 2), Color.BLACK))
        board.place_stone(((1, 1), Color.BLACK))

        self.assertEqual(len(board.stone_groups), 3)

        board.place_stone(((0, 1), Color.BLACK))
        self.assertEqual(len(board.stone_groups), 1)
