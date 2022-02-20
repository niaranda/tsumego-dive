from __future__ import annotations

from copy import copy
from typing import Optional, Tuple

from src.beans.board.stone import Stone, Color
from src.beans.gameplay_exception import GamePlayException

Pos = Tuple[int, int]


class BoardPoint:
    """Represents a board point"""

    def __init__(self, pos: Pos):
        """Creates an empty board point in given board position"""
        self.__stone: Optional[Stone] = None
        self.__pos: Pos = pos

    def __str__(self):
        if self.__stone is None:
            return " "
        return "X" if self.__stone.color == Color.BLACK else "O"

    def __deepcopy__(self, memodict={}) -> BoardPoint:
        new_point = BoardPoint(self.__pos)
        if self.is_empty():
            return new_point
        new_point.stone = copy(self.__stone)
        return new_point

    @property
    def stone(self) -> Optional[Stone]:
        return self.__stone

    @stone.setter
    def stone(self, stone: Stone):
        if self.__stone is not None:
            raise GamePlayException(f"Trying to place a stone {stone} in point already containing {self.__stone}")
        if stone.pos != self.__pos:
            raise GamePlayException(f"Trying to place a stone {stone} in wrong position {self.__pos}")
        self.__stone = stone

    @property
    def pos(self) -> Pos:
        return self.__pos

    def is_empty(self) -> bool:
        """True if the point is empty"""
        return self.__stone is None

    def remove_stone(self):
        """Removes the placed stone"""
        if self.is_empty():
            raise GamePlayException(f"Trying to remove a stone from empty point {self.__pos}")
        self.__stone = None
