import unittest
from typing import List, Tuple, Dict

from src.beans.board.board import Board
from src.beans.board.color import Color

Pos = Tuple[int, int]
Stone = Tuple[Pos, Color]


class TestBoard(unittest.TestCase):

    def test_get_placed_stone_positions(self):
        stones: List[Stone] = [((1, 3), Color.BLACK), ((2, 5), Color.WHITE)]
        board: Board = Board(stones)
        positions = [(1, 3), (2, 5)]
        self.assertEqual(positions, board.get_placed_stone_positions())

    def test_place_stones(self):
        board: Board = Board()
        stones: List[Stone] = [((1, 3), Color.BLACK), ((2, 5), Color.WHITE)]
        board.place_stones(stones)

        stone_dict: Dict[Pos, Color] = {(1, 3): Color.BLACK, (2, 5): Color.WHITE}

        self.assertEqual(stone_dict, board.placed_stones)
