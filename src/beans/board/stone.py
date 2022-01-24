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
        return stone.pos in self.get_neighbor_positions()

    def has_liberties(self):
        return self.__liberties != 0

    def get_neighbor_positions(self) -> List[Pos]:
        row, col = self.__pos
        positions: List[Pos] = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        return list(filter(lambda pos: 0 <= pos[0] <= 18 and 0 <= pos[1] <= 18, positions))
