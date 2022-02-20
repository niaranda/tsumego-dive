from typing import List, Tuple

from src.beans.board.stone import Color, Stone
from src.preprocessing.preprocessing_exception import PreprocessingException

Pos = Tuple[int, int]


class StoneGroup:
    """Represents a group of stones"""

    def __init__(self, stones: List[Stone], validate: bool = True):
        """Create a group of stones with given stones"""
        self.__stones: List[Stone] = stones
        self.__positions: List[Pos] = [stone.pos for stone in stones]

        # Check valid state
        if validate and not self.__valid_state():
            raise PreprocessingException(f"Trying to create invalid group {self}")

    def __str__(self) -> str:
        return str([str(stone) for stone in self.__stones])

    @property
    def stones(self) -> List[Stone]:
        return self.__stones

    @stones.setter
    def stones(self, stones):
        self.__stones = stones

    @property
    def positions(self) -> List[Pos]:
        return self.__positions

    @positions.setter
    def positions(self, positions):
        self.__positions = positions

    def add_stone(self, stone: Stone):
        """Adds a stone to the group"""
        # Check same color
        if stone.color != self.get_color():
            raise PreprocessingException(f"Trying to add stone {stone} to group {self} of different color")
        # Check already in group
        if stone in self.__stones:
            raise PreprocessingException(f"Trying to add again stone {stone} to group {self} that contains it")
        self.__stones.append(stone)
        self.__positions.append(stone.pos)

    def get_color(self) -> Color:
        """Get the group color"""
        return self.__stones[0].color

    def is_attached(self, stone: Stone):
        """True if the given stone is neighbor to a stone in the group"""
        return any([group_stone.is_neighbor(stone) for group_stone in self.__stones])

    def has_liberties(self) -> bool:
        """True if the group has liberties"""
        for stone in self.__stones:
            if stone.has_liberties():
                return True
        return False

    def __valid_state(self) -> bool:
        # Not empty
        if len(self.__stones) == 0:
            return False

        # No repeated stones
        if len(self.__stones) != len(set(self.__stones)):
            return False

        # All stones have the same color
        return all([stone.color == self.get_color() for stone in self.__stones])
