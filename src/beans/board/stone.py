from __future__ import annotations

from enum import Enum
from typing import Tuple, Optional, List

Pos = Tuple[int, int]


class Color(Enum):
    """Represents a stone color"""
    BLACK = 1
    WHITE = -1

    def __str__(self):
        return self.name

    def get_other(self):
        return Color.BLACK if self == Color.WHITE else Color.WHITE


class Stone:
    """Represents a stone"""

    def __init__(self, color: Color, pos: Pos, liberties: Optional[int] = None):
        self.__color: Color = color
        self.__pos: Pos = pos
        self.__liberties: Optional[int] = liberties

    def __str__(self):
        return str(self.__color) + " " + str(self.__pos)

    @property
    def color(self) -> Color:
        return self.__color

    @property
    def pos(self) -> Pos:
        return self.__pos

    @property
    def liberties(self) -> int:
        return self.__liberties

    @liberties.setter
    def liberties(self, num_liberties: int):
        self.__liberties = num_liberties

    def is_neighbor(self, stone: Stone) -> bool:
        self_row, self_col = self.__pos
        row, col = stone.pos

        if abs(self_row - row) == 1 and self_col == col:
            return True
        return abs(self_col - col) == 1 and self_row == row

    def has_liberties(self):
        return self.__liberties != 0
