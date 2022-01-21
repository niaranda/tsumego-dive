from __future__ import annotations

from enum import Enum
from typing import Optional, List

from src.beans.board.board import Board
from src.beans.board.stone import Stone


class PathType(Enum):
    CORRECT = 1
    WRONG = 2
    UNKNOWN = 3
    DUAL = 4


class GameNode:
    def __init__(self, parent: Optional[GameNode], board: Board, stone: Optional[Stone]):
        self.__parent: Optional[GameNode] = parent
        self.__children: List[GameNode] = []
        self.__stone: Optional[Stone] = stone
        self.__board: Board = board
        self.__path_type: PathType = PathType.UNKNOWN

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

    @path_type.setter
    def path_type(self, path_type: PathType):
        self.__path_type = path_type

    def add_child(self, game_node: GameNode):
        self.__children.append(game_node)

    def is_root(self) -> bool:
        return self.__parent is None

    def is_leaf(self) -> bool:
        return len(self.__children) == 0
