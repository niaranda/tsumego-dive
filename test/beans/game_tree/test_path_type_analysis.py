import unittest
from typing import Optional

from src.beans.board.board import Board
from src.beans.game_tree.game_node import GameNode
from src.beans.game_tree.game_tree import GameTree


def _create_game_tree(leaf1_comment: Optional[str], leaf2_comment: Optional[str]) -> GameTree:
    root = GameNode(None, Board(), None)
    branch1 = GameNode(root, Board(), None)
    branch2 = GameNode(root, Board(), None)

    GameNode(branch1, Board(), None, [leaf1_comment])
    GameNode(branch2, Board(), None, [leaf2_comment])

    return GameTree(root)


class TestPathTypeAnalysis(unittest.TestCase):

    def test_dual_path_analysis(self):
        with self.assertRaises(Exception):
            _create_game_tree("Correct wrong", "Incorrect success")

        with self.assertRaises(Exception):
            _create_game_tree("正解 incorrect", "failure")

        dual_none = _create_game_tree("success 失败", None)
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
