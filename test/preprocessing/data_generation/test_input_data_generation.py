import unittest
from copy import deepcopy

import numpy as np

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Stone
from src.beans.game_tree.game_node import GameNode
from src.beans.game_tree.game_tree import GameTree
from src.preprocessing.data_generation.preprocessing_data_generation import generate_preprocessing_data

BLACK_POSITIONS = [(2, 1), (2, 2), (2, 3), (1, 4), (1, 5), (4, 1)]
WHITE_POSITIONS = [(0, 3), (1, 0), (1, 1), (1, 2), (1, 3)]


def _create_game_tree() -> GameTree:
    black_stones = [Stone(pos, Color.BLACK) for pos in BLACK_POSITIONS]

    white_stones = [Stone(pos, Color.WHITE) for pos in WHITE_POSITIONS]

    initial_board = Board(black_stones + white_stones)
    root = GameNode(None, initial_board, None)

    correct_move = Stone((0, 1), Color.BLACK)
    correct_board = deepcopy(initial_board)
    correct_board.place_stone(correct_move)
    GameNode(root, correct_board, correct_move, "Correct")

    wrong_move = Stone((3, 2), Color.BLACK)
    wrong_board1 = deepcopy(initial_board)
    wrong_board1.place_stone(wrong_move)
    wrong_node1 = GameNode(root, wrong_board1, wrong_move)

    white_move = Stone((0, 1), Color.WHITE)
    wrong_board2 = deepcopy(wrong_board1)
    wrong_board2.place_stone(white_move)
    GameNode(wrong_node1, wrong_board2, white_move, "Wrong")

    return GameTree(root)


class TestInputDataGeneration(unittest.TestCase):

    def test_data_generation(self):
        black_data, white_data = generate_preprocessing_data(_create_game_tree())

        self.assertEqual(black_data.shape, (2, 19 ** 2 + 2))
        self.assertEqual(white_data.shape, (1, 19 ** 2 + 1))

        black_board1 = black_data[0][:(19 ** 2)].reshape(19, 19)
        self.assertEqual(len(black_board1[black_board1 == 1]), 6)
        self.assertEqual(len(black_board1[black_board1 == -1]), 5)
        for pos in BLACK_POSITIONS:
            self.assertEqual(black_board1[pos], 1)
        for pos in WHITE_POSITIONS:
            self.assertEqual(black_board1[pos], -1)

        black_move1 = black_data[0][-2]
        self.assertEqual(black_move1, 1)

        black_path_type1 = black_data[0][-1]
        self.assertEqual(black_path_type1, 1)

        black_board2 = black_data[1][:(19 ** 2)].reshape(19, 19)
        self.assertTrue(np.all(np.equal(black_board1, black_board2)))

        black_move2 = black_data[1][-2]
        self.assertEqual(black_move2, 59)

        black_path_type2 = black_data[1][-1]
        self.assertEqual(black_path_type2, 0)

        white_board = white_data[0][:(19 ** 2)].reshape(19, 19)
        self.assertEqual(len(white_board[white_board == 1]), 7)
        self.assertEqual(len(white_board[white_board == -1]), 5)

        for pos in BLACK_POSITIONS + [(3, 2)]:
            self.assertEqual(white_board[pos], 1)
        for pos in WHITE_POSITIONS:
            self.assertEqual(white_board[pos], -1)

        white_move = white_data[0][-1]
        self.assertEqual(white_move, 1)
