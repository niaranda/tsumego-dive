from typing import List, Dict, Optional

from src.beans.board.stone import Pos, Stone
from src.beans.board.stone_group import StoneGroup


class StoneLibertiesHandler:
    """Handles stone liberties count"""

    def __init__(self, stones: Optional[List[Stone]]):
        # Compute liberties for all placed stones
        self.__stone_liberties: Dict[Pos, int] = {}
        if stones:
            for stone in stones:
                self._compute_liberties(stone.pos)

    @property
    def stone_liberties(self) -> Dict[Pos, int]:
        return self.__stone_liberties

    @stone_liberties.setter
    def stone_liberties(self, liberties: Dict[Pos, int]):
        self.__stone_liberties = liberties

    def _get_placed_stone_positions(self) -> List[Pos]:
        """Returns list of occupied positions"""
        pass

    def _get_neighbor_positions(self, position: Pos) -> List[Pos]:
        """Returns list of neighbor positions"""
        pass

    def _get_neighbor_stone_positions(self, position: Pos) -> List[Pos]:
        """Returns list of neighbor positions containing stones"""
        pass

    def _compute_liberties(self, position: Pos):
        """Computes the number of liberties of the stone placed in given position"""
        neighbor_positions = self._get_neighbor_positions(position)
        neighbor_stones = self._get_neighbor_stone_positions(position)
        self.__stone_liberties[position] = len(neighbor_positions) - len(neighbor_stones)

    def _add_liberty_to_neighbors(self, positions: List[Pos]):
        """Adds one liberty to the stones that are neighbors to any of given positions"""
        neighbor_stones = [neighbor for pos in positions for neighbor in self._get_neighbor_stone_positions(pos)]
        for neighbor in neighbor_stones:
            self.__add_liberty(neighbor)

    def _remove_liberty_from_neighbors(self, positions: List[Pos]):
        """Removes one liberty to the stones that are neighbors to any of given positions"""
        neighbor_stones = [neighbor for pos in positions for neighbor in self._get_neighbor_stone_positions(pos)]
        for neighbor in neighbor_stones:
            self.__remove_liberty(neighbor)

    def _has_liberties(self, group: StoneGroup) -> bool:
        """True if the given group has liberties"""
        for pos in group.positions:
            if self.__stone_liberties[pos] != 0:  # if any stone in the group has liberties, so does the group
                return True
        return False

    def _remove_liberty_count(self, position: Pos):
        """Removes given position from the count of liberties"""
        del self.__stone_liberties[position]

    def _remove_liberties_count(self, positions: List[Pos]):
        """Removes given positions from the count of liberties"""
        for pos in positions:
            self._remove_liberty_count(pos)

    def __add_liberty(self, position: Pos):
        """Adds one liberty to given position"""
        self.__stone_liberties[position] += 1

    def __remove_liberty(self, position: Pos):
        """Removes one liberty to given position"""
        self.__stone_liberties[position] -= 1
