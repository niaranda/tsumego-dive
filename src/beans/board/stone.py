from enum import Enum
from typing import Tuple

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

    def __init__(self, color: Color, pos: Pos):
        self.__color: Color = color
        self.__pos: Pos = pos

    def __str__(self):
        return str(self.__color) + " " + str(self.__pos)

    @property
    def color(self) -> Color:
        return self.__color

    @property
    def pos(self) -> Pos:
        return self.__pos
