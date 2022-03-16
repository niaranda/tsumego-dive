from copy import deepcopy
from typing import List, Dict

import sgf

import src.preprocessing.corrections.tree_adapter_corrections as corrections
from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Pos, Stone
from src.beans.game_tree.game_node import GameNode
from src.beans.game_tree.game_tree import GameTree
from src.beans.gameplay_exception import GamePlayException
from src.preprocessing.adapter.normalizer import Normalizer
from src.preprocessing.errors.preprocessing_exception import PreprocessingException


def _parse_position(str_position: str) -> Pos:
    """Returns position by parsing given string format position"""
    if not str_position:  # If string is empty, the movement is a pass
        raise GamePlayException("Unallowed pass")

    if len(str_position) != 2:  # Should have two letters
        raise PreprocessingException(f"Wrong stone position format {str_position} in sgf")

    col, row = str_position.lower()
    return ord(col) - ord("a"), ord(row) - ord("a")


def _parse_stone(properties: Dict[str, str], color: Color) -> Stone:
    """Returns stone of expected given color by parsing given properties"""
    property_name: str = "B" if color == Color.BLACK else "W"

    if property_name not in properties:
        raise PreprocessingException(f"Not found expected {color} stone property while parsing sgf tree")

    # Get position from properties
    pos: Pos = _parse_position(properties.get(property_name)[0])

    # Check valid position
    if __is_valid_position(pos):
        return Stone(pos, color)

    # "ZZ" means a pass
    row, col = pos
    if row == 25 and col == 25:
        raise GamePlayException("Unallowed pass")

    raise PreprocessingException(f"Wrong stone position {properties.get(property_name)[0]}")


def _get_first_node_properties(problem: sgf.GameTree) -> Dict[str, str]:
    """Returns properties of first node of given problem"""
    # If first branch has more than one node, the second one is the first node (first has initial board properties)
    if len(problem.nodes) > 1:
        return problem.nodes[1].properties

    # Else get first node of first branch
    return problem.children[0].root.properties


def _get_first_stone(problem: sgf.GameTree) -> Stone:
    """Returns first stone for given problem"""
    # Get first stone properties
    properties: Dict[str, str] = _get_first_node_properties(problem)

    # First node should have a stone placement
    if "B" not in properties and "W" not in properties:

        # If no stone found, this could be an only comment node
        if "C" in properties or "N" in properties:
            # Perform correction
            corrections.correct_only_comment_first_node(problem)

            # Try retrieving first node properties again
            properties = _get_first_node_properties(problem)

            if "B" not in properties and "W" not in properties:  # Still no stone
                raise PreprocessingException("Found no stone while parsing sgf tree root")

    # Should not have both colors
    if "B" in properties and "W" in properties:
        raise PreprocessingException("Found stones for both colors while parsing sgf tree root")

    if "B" in properties:  # Has black stone
        return _parse_stone(properties, Color.BLACK)

    # Has white stone
    return _parse_stone(properties, Color.WHITE)


def _parse_positions(str_positions: List[str]) -> List[Pos]:
    """Returns list of positions by parsing list of string format positions"""
    return [_parse_position(str_pos) for str_pos in str_positions]


def _parse_init_stones(properties: dict, color: Color) -> List[Stone]:
    """Returns list of initial stones by parsing given properties for given color"""
    property_name: str = "AB" if color == Color.BLACK else "AW"
    if property_name not in properties:  # No stones for given color
        return []

    # Get positions
    stones_pos: List[Pos] = _parse_positions(properties.get(property_name))
    # Create stones
    return [Stone(pos, color) for pos in stones_pos]


def _get_init_stones(problem: sgf.GameTree) -> List[Stone]:
    """Returns list of initial stones in given problem"""
    # Initial stones info is in first node properties
    properties: dict = problem.nodes[0].properties

    black_stones: List[Stone] = _parse_init_stones(properties, Color.BLACK)
    white_stones: List[Stone] = _parse_init_stones(properties, Color.WHITE)

    return list(set(black_stones + white_stones))  # remove duplicates


def _get_comment(properties: Dict[str, str]) -> str:
    """Retrieves comment from given properties. Returns empty string if none found"""
    # Comments can appear with C or N keys
    comment, note = "", ""

    if "C" in properties:
        comment = properties["C"][0]  # always list of one element

    if "N" in properties:
        note = properties["N"][0]  # always list of one element

    return comment + note  # Join both types


def _has_invalid_size(problem: sgf.GameTree) -> bool:
    """True if the problem size is not 19x19.
    No size specified is considered 19x19 by default"""
    if "SZ" not in problem.root.properties:  # No size specified
        return False

    return problem.root.properties["SZ"][0] != "19"


def __is_valid_position(position: Pos) -> bool:
    """Returns true if given position is valid"""
    row, col = position
    return 0 <= row <= 18 and 0 <= col <= 18  # inside the board grid


class TreeAdapter:
    """Performs sgf.GameTree to this project's GameTree class adaptation"""

    def __init__(self, problem: sgf.GameTree):
        self.__problem = problem

        # Check invalid size
        if _has_invalid_size(problem):
            raise PreprocessingException("Invalid size")

        # Perform corrections
        while corrections.has_first_empty_branch(problem):  # can have several empty branches
            corrections.correct_first_empty_branch(problem)

        while corrections.has_fake_root(problem):  # can be several nodes
            corrections.correct_fake_root(problem)

        # Place initial stones
        init_stones: List[Stone] = _get_init_stones(problem)
        init_board: Board = Board(init_stones)

        # Perform normalization
        first_stone: Stone = _get_first_stone(problem)
        self.__normalizer = Normalizer(init_board, first_stone.color)
        self.__normalizer.normalize_board(init_board)

        # Create root and first color property
        self.__root = GameNode(None, init_board, None)
        self.__first_color: Color = first_stone.color

    def parse_tree(self) -> GameTree:
        """Returns adapted tree by parsing sgf tree in property"""
        # If the problem begins with only one branch (first node has initial board properties)
        if self.__problem.nodes[1:]:
            # Add all nodes
            last_game_node = self.__add_branch_nodes(self.__problem.nodes[1:], self.__root,
                                                     self.__first_color)
            # Get next color
            next_color = last_game_node.stone.color.get_other()

        else:  # The problem does not begin with one branch
            # The last node is root and next color is first color
            last_game_node = self.__root
            next_color = self.__first_color

        if self.__problem.children:  # The problem has several branches
            self.__add_branches(self.__problem.children, last_game_node, next_color)

        # Create GameTree object
        return GameTree(self.__root)

    def __add_branches(self, branches: List[sgf.GameTree], game_node: GameNode, color: Color):
        """Recursively adds all given branches as given game node's children. The first color is given color"""
        for branch in branches:
            # If the branch starts with several nodes, it could begin with an only comment node
            if branch.nodes and corrections.check_only_comment_branch_node(branch):
                corrections.correct_only_comment_branch_node(branch)

            # After removing the only comment node, there could be no nodes remaining
            if branch.nodes:
                # If there are nodes, add them to tree
                last_game_node = self.__add_branch_nodes(branch.nodes, game_node, color)
                # Get next color
                next_color = last_game_node.stone.color.get_other()
            else:
                # If there were no nodes, the last one is given argument. Same with color
                last_game_node = game_node
                next_color = color

            # If branch has children branches, add those recursively
            if branch.children:
                self.__add_branches(branch.children, last_game_node, next_color)

    def __add_branch_nodes(self, nodes: List[sgf.Node], game_node: GameNode, color: Color):
        """Creates game nodes for all given nodes as children of given game node. Next color is given color."""
        last_game_node = game_node
        next_color = color

        for node in nodes:
            last_game_node = self.__create_game_node(node.properties, last_game_node, next_color)
            next_color = next_color.get_other()

        return last_game_node

    def __create_game_node(self, properties: dict, game_node: GameNode, color: Color) -> GameNode:
        """Creates a new game node with given parent node by adding a new stone of given color to the board.
        The stone position is searched for in given properties"""
        # Get new stone from properties
        new_stone: Stone = _parse_stone(properties, color)

        # Copy current board
        new_board: Board = deepcopy(game_node.board)

        # Normalize stone and place it in board
        normalized_stone = self.__normalizer.normalize_stone(new_stone)
        new_board.place_stone(normalized_stone)

        comment: str = _get_comment(properties)

        # Create game node
        return GameNode(game_node, new_board, normalized_stone, comment)
