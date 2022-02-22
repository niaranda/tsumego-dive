from typing import List, Tuple, Dict

from src.beans.board.color import Color
from src.beans.board.stone_group import StoneGroup

Pos = Tuple[int, int]
Stone = Tuple[Pos, Color]


def _get_neighbor_positions(position: Pos) -> List[Pos]:
    """Returns list of neighbor positions"""
    row, col = position
    positions: List[Pos] = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    return list(filter(lambda pos: 0 <= pos[0] <= 18 and 0 <= pos[1] <= 18, positions))


class StoneLibertiesHandler:

    def __init__(self):
        super().__init__()
        self.__stone_liberties: Dict[Pos, int] = {}

    @property
    def stone_liberties(self) -> Dict[Pos, int]:
        return self.__stone_liberties

    def get_placed_stone_positions(self) -> List[Pos]:
        pass

    def add_liberty(self, position: Pos):
        self.__stone_liberties[position] += 1

    def remove_liberty(self, position: Pos):
        self.__stone_liberties[position] -= 1

    def _compute_liberties(self, position: Pos):
        neighbor_positions = _get_neighbor_positions(position)
        neighbor_stones = self.__get_neighbor_stones(position)
        self.__stone_liberties[position] = len(neighbor_positions) - len(neighbor_stones)

    def _add_liberty_to_neighbors(self, positions: List[Pos]):
        neighbor_stones = [neighbor for pos in positions for neighbor in self.__get_neighbor_stones(pos)]
        for neighbor in neighbor_stones:
            self.add_liberty(neighbor)

    def _remove_liberty_from_neighbors(self, positions: List[Pos]):
        neighbor_stones = [neighbor for pos in positions for neighbor in self.__get_neighbor_stones(pos)]
        for neighbor in neighbor_stones:
            self.remove_liberty(neighbor)

    def _has_liberties(self, group: StoneGroup) -> bool:
        for pos in group.positions:
            if self.__stone_liberties[pos] != 0:
                return True
        return False

    def __get_neighbor_stones(self, position: Pos) -> List[Pos]:
        neighbor_positions = _get_neighbor_positions(position)
        return list(filter(lambda pos: pos in neighbor_positions, self.get_placed_stone_positions()))
