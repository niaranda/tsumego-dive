import unittest
from copy import copy
from typing import Optional

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.game_tree.game_node import GameNode, PathType


def _create_game_node(parent: Optional[GameNode], path_type: PathType = PathType.UNKNOWN) -> GameNode:
    node = GameNode(parent, Board(), None, None)
    node.path_type = path_type
    return node

class TestGameNode(unittest.TestCase):

    def test_children(self):
        root = _create_game_node(None)
        _create_game_node(root)
        _create_game_node(root)

        self.assertEqual(len(root.children), 2)

    def test_add_child(self):
        root = _create_game_node(None)
        node = _create_game_node(None)
        root.add_child(node)

        self.assertEqual(len(root.children), 1)
        self.assertFalse(root.is_leaf())

    def test_is_root(self):
        root = _create_game_node(None)
        leaf = _create_game_node(root)

        self.assertTrue(root.is_root())
        self.assertFalse(leaf.is_root())

    def test_is_leaf(self):
        root = _create_game_node(None)
        leaf = _create_game_node(root)

        self.assertTrue(leaf.is_leaf())
        self.assertFalse(root.is_leaf())

    def test_is_valid(self):
        root = _create_game_node(None, PathType.UNKNOWN)
        node1 = _create_game_node(root, PathType.DUAL)
        node2 = _create_game_node(root, PathType.CORRECT)
        node3 = _create_game_node(root, PathType.WRONG)

        self.assertFalse(root.is_valid())
        self.assertFalse(node1.is_valid())
        self.assertTrue(node2.is_valid())
        self.assertTrue(node3.is_valid())

    def test_is_correct(self):
        root = _create_game_node(None, PathType.UNKNOWN)
        node1 = _create_game_node(root, PathType.DUAL)
        node2 = _create_game_node(root, PathType.CORRECT)
        node3 = _create_game_node(root, PathType.WRONG)

        self.assertFalse(root.is_correct())
        self.assertFalse(node1.is_correct())
        self.assertTrue(node2.is_correct())
        self.assertFalse(node3.is_correct())

    def test_ko_rule(self):
        black_stones = [((0, 1), Color.BLACK), ((1, 0), Color.BLACK)]
        white_stones = [((0, 2), Color.WHITE), ((1, 1), Color.WHITE)]
        board1 = Board(black_stones + white_stones)
        root = GameNode(None, board1, None)

        board2 = copy(board1)
        stone = ((0, 0), Color.WHITE)
        board2.place_stone(stone)
        node = GameNode(root, board2, stone)

        board3 = copy(board2)
        illegal_stone = ((0, 1), Color.BLACK)
        board3.place_stone(illegal_stone)

        with self.assertRaises(Exception):
            GameNode(node, board3, illegal_stone)
