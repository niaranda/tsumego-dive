from __future__ import annotations

from copy import deepcopy
from enum import Enum
from typing import Optional, List, Dict

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Stone
from src.beans.gameplay_exception import GamePlayException


class PathType(Enum):
    """Represents a type of path in the game tree"""
    CORRECT = 1
    WRONG = 2
    UNKNOWN = 3  # Unknown means the analysis has yet to be performed
    DUAL = 4  # Dual means analysis could not determine the path type


def _get_stone_from_data(stone_data: Dict[str, str]) -> Stone:
    stone_index = int(list(stone_data.keys())[0])
    row, col = int(stone_index / 19), stone_index % 19
    color = Color.BLACK if list(stone_data.values())[0] == "black" else Color.WHITE

    return Stone((row, col), color)


class GameNode:
    """A node of the game tree, representing a state of the board"""

    def __init__(self, parent: Optional[GameNode], board: Board, stone: Optional[Stone],
                 comment: str = ""):
        """Creates a new game node with given parent, board, lastly placed stone and optional comment.
        Adds this game node to given parent node's children list."""
        self.__parent: Optional[GameNode] = parent
        self.__children: List[GameNode] = []  # The node is initialized without children nodes
        self.__stone: Optional[Stone] = stone
        self.__board: Board = board
        self.__path_type: PathType = PathType.UNKNOWN  # The path type is initialized as unknown
        self.__comment: str = comment

        # Add this node as the parent's child
        if parent:
            parent.add_child(self)

        # Check ko rule
        if self.__broken_ko_rule():
            raise GamePlayException(f"Ko rule broken when adding {self.stone.color} "
                                    f"stone in {self.stone.pos}")

    @property
    def parent(self) -> Optional[GameNode]:
        return self.__parent

    @property
    def children(self) -> List[GameNode]:
        return self.__children

    @property
    def stone(self) -> Optional[Stone]:
        return self.__stone

    @property
    def board(self) -> Board:
        return self.__board

    @property
    def path_type(self) -> PathType:
        return self.__path_type

    @property
    def comment(self) -> str:
        return self.__comment

    @path_type.setter
    def path_type(self, path_type: PathType):
        self.__path_type = path_type

    def add_child(self, game_node: GameNode):
        """Adds child node to this node"""
        self.__children.append(game_node)

    def is_root(self) -> bool:
        """True if the node is the tree root"""
        return self.__parent is None

    def is_leaf(self) -> bool:
        """True if the node is a leaf"""
        return len(self.__children) == 0

    def is_valid(self) -> bool:
        """True if the path type is valid"""
        return self.__path_type in [PathType.CORRECT, PathType.WRONG]

    def is_correct(self) -> bool:
        """True if the path is correct"""
        return self.__path_type == PathType.CORRECT

    def add_children_from_data(self, children_data: List[Dict[str, str]]):
        for child_data in children_data:
            new_stone = _get_stone_from_data(child_data["new_stone"])

            new_board: Board = deepcopy(self.board)
            new_board.place_stone(new_stone)

            comment = ""
            if "path_type" in child_data.keys():
                comment = child_data["path_type"]

            new_game_node = GameNode(self, new_board, new_stone, comment)

            if "children" in child_data.keys():
                new_game_node.add_children_from_data(child_data["children"])

    def __broken_ko_rule(self) -> bool:
        """True if the ko rule was broken when placing the last stone"""
        if self.__parent is None:
            return False

        grandparent = self.__parent.__parent
        if grandparent is None:
            return False

        # Ko rule was broken if the grandparent node has the same board state
        return grandparent.board == self.__board
