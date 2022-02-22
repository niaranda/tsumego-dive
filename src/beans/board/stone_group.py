from typing import List, Tuple

from src.beans.board.color import Color
from src.preprocessing.preprocessing_exception import PreprocessingException

Pos = Tuple[int, int]


def _are_neighbor_positions(pos1: Pos, pos2: Pos) -> bool:
    row1, col1 = pos1
    row2, col2 = pos2
    if row1 != row2 and col1 != col2:
        return False
    if row1 == row2:
        return abs(col1 - col2) == 1
    return abs(row1 - row2) == 1


class StoneGroup:
    """Represents a group of stones"""

    def __init__(self, positions: List[Pos], color: Color):
        """Create a group of stones with given stones"""
        self.__positions: List[Pos] = positions
        self.__color = color

        # Check valid state
        if not self.__valid_state():
            raise PreprocessingException(f"Trying to create invalid group {self}")

    def __str__(self) -> str:
        return f"Group: {str(self.__color)} {str([str(pos) for pos in self.__positions])}"

    @property
    def positions(self) -> List[Pos]:
        return self.__positions

    @property
    def color(self) -> Color:
        return self.__color

    def add_position(self, pos: Pos):
        """Adds a stone to the group"""
        # Check already in group
        if pos in self.__positions:
            raise PreprocessingException(f"Trying to add again stone in {pos} to group {self} that contains it")
        self.__positions.append(pos)

    def is_attached(self, position: Pos) -> bool:
        """True if the given position is neighbor to a position in the group"""
        return any([_are_neighbor_positions(position, group_pos) for group_pos in self.__positions])

    def __valid_state(self) -> bool:
        # Not empty
        if len(self.__positions) == 0:
            return False

        # No repeated stones
        if len(self.__positions) != len(set(self.__positions)):
            return False

        return True
