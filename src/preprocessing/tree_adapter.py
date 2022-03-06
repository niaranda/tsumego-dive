from copy import deepcopy
from typing import List, Dict

import sgf

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Pos, Stone
from src.beans.game_tree.game_node import GameNode
from src.beans.game_tree.game_tree import GameTree
from src.beans.gameplay_exception import GamePlayException
from src.preprocessing.normalizer import Normalizer
from src.preprocessing.preprocessing_exception import PreprocessingException


def _parse_position(str_position: str) -> Pos:
    if not str_position:
        raise GamePlayException("Unallowed pass")
    if len(str_position) != 2:
        raise PreprocessingException(f"Wrong stone position format {str_position} in sgf")
    col, row = str_position
    return ord(col) - ord("a"), ord(row) - ord("a")


def _parse_stone(properties: dict, color: Color) -> Stone:
    property_name: str = "B" if color == Color.BLACK else "W"

    if property_name not in properties:
        raise PreprocessingException(f"Not found expected {color} stone property while parsing sgf tree")

    # Get position from properties
    pos: Pos = _parse_position(properties.get(property_name)[0].lower())

    if __is_valid_position(pos):
        return Stone(pos, color)

    row, col = pos
    if row == 25 and col == 25:
        raise GamePlayException("Unallowed pass")

    raise PreprocessingException(f"Wrong stone position {properties.get(property_name)[0]}")


def _correct_only_comment_tree_node(problem: sgf.GameTree):
    if len(problem.nodes) > 1:
        problem.root.nodes.pop(1)

    problem.children[0].nodes.pop(0)
    return


def _correct_only_comment_branch_node(branch: sgf.GameTree):
    branch.nodes.pop(0)


def _check_only_comment_branch_node(branch: sgf.GameTree) -> bool:
    if not branch.nodes:
        return False

    properties: Dict[str, str] = branch.nodes[0].properties
    if "B" in properties or "W" in properties:
        return False

    return "C" in properties or "N" in properties


def _get_first_node_properties(problem: sgf.GameTree) -> Dict[str, str]:
    if len(problem.nodes) > 1:
        return problem.nodes[1].properties
    return problem.children[0].root.properties


def _get_first_stone(problem: sgf.GameTree) -> Stone:
    properties: Dict[str, str] = _get_first_node_properties(problem)

    if "B" not in properties and "W" not in properties:
        if "C" in properties or "N" in properties:
            _correct_only_comment_tree_node(problem)
            properties = _get_first_node_properties(problem)
            if "B" not in properties and "W" not in properties:
                raise PreprocessingException("Found no stone while parsing sgf tree root")

    if "B" in properties and "W" in properties:
        raise PreprocessingException("Found stones for both colors while parsing sgf tree root")

    if "B" in properties:
        return _parse_stone(properties, Color.BLACK)
    return _parse_stone(properties, Color.WHITE)


def _parse_positions(str_positions: List[str]) -> List[Pos]:
    return [_parse_position(str_pos) for str_pos in str_positions]


def _parse_init_stones(properties: dict, color: Color) -> List[Stone]:
    property_name: str = "AB" if color == Color.BLACK else "AW"
    if property_name not in properties:
        return []

    stones_pos: List[Pos] = _parse_positions(properties.get(property_name))
    return [Stone(pos, color) for pos in stones_pos]


def _get_init_stones(problem: sgf.GameTree) -> List[Stone]:
    """Gets sgf game tree initial stones"""
    properties: dict = problem.nodes[0].properties

    black_stones: List[Stone] = _parse_init_stones(properties, Color.BLACK)
    white_stones: List[Stone] = _parse_init_stones(properties, Color.WHITE)

    return list(set(black_stones + white_stones))  # remove duplicates


def _get_comment(properties: Dict[str, str]) -> str:
    comment, note = "", ""
    if "C" in properties:
        comment = properties["C"][0]
    if "N" in properties:
        note = properties["N"][0]
    return comment + note


def __is_valid_position(position: Pos) -> bool:
    row, col = position
    return 0 <= row <= 18 and 0 <= col <= 18


def _has_fake_root(problem: sgf.GameTree) -> bool:
    return "AW" not in problem.root.properties and "AB" not in problem.root.properties


def _correct_fake_root(problem: sgf.GameTree):
    # root must have at least 2 nodes
    if len(problem.nodes) == 1:
        raise PreprocessingException("Found impossible fake root with only one node")

    problem.nodes.pop(0)


def _invalid_size(problem: sgf.GameTree) -> bool:
    if "SZ" not in problem.root.properties:
        return False
    return problem.root.properties["SZ"][0] != "19"


def _has_first_empty_branch(problem: sgf.GameTree) -> bool:
    if len(problem.nodes) > 1:
        return False
    first_branch: sgf.GameTree = problem.children[0]
    if len(first_branch.nodes) > 1:
        return False
    properties: Dict[str, str] = first_branch.nodes[0].properties
    return "B" not in properties and "W" not in properties


def _correct_first_empty_branch(problem: sgf.GameTree):
    problem.children.pop(0)  # remove first branch


class TreeAdapter:

    def __init__(self, problem: sgf.GameTree):
        self.__problem = problem

        if _invalid_size(problem):
            raise PreprocessingException("Invalid size")

        if _has_first_empty_branch(problem):
            _correct_first_empty_branch(problem)

        while _has_fake_root(problem):  # can be several nodes
            _correct_fake_root(problem)

        init_stones: List[Stone] = _get_init_stones(problem)
        if not init_stones:
            raise PreprocessingException("Empty initial board")

        init_board: Board = Board(init_stones)
        first_stone: Stone = _get_first_stone(problem)

        self.__normalizer = Normalizer(init_board, first_stone)
        self.__normalizer.normalize_board(init_board)

        self.__root = GameNode(None, init_board, None)
        self.__first_color: Color = first_stone.color

    def parse_tree(self) -> GameTree:
        """Converts an sgf game tree to a game tree for this project"""
        if self.__problem.nodes[1:]:
            last_game_node = self.__add_branch_nodes(self.__problem.nodes[1:], self.__root,
                                                     self.__first_color)  # first node is root
            next_color = last_game_node.stone.color.get_other()
        else:
            last_game_node = self.__root
            next_color = self.__first_color
        if self.__problem.children:
            self.__add_branches(self.__problem.children, last_game_node, next_color)

        return GameTree(self.__root)

    def __add_branches(self, branches: List[sgf.GameTree], game_node: GameNode, color: Color):
        """Recursively adds all branches"""
        for branch in branches:
            if branch.nodes and _check_only_comment_branch_node(branch):
                _correct_only_comment_branch_node(branch)

            if branch.nodes:
                last_game_node = self.__add_branch_nodes(branch.nodes, game_node, color)
                next_color = last_game_node.stone.color.get_other()
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
        normalized_stone = self.__normalizer.normalize_stone(new_stone)
        new_board.place_stone(normalized_stone)

        comment: str = _get_comment(properties)

        return GameNode(game_node, new_board, normalized_stone, comment)
