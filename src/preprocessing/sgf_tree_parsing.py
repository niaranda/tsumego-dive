import copy
from typing import List, Tuple

import sgf

from src.beans.board.board import Board
from src.beans.board.stone import Color, Stone
from src.beans.game_tree.game_node import GameNode
from src.beans.game_tree.game_tree import GameTree

Pos = Tuple[int, int]


def parse_sgf_tree(problem: sgf.GameTree) -> GameTree:
    """Converts an sgf game tree to a game tree for this project"""
    # Initialize first board state
    init_stones: List[Stone] = __get_init_stones(problem)

    init_board: Board = Board(init_stones)
    root = GameNode(None, init_board, None)

    # recursively add all branches
    first_color: Color = __get_first_color(problem)
    __add_branches(problem.children, root, first_color)

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
    return [Stone(color, pos) for pos in stones_pos]


def __parse_positions(str_positions: List[str]) -> List[Pos]:
    return [__parse_position(str_pos) for str_pos in str_positions]


def __parse_stone(properties: dict, color: Color) -> Stone:
    property_name: str = "B" if color == Color.BLACK else "W"

    if property_name not in properties.keys():
        raise Exception(f"Not found expected {color} stone property while parsing sgf tree")

    # Get position from properties
    pos: Pos = __parse_position(properties.get(property_name)[0])
    return Stone(color, pos)


def __parse_position(str_position: str) -> Pos:
    col, row = str_position
    return ord(col) - ord("a"), ord(row) - ord("a")


def __get_first_color(problem: sgf.GameTree) -> Color:
    keys: List[str] = list(problem.children[0].root.properties.keys())
    if "B" in keys and "W" in keys:
        raise Exception("Found stones for both colors while parsing sgf tree root")
    if "B" not in keys and "W" not in keys:
        raise Exception("Found no stone while parsing sgf tree root")
    return Color.BLACK if "B" in keys else Color.WHITE


def __add_branches(branches: List[sgf.GameTree], game_node: GameNode, color: Color):
    """Recursively adds all branches"""
    for branch in branches:
        new_game_node = game_node
        next_color = color
        for branch_node in branch.nodes:
            new_game_node = __create_game_node(branch_node.properties, new_game_node, next_color)
            next_color = next_color.get_other()

        __add_branches(branch.children, new_game_node, next_color)


def __create_game_node(properties: dict, game_node: GameNode, color: Color) -> GameNode:
    """Creates a new game node with given parent node by adding a new stone of given color to the board"""
    new_stone: Stone = __parse_stone(properties, color)
    new_board: Board = copy.deepcopy(game_node.board)  # Copy current board

    comment: str = properties.get("C")  # Can be None

    # Place the new stone and create a new game node
    new_board.place_stones([new_stone])
    new_game_node = GameNode(game_node, new_board, new_stone, comment)

    game_node.add_child(new_game_node)
    return new_game_node
