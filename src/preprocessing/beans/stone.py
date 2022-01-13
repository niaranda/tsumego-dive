from enum import Enum


class Color(Enum):
    """Represents a stone color"""
    BLACK = 1
    WHITE = -1


class Stone:
    """Represents a stone"""

    def __init__(self, color: Color):
        self.__color: Color = color

    @property
    def color(self) -> Color:
        return self.__color
