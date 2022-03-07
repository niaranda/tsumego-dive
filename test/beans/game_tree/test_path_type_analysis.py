import unittest

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Stone
from src.beans.game_tree.game_node import GameNode
from src.beans.game_tree.game_tree import GameTree


def _create_game_tree(leaf1_comment: str, leaf2_comment: str) -> GameTree:
    stones = [Stone((0, pos), Color.BLACK) for pos in range(4)]
    boards = [Board([stone]) for stone in stones]

    root = GameNode(None, Board(), None)
    branch1 = GameNode(root, boards[0], None)
    branch2 = GameNode(root, boards[1], None)

    GameNode(branch1, boards[2], None, leaf1_comment)
    GameNode(branch2, boards[3], None, leaf2_comment)

    return GameTree(root)


class TestPathTypeAnalysis(unittest.TestCase):

    def test_dual_path_analysis(self):
        with self.assertRaises(Exception):
            _create_game_tree("Correct wrong", "Incorrect success")

        with self.assertRaises(Exception):
            _create_game_tree("正解 incorrect", "failure")

        dual_none = _create_game_tree("success 失败", "")
        self.assertTrue(dual_none.root.is_correct())
        self.assertTrue(dual_none.root.children[1].is_correct())
        self.assertFalse(dual_none.root.children[0].is_valid())

    def test_wrong_path_analysis(self):
        with self.assertRaises(Exception):
            _create_game_tree("WRONG", "shi bai")

        wrong_correct = _create_game_tree("FAILure", "correct")
        self.assertTrue(wrong_correct.root.is_correct())
        self.assertFalse(wrong_correct.root.children[0].is_correct())
        self.assertTrue(wrong_correct.root.children[1].is_correct())
