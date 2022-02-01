import unittest
from typing import List

from src.beans.board.board import Board
from src.beans.board.stone import Stone, Color


class TestBoard(unittest.TestCase):

    def test_get_stones(self):
        stones: List[Stone] = [Stone(Color.BLACK, (1, 3)), Stone(Color.WHITE, (2, 5))]
        board: Board = Board(stones)
        self.assertEqual(stones, board.get_stones())

    def test_place_stones(self):
        board: Board = Board()
        stones: List[Stone] = [Stone(Color.BLACK, (1, 3)), Stone(Color.WHITE, (2, 5))]
        board.place_stones(stones)

        self.assertEqual(stones, board.get_stones())
