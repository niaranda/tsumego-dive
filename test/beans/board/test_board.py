import unittest
from typing import Dict

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Stone, Pos


class TestBoard(unittest.TestCase):

    def test_get_placed_stone_positions(self):
        stones = [Stone((1, 3), Color.BLACK), Stone((2, 5), Color.WHITE)]
        board: Board = Board(stones)
        positions = [(1, 3), (2, 5)]
        self.assertEqual(positions, list(board.placed_stones.keys()))

    def test_place_stones(self):
        board: Board = Board()
        stones = [Stone((1, 3), Color.BLACK), Stone((2, 5), Color.WHITE)]
        board.place_stones(stones)

        stone_dict: Dict[Pos, Color] = {(1, 3): Color.BLACK, (2, 5): Color.WHITE}

        self.assertEqual(stone_dict, board.placed_stones)

    def test_suicide_rule(self):
        positions = [(0, 1), (1, 0)]
        board: Board = Board([Stone(pos, Color.BLACK) for pos in positions])
        with self.assertRaises(Exception):
            board.place_stone(Stone((0, 0), Color.WHITE))
