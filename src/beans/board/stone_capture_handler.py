from typing import Tuple, List

from src.beans.board.board_point import BoardPoint
from src.beans.board.stone import Stone
from src.beans.board.stone_group import StoneGroup
from src.beans.board.stone_group_handler import StoneGroupHandler

Pos = Tuple[int, int]


class StoneCaptureHandler(StoneGroupHandler):
    def __get_point(self, pos: Pos) -> BoardPoint:
        pass

    def __remove_stones(self, captured_stones):
        pass

    def __capture_groups(self, stone: Stone):
        self.__compute_liberties([stone])

        captured_groups: List[StoneGroup] = self.__get_groups_captured_by(stone)
        self.__remove_groups(captured_groups)

        captured_stones: List[Stone] = [stone for group in captured_groups for stone in group.stones]
        self.__remove_stones(captured_stones)

        affected_stones = self.__get_neighbor_stones(captured_stones)
        self.__compute_liberties(affected_stones)

    def __compute_liberties(self, stones: List[Stone]):
        for stone in stones:
            neighbor_stones: List[Stone] = self.__get_neighbor_stones([stone])
            stone.liberties = len(neighbor_stones)

            self.__compute_liberties(neighbor_stones)

    def __get_neighbor_stones(self, stones: List[Stone]) -> List[Stone]:
        neighbor_stones = []

        for stone in stones:
            neighbor_positions = stone.get_neighbor_positions()
            neighbor_points = [self.__get_point(pos) for pos in neighbor_positions]

            filled_neighbor_points = list(filter(lambda point: not point.is_empty(), neighbor_points))
            neighbor_stones += [point.stone for point in filled_neighbor_points]

        return neighbor_stones

    def __get_groups_captured_by(self, stone: Stone) -> List[StoneGroup]:
        neighbor_groups: List[StoneGroup] = self.__get_neighbor_groups_of_color(stone, stone.color.get_other())
        return list(filter(lambda group: not group.has_liberties(), neighbor_groups))
