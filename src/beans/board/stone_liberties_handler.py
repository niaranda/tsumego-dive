from typing import List, Tuple

from src.beans.board.board_point import BoardPoint
from src.beans.board.stone import Stone

Pos = Tuple[int, int]


class StoneLibertiesHandler:

    def _get_point(self, pos: Pos) -> BoardPoint:
        pass

    def _compute_liberties(self, stone: Stone):
        """Compute liberties for a stone"""
        neighbor_points: List[BoardPoint] = self.__get_neighbor_points(stone)
        empty_neighbor_points: List[BoardPoint] = list(filter(lambda point: point.is_empty(), neighbor_points))

        stone.liberties = len(empty_neighbor_points)

    def _update_neighbor_liberties(self, stones: List[Stone], quantity: int):
        """Update stone liberties for neighbor of given stones in given quantity"""
        neighbor_stones: List[Stone] = self.__get_neighbor_stones(stones)
        for stone in neighbor_stones:
            stone.liberties += quantity

    def __get_neighbor_points(self, stone: Stone) -> List[BoardPoint]:
        neighbor_positions: List[Pos] = stone.get_neighbor_positions()
        return [self._get_point(pos) for pos in neighbor_positions]

    def __get_neighbor_stones(self, stones: List[Stone]) -> List[Stone]:
        neighbor_points: List[BoardPoint] = [point for stone in stones for point in self.__get_neighbor_points(stone)]
        filled_neighbor_points: List[BoardPoint] = list(filter(lambda point: not point.is_empty(), neighbor_points))
        return [point.stone for point in filled_neighbor_points]
