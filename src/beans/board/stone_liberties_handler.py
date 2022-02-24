from typing import List, Dict, Optional

from src.beans.board.stone import Pos, Stone
from src.beans.board.stone_group import StoneGroup


def _get_neighbor_positions(position: Pos) -> List[Pos]:
    """Returns list of neighbor positions"""
    row, col = position
    positions: List[Pos] = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    return list(filter(lambda pos: 0 <= pos[0] <= 18 and 0 <= pos[1] <= 18, positions))


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

    def get_placed_stone_positions(self) -> List[Pos]:
        pass

    def _compute_liberties(self, position: Pos):
        neighbor_positions = _get_neighbor_positions(position)
        neighbor_stones = self.__get_neighbor_stones(position)
        self.__stone_liberties[position] = len(neighbor_positions) - len(neighbor_stones)

    def _add_liberty_to_neighbors(self, positions: List[Pos]):
        neighbor_stones = [neighbor for pos in positions for neighbor in self.__get_neighbor_stones(pos)]
        for neighbor in neighbor_stones:
            self.__add_liberty(neighbor)

    def _remove_liberty_from_neighbors(self, positions: List[Pos]):
        neighbor_stones = [neighbor for pos in positions for neighbor in self.__get_neighbor_stones(pos)]
        for neighbor in neighbor_stones:
            self.__remove_liberty(neighbor)

    def _has_liberties(self, group: StoneGroup) -> bool:
        for pos in group.positions:
            if self.__stone_liberties[pos] != 0:
                return True
        return False

    def __add_liberty(self, position: Pos):
        self.__stone_liberties[position] += 1

    def __remove_liberty(self, position: Pos):
        self.__stone_liberties[position] -= 1

    def __get_neighbor_stones(self, position: Pos) -> List[Pos]:
        neighbor_positions = _get_neighbor_positions(position)
        return list(filter(lambda pos: pos in neighbor_positions, self.get_placed_stone_positions()))
