from typing import List, Dict, Optional

from src.beans.board.stone import Pos, Stone
from src.beans.board.stone_group import StoneGroup


class StoneLibertiesHandler:

    def __init__(self, stones: Optional[List[Stone]]):
        self.__stone_liberties: Dict[Pos, int] = {}
        if stones:
            for stone in stones:
                self._compute_liberties(stone[0])

    @property
    def stone_liberties(self) -> Dict[Pos, int]:
        return self.__stone_liberties

    @stone_liberties.setter
    def stone_liberties(self, liberties: Dict[Pos, int]):
        self.__stone_liberties = liberties

    def __get_placed_stone_positions(self) -> List[Pos]:
        pass

    def _get_neighbor_positions(self, position: Pos) -> List[Pos]:
        pass

    def _get_neighbor_stone_positions(self, position: Pos) -> List[Pos]:
        pass

    def _compute_liberties(self, position: Pos):
        neighbor_positions = self._get_neighbor_positions(position)
        neighbor_stones = self._get_neighbor_stone_positions(position)
        self.__stone_liberties[position] = len(neighbor_positions) - len(neighbor_stones)

    def _add_liberty_to_neighbors(self, positions: List[Pos]):
        neighbor_stones = [neighbor for pos in positions for neighbor in self._get_neighbor_stone_positions(pos)]
        for neighbor in neighbor_stones:
            self.__add_liberty(neighbor)

    def _remove_liberty_from_neighbors(self, positions: List[Pos]):
        neighbor_stones = [neighbor for pos in positions for neighbor in self._get_neighbor_stone_positions(pos)]
        for neighbor in neighbor_stones:
            self.__remove_liberty(neighbor)

    def _has_liberties(self, group: StoneGroup) -> bool:
        for pos in group.positions:
            if self.__stone_liberties[pos] != 0:
                return True
        return False

    def _remove_liberty_count(self, position: Pos):
        del self.__stone_liberties[position]

    def _remove_liberties_count(self, positions: List[Pos]):
        for pos in positions:
            self._remove_liberty_count(pos)

    def __add_liberty(self, position: Pos):
        self.__stone_liberties[position] += 1

    def __remove_liberty(self, position: Pos):
        self.__stone_liberties[position] -= 1
