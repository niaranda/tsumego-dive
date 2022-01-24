from typing import Optional, Tuple

from src.beans.board.stone import Stone, Color


Pos = Tuple[int, int]


class BoardPoint:
    """Represents a board point"""

    def __init__(self, pos: Pos):
        self.__stone: Optional[Stone] = None
        self.__pos: Pos = pos

    def __str__(self):
        if self.__stone is None:
            return " "
        return "X" if self.__stone.color == Color.BLACK else "O"

    @property
    def stone(self) -> Optional[Stone]:
        return self.__stone

    @stone.setter
    def stone(self, stone: Stone):
        if self.__stone is not None:
            raise Exception()
        self.__stone = stone

    @property
    def pos(self) -> Pos:
        return self.__pos

    def place_stone(self, color: Color):
        """Places a stone of given color in this board point"""
        if self.__stone is not None:
            raise Exception("Stone placement error")
        self.__stone = Stone(color, self.pos)

    def is_empty(self) -> bool:
        return self.__stone is None
