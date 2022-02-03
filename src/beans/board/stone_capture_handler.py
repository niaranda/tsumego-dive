from typing import Tuple, List

from src.beans.board.board_point import BoardPoint
from src.beans.board.stone import Stone
from src.beans.board.stone_group import StoneGroup
from src.beans.board.stone_group_handler import StoneGroupHandler

Pos = Tuple[int, int]


class StoneCaptureHandler(StoneGroupHandler):
    """Class to compute stone capture"""

    def _get_point(self, pos: Pos) -> BoardPoint:
        pass

    def _remove_stones(self, captured_stones):
        pass

    def _capture_groups(self, stone: Stone):
        """Captures groups after given stone is placed"""
        # Update number of liberties for the stone and its neighbors
        self.__update_liberties([stone], True)

        # Remove neighbor groups with no liberties left
        captured_groups: List[StoneGroup] = self.__get_groups_captured_by(stone)
        self._remove_groups(captured_groups)

        # Remove stones for the captured groups from the board
        captured_stones: List[Stone] = [stone for group in captured_groups for stone in group.stones]
        self._remove_stones(captured_stones)

        # Update liberties for all affected stones
        affected_stones = self.__get_neighbor_stones(captured_stones)
        self.__update_liberties(affected_stones, False)

    def __update_liberties(self, stones: List[Stone], update_neighbors: bool):
        """Update liberties for given stones. Optionally update neighbor stones liberties"""
        for stone in stones:
            neighbor_stones: List[Stone] = self.__get_neighbor_stones([stone])
            stone.liberties = 4 - len(neighbor_stones)

            if update_neighbors and neighbor_stones:
                self.__update_liberties(neighbor_stones, False)

    def __get_neighbor_stones(self, stones: List[Stone]) -> List[Stone]:
        """Get neighbor stones for a list of stones"""
        neighbor_stones: List[Stone] = []

        for stone in stones:
            neighbor_positions: List[Pos] = stone.get_neighbor_positions()
            neighbor_points: List[BoardPoint] = [self._get_point(pos) for pos in neighbor_positions]

            filled_neighbor_points: List[BoardPoint] = list(filter(lambda point: not point.is_empty(), neighbor_points))
            neighbor_stones += [point.stone for point in filled_neighbor_points]

        return neighbor_stones

    def __get_groups_captured_by(self, stone: Stone) -> List[StoneGroup]:
        """Get groups left without liberties after stone placement"""
        neighbor_groups: List[StoneGroup] = self._get_neighbor_groups_of_color(stone, stone.color.get_other())
        return list(filter(lambda group: not group.has_liberties(), neighbor_groups))
