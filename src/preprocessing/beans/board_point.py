from typing import Optional, Tuple

from src.preprocessing.beans.stone import Stone, Color


class BoardPoint:
    """Represents a board point"""

    def __init__(self, pos: Tuple[int, int]):
        self.__stone: Optional[Stone] = None
        self.__pos: Tuple[int, int] = pos

    @property
    def stone(self) -> Optional[Stone]:
        return self.__stone

    @property
    def pos(self) -> Tuple[int, int]:
        return self.__pos

    def place_stone(self, color: Color):
        """Places a stone of given color in this board point"""
        if self.__stone is not None:
            raise Exception("Stone placement error")
        self.__stone = Stone(color, self.pos)

    def is_empty(self) -> bool:
        return self.__stone is None
