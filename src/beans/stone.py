from enum import Enum
from typing import Tuple


class Color(Enum):
    """Represents a stone color"""
    BLACK = 1
    WHITE = -1


class Stone:
    """Represents a stone"""

    def __init__(self, color: Color, pos: Tuple[int, int]):
        self.__color: Color = color
        self.__pos: Tuple[int, int] = pos

    @property
    def color(self) -> Color:
        return self.__color

    @property
    def pos(self) -> Tuple[int, int]:
        return self.__pos
