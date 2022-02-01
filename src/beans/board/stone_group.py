from typing import List, Tuple

from src.beans.board.stone import Color, Stone

Pos = Tuple[int, int]


class StoneGroup:
    """Represents a group of stones"""

    def __init__(self, stones: List[Stone]):
        """Create a group of stones with given stones"""
        self.__stones: List[Stone] = stones

        # Check valid state
        if not self.__valid_state():
            raise Exception(f"Trying to create invalid group {self}")

    def __str__(self) -> str:
        return str([str(stone) for stone in self.__stones])

    @property
    def stones(self):
        return self.__stones

    def add_stone(self, stone: Stone):
        """Adds a stone to the group"""
        # Check same color
        if stone.color != self.get_color():
            raise Exception(f"Trying to add stone {stone} to group {self} of different color")
        # Check already in group
        if stone in self.__stones:
            raise Exception(f"Trying to add again stone {stone} to group {self} that contains it")
        self.__stones.append(stone)

    def get_color(self) -> Color:
        """Get the group color"""
        return self.__stones[0].color

    def get_positions(self) -> List[Pos]:
        """Get positions of stones in the group"""
        return [stone.pos for stone in self.__stones]

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
