from typing import List

from src.beans.board.stone import Stone, Color
from src.beans.board.stone_group import StoneGroup


class StoneGroupHandler:
    def __init__(self):
        self.__stone_groups: List[StoneGroup] = []

    @property
    def stone_groups(self) -> List[StoneGroup]:
        return self.__stone_groups

    def __add_stone_to_groups(self, stone: Stone):
        neighbor_groups: List[StoneGroup] = self.__get_neighbor_groups_of_color(stone, stone.color)

        if len(neighbor_groups) == 0:
            self.__add_group(StoneGroup([stone]))
            return

        neighbor_groups[0].add_stone(stone)
        if len(neighbor_groups) != 1:
            self.__fuse_groups(neighbor_groups)

    def __get_groups_of_color(self, color: Color) -> List[StoneGroup]:
        return list(filter(lambda group: group.color == color, self.__stone_groups))

    def __get_neighbor_groups_of_color(self, stone: Stone, color: Color) -> List[StoneGroup]:
        groups: List[StoneGroup] = self.__get_groups_of_color(color)
        return list(filter(lambda group: group.is_attached(stone), groups))

    def __add_group(self, group: StoneGroup):
        self.__stone_groups.append(group)

    def __remove_groups(self, groups: List[StoneGroup]):
        for group in groups:
            self.__stone_groups.remove(group)

    def __fuse_groups(self, groups: List[StoneGroup]):
        self.__remove_groups(groups)
        stones: List[Stone] = [stone for group in groups for stone in group.stones]
        self.__add_group(StoneGroup(stones))
