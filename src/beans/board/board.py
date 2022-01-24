from typing import List, Tuple, Optional

import numpy as np

from src.beans.board.board_point import BoardPoint
from src.beans.board.stone import Stone, Color
from src.beans.board.stone_group import StoneGroup

Pos = Tuple[int, int]


class Board:
    """Represents a Go board"""

    def __init__(self, stones: Optional[List[Stone]] = None):
        self.__grid = np.empty((19, 19), dtype=BoardPoint)
        for index, _ in np.ndenumerate(self.__grid):
            self.__grid[index] = BoardPoint(index)

        self.__stone_groups: List[StoneGroup] = []
        if stones is not None:
            self.place_stones(stones)

    def __str__(self):
        str_board: str = ""
        row: np.ndarray
        for row in self.__grid:
            str_board += " ---" * 19 + "\n| "
            point: BoardPoint
            for point in row:
                str_board += str(point) + " | "
            str_board += "\n"
        return str_board + " ---" * 19 + "\n"

    def get_stones(self) -> List[Stone]:
        stones: List[Stone] = []
        board_point: BoardPoint
        for _, board_point in np.ndenumerate(self.__grid):
            if not board_point.is_empty():
                stones.append(board_point.stone)
        return stones

    def place_stones(self, stones: List[Stone]):
        """Places a list of stones in the board"""
        for stone in stones:
            self.place_stone(stone)

    def place_stone(self, stone: Stone):
        """Places a stone in the board"""
        pos = stone.pos
        point = self.__get_point(pos)
        point.stone = stone

        self.__add_stone_to_groups(stone)

    def __get_point(self, pos: Pos) -> BoardPoint:
        return self.__grid[pos]

    def __add_stone_to_groups(self, stone: Stone):
        groups: List[StoneGroup] = self.__get_groups_of_color(stone.color)
        neighbor_groups: List[StoneGroup] = list(filter(lambda group: group.is_attached(stone), groups))

        if len(neighbor_groups) == 0:
            self.__add_group(StoneGroup([stone]))
            return

        neighbor_groups[0].add_stone(stone)
        if len(neighbor_groups) != 1:
            self.__fuse_groups(neighbor_groups)

    def __get_groups_of_color(self, color: Color) -> List[StoneGroup]:
        return list(filter(lambda group: group.color == color, self.__stone_groups))

    def __add_group(self, group: StoneGroup):
        self.__stone_groups.append(group)

    def __remove_groups(self, groups: List[StoneGroup]):
        for group in groups:
            self.__stone_groups.remove(group)

    def __fuse_groups(self, groups: List[StoneGroup]):
        self.__remove_groups(groups)
        stones: List[Stone] = [stone for group in groups for stone in group.stones]
        self.__add_group(StoneGroup(stones))
