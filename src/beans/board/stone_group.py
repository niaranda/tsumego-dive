from __future__ import annotations

from copy import copy
from typing import List

from src.beans.board.color import Color
from src.beans.board.stone import Pos
from src.preprocessing.preprocessing_exception import PreprocessingException


def _are_neighbor_positions(pos1: Pos, pos2: Pos) -> bool:
    """True if given positions are neighbors"""
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
        """Creates a group of stones with given stones and color"""
        self.__positions: List[Pos] = positions
        self.__color = color

        # Check valid state
        if not self.__valid_state():
            raise PreprocessingException(f"Trying to create invalid group {self}")

    def __str__(self) -> str:
        return f"Group: {str(self.__color)} {str([str(pos) for pos in self.__positions])}"

    def __deepcopy__(self, memodict={}) -> StoneGroup:
        positions = copy(self.__positions)
        return StoneGroup(positions, self.__color)

    def __eq__(self, other: StoneGroup) -> bool:
        return self.__color == other.__color and self.__positions == other.__positions

    def __hash__(self) -> int:
        return hash((self.__color, self.__positions))

    @property
    def positions(self) -> List[Pos]:
        return self.__positions

    @positions.setter
    def positions(self, value):
        self.__positions = value

    @property
    def color(self) -> Color:
        return self.__color

    def add_position(self, pos: Pos):
        """Adds a stone to the group"""
        # Check already in group
        if pos in self.__positions:
            raise PreprocessingException(f"Trying to add again stone in {pos} to {self} that contains it")
        self.__positions.append(pos)

    def is_attached(self, position: Pos) -> bool:
        """True if the given position is neighbor to a position in the group"""
        return any([_are_neighbor_positions(position, group_pos) for group_pos in self.__positions])

    def inverse_color(self):
        """Changes the group color"""
        self.__color = self.__color.get_other()

    def __valid_state(self) -> bool:
        """True if the state of the group is valid"""
        # Not empty
        if len(self.__positions) == 0:
            return False

        # No repeated stones
        if len(self.__positions) != len(set(self.__positions)):
            return False

        return True

