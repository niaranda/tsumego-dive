from copy import deepcopy
from typing import List

import sgf

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Pos, Stone
from src.beans.game_tree.game_node import GameNode
from src.beans.game_tree.game_tree import GameTree
from src.preprocessing.preprocessing_exception import PreprocessingException


def parse_sgf_tree(problem: sgf.GameTree) -> GameTree:
    """Converts an sgf game tree to a game tree for this project"""
    # Initialize first board state
    init_stones: List[Stone] = __get_init_stones(problem)

    init_board: Board = Board(init_stones)
    root = GameNode(None, init_board, None)

    # recursively add all branches
    first_color: Color = __get_first_color(problem)
    last_game_node = __add_branch_nodes(problem.nodes[1:], root, first_color)  # first node is root
    next_color = last_game_node.stone_color.get_other() if last_game_node.stone else first_color
    if problem.children:
        __add_branches(problem.children, last_game_node, next_color)

    return GameTree(root)


def __get_init_stones(problem: sgf.GameTree) -> List[Stone]:
    """Gets sgf game tree initial stones"""
    properties: dict = problem.root.properties

    black_stones: List[Stone] = __parse_init_stones(properties, Color.BLACK)
    white_stones: List[Stone] = __parse_init_stones(properties, Color.WHITE)

    return black_stones + white_stones


def __parse_init_stones(properties: dict, color: Color) -> List[Stone]:
    property_name: str = "AB" if color == Color.BLACK else "AW"
    stones_pos: List[Pos] = __parse_positions(properties.get(property_name))
    return [(pos, color) for pos in stones_pos]


def __parse_positions(str_positions: List[str]) -> List[Pos]:
    return [__parse_position(str_pos) for str_pos in str_positions]


def __parse_stone(properties: dict, color: Color) -> Stone:
    property_name: str = "B" if color == Color.BLACK else "W"

    if property_name not in properties.keys():
        raise PreprocessingException(f"Not found expected {color} stone property while parsing sgf tree")

    # Get position from properties
    pos: Pos = __parse_position(properties.get(property_name)[0])
    return pos, color


def __parse_position(str_position: str) -> Pos:
    col, row = str_position
    return ord(col) - ord("a"), ord(row) - ord("a")


def __get_first_color(problem: sgf.GameTree) -> Color:
    if problem.children:
        keys: List[str] = list(problem.children[0].root.properties.keys())
    else:
        keys: List[str] = list(problem.root.next.properties.keys())
    if "B" in keys and "W" in keys:
        raise PreprocessingException("Found stones for both colors while parsing sgf tree root")
    if "B" not in keys and "W" not in keys:
        raise PreprocessingException("Found no stone while parsing sgf tree root")
    return Color.BLACK if "B" in keys else Color.WHITE


def __add_branches(branches: List[sgf.GameTree], game_node: GameNode, color: Color):
    """Recursively adds all branches"""
    for branch in branches:
        last_game_node = __add_branch_nodes(branch.nodes, game_node, color)
        next_color = last_game_node.stone_color.get_other()
        __add_branches(branch.children, last_game_node, next_color)


def __add_branch_nodes(nodes: List[sgf.Node], game_node: GameNode, color: Color):
    last_game_node = game_node
    next_color = color
    for node in nodes:
        last_game_node = __create_game_node(node.properties, last_game_node, next_color)
        next_color = next_color.get_other()
    return last_game_node


def __create_game_node(properties: dict, game_node: GameNode, color: Color) -> GameNode:
    """Creates a new game node with given parent node by adding a new stone of given color to the board"""
    new_stone: Stone = __parse_stone(properties, color)
    new_board: Board = deepcopy(game_node.board)  # Copy current board

    comment: str = properties.get("C")  # Can be None

    # Place the new stone and create a new game node
    new_board.place_stones([new_stone])
    new_game_node = GameNode(game_node, new_board, new_stone, comment)

    return new_game_node
