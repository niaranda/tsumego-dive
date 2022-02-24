from copy import deepcopy
from typing import List, Dict

import sgf

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Pos, Stone
from src.beans.game_tree.game_node import GameNode
from src.beans.game_tree.game_tree import GameTree
from src.preprocessing.preprocessing_exception import PreprocessingException


def _parse_position(str_position: str) -> Pos:
    col, row = str_position
    return ord(col) - ord("a"), ord(row) - ord("a")


def _parse_stone(properties: dict, color: Color) -> Stone:
    property_name: str = "B" if color == Color.BLACK else "W"

    if property_name not in properties.keys():
        raise PreprocessingException(f"Not found expected {color} stone property while parsing sgf tree")

    # Get position from properties
    pos: Pos = _parse_position(properties.get(property_name)[0])
    return pos, color


def _get_first_stone(problem: sgf.GameTree) -> Stone:
    properties: Dict[str, str]
    if problem.children:
        properties = problem.children[0].root.properties
    else:
        properties = problem.root.next.properties

    keys = properties.keys()

    if "B" in keys and "W" in keys:
        raise PreprocessingException("Found stones for both colors while parsing sgf tree root")
    if "B" not in keys and "W" not in keys:
        raise PreprocessingException("Found no stone while parsing sgf tree root")

    if "B" in keys:
        return _parse_stone(properties, Color.BLACK)
    return _parse_stone(properties, Color.WHITE)


def _parse_positions(str_positions: List[str]) -> List[Pos]:
    return [_parse_position(str_pos) for str_pos in str_positions]


def _parse_init_stones(properties: dict, color: Color) -> List[Stone]:
    property_name: str = "AB" if color == Color.BLACK else "AW"
    stones_pos: List[Pos] = _parse_positions(properties.get(property_name))
    return [(pos, color) for pos in stones_pos]


def _get_init_stones(problem: sgf.GameTree) -> List[Stone]:
    """Gets sgf game tree initial stones"""
    properties: dict = problem.root.properties

    black_stones: List[Stone] = _parse_init_stones(properties, Color.BLACK)
    white_stones: List[Stone] = _parse_init_stones(properties, Color.WHITE)

    return black_stones + white_stones


class SgfTreeParser:

    def __init__(self, problem: sgf.GameTree):
        self.__problem = problem

        init_stones: List[Stone] = _get_init_stones(problem)

        init_board: Board = Board(init_stones)
        first_stone: Stone = _get_first_stone(problem)

        self.__root = GameNode(None, init_board, None)
        self.__first_color: Color = first_stone[1]

    def parse_tree(self) -> GameTree:
        """Converts an sgf game tree to a game tree for this project"""
        if self.__problem.nodes[1:]:
            last_game_node = self.__add_branch_nodes(self.__problem.nodes[1:], self.__root,
                                                     self.__first_color)  # first node is root
            next_color = last_game_node.stone_color.get_other()
        else:
            last_game_node = self.__root
            next_color = self.__first_color
        if self.__problem.children:
            self.__add_branches(self.__problem.children, last_game_node, next_color)

        return GameTree(self.__root)

    def __add_branches(self, branches: List[sgf.GameTree], game_node: GameNode, color: Color):
        """Recursively adds all branches"""
        for branch in branches:
            if branch.nodes:
                last_game_node = self.__add_branch_nodes(branch.nodes, game_node, color)
                next_color = last_game_node.stone_color.get_other()
            else:
                last_game_node = game_node
                next_color = color
            if branch.children:
                self.__add_branches(branch.children, last_game_node, next_color)

    def __add_branch_nodes(self, nodes: List[sgf.Node], game_node: GameNode, color: Color):
        last_game_node = game_node
        next_color = color
        for node in nodes:
            last_game_node = self.__create_game_node(node.properties, last_game_node, next_color)
            next_color = next_color.get_other()
        return last_game_node

    def __create_game_node(self, properties: dict, game_node: GameNode, color: Color) -> GameNode:
        """Creates a new game node with given parent node by adding a new stone of given color to the board"""
        new_stone: Stone = _parse_stone(properties, color)

        new_board: Board = deepcopy(game_node.board)  # Copy current board

        # Place the new stone and create a new game node
        new_board.place_stone(new_stone)
        return GameNode(game_node, new_board, new_stone, properties.get("C"))
