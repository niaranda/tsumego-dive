import unittest
from typing import Optional

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Stone
from src.beans.game_tree.game_node import GameNode
from src.beans.game_tree.game_tree import GameTree


def _create_game_node(parent: Optional[GameNode], board: Board) -> GameNode:
    return GameNode(parent, board, None, "")


class TestGameTree(unittest.TestCase):

    def test_get_leaves(self):
        stone0 = Stone((0, 0), Color.BLACK)
        stone1 = Stone((0, 1), Color.BLACK)
        stone2 = Stone((0, 2), Color.WHITE)

        root = _create_game_node(None, Board())
        leaf1 = _create_game_node(root, Board([stone0]))
        branch2 = _create_game_node(root, Board([stone1]))
        leaf2 = _create_game_node(branch2, Board([stone1, stone2]))

        game_tree = GameTree(root)

        self.assertEqual(len(game_tree.get_leaves()), 2)
        self.assertIn(leaf1, game_tree.get_leaves())
        self.assertIn(leaf2, game_tree.get_leaves())

    def test_get_nodes(self):
        stones = [Stone((0, pos), Color.BLACK) for pos in range(9)]
        boards = [Board([stone]) for stone in stones]

        root = _create_game_node(None, boards[0])
        node1 = _create_game_node(root, boards[1])
        node2 = _create_game_node(root, boards[2])
        node3 = _create_game_node(root, boards[3])
        node4 = _create_game_node(node1, boards[4])
        _create_game_node(node1, boards[5])
        _create_game_node(node3, boards[6])
        _create_game_node(node2, boards[7])
        _create_game_node(node4, boards[8])

        game_tree = GameTree(root)

        self.assertEqual(len(game_tree.get_nodes()), 9)
