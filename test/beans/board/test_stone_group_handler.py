import unittest
from typing import Tuple, List

from src.beans.board.board import Board
from src.beans.board.stone import Stone, Color
from src.beans.board.stone_group import StoneGroup

Pos = Tuple[int, int]


class TestStoneGroupHandler(unittest.TestCase):

    def test_groups_creation(self):
        black_pos = [(1, 2), (2, 5), (2, 6)]  # 2 black groups
        white_pos = [(1, 1), (0, 1), (1, 3), (8, 3), (8, 4), (9, 3), (9, 2)]  # 3 white groups

        black_stones: List[Stone] = [Stone(Color.BLACK, pos) for pos in black_pos]
        white_stones: List[Stone] = [Stone(Color.WHITE, pos) for pos in white_pos]

        board = Board(black_stones + white_stones)

        self.assertEqual(len(board.stone_groups), 5)
        black_groups: List[StoneGroup] = list(
            filter(lambda group: group.get_color() == Color.BLACK, board.stone_groups)
        )
        white_groups: List[StoneGroup] = list(
            filter(lambda group: group.get_color() == Color.WHITE, board.stone_groups)
        )

        self.assertEqual(len(black_groups), 2)
        self.assertEqual(len(white_groups), 3)

    def test_group_fusion(self):
        board = Board()
        board.place_stone(Stone(Color.BLACK, (0, 0)))
        board.place_stone(Stone(Color.BLACK, (0, 2)))
        board.place_stone(Stone(Color.BLACK, (1, 1)))

        self.assertEqual(len(board.stone_groups), 3)

        board.place_stone(Stone(Color.BLACK, (0, 1)))
        self.assertEqual(len(board.stone_groups), 1)
