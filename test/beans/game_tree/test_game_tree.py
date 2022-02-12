import unittest
from typing import Optional

from src.beans.board.board import Board
from src.beans.game_tree.game_node import GameNode
from src.beans.game_tree.game_tree import GameTree


def _create_game_node(parent: Optional[GameNode]) -> GameNode:
    return GameNode(parent, Board(), None, None)


class TestGameTree(unittest.TestCase):

    def test_get_leaves(self):
        root = _create_game_node(None)
        leaf1 = _create_game_node(root)
        branch2 = _create_game_node(root)
        leaf2 = _create_game_node(branch2)

        game_tree = GameTree(root)

        self.assertEqual(len(game_tree.get_leaves()), 2)
        self.assertIn(leaf1, game_tree.get_leaves())
        self.assertIn(leaf2, game_tree.get_leaves())

    def test_get_nodes(self):
        root = _create_game_node(None)
        node1 = _create_game_node(root)
        node2 = _create_game_node(root)
        node3 = _create_game_node(root)
        node4 = _create_game_node(node1)
        _create_game_node(node1)
        _create_game_node(node3)
        _create_game_node(node2)
        _create_game_node(node4)

        game_tree = GameTree(root)

        self.assertEqual(len(game_tree.get_nodes()), 9)
