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
        """Get the other color"""
        return Color.BLACK if self == Color.WHITE else Color.WHITE


def _valid_position(pos: Pos) -> bool:
    row, col = pos
    return 0 <= row <= 18 and 0 <= col <= 18


class Stone:
    """Represents a stone"""

    def __init__(self, color: Color, pos: Pos, liberties: Optional[int] = None):
        """Creates a new stone of given color to be placed in given board position"""
        if not _valid_position(pos):
            raise Exception(f"Trying to create a stone with invalid position {pos}")
        self.__color: Color = color
        self.__pos: Pos = pos
        self.__liberties: Optional[int] = liberties

    def __eq__(self, other: object):
        if not isinstance(other, Stone):
            return False
        return other.color == self.__color and other.pos == self.__pos

    def __hash__(self):
        return hash((self.__color, self.__pos))

    def __str__(self):
        return str(self.__color) + " " + str(self.__pos)

    def __copy__(self) -> Stone:
        return Stone(self.__color, self.__pos, self.__liberties)

    @property
    def color(self) -> Color:
        return self.__color

    @property
    def pos(self) -> Pos:
        return self.__pos

    @property
    def liberties(self) -> int:
        if self.__liberties is None:
            raise Exception(f"Trying to access stone {self} liberties without prior setting")
        return self.__liberties

    @liberties.setter
    def liberties(self, num_liberties: int):
        self.__liberties = num_liberties

    def is_neighbor(self, stone: Stone) -> bool:
        """True if given stone is neighbor"""
        return stone.pos in self.get_neighbor_positions()

    def has_liberties(self):
        """True if the stone has liberties"""
        # Can raise exception
        return self.liberties != 0

    def get_neighbor_positions(self) -> List[Pos]:
        """Returns list of neighbor positions"""
        row, col = self.__pos
        positions: List[Pos] = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        return list(filter(lambda pos: 0 <= pos[0] <= 18 and 0 <= pos[1] <= 18, positions))
