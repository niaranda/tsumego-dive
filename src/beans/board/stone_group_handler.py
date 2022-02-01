from typing import List

from src.beans.board.stone import Stone, Color
from src.beans.board.stone_group import StoneGroup


class StoneGroupHandler:
    """Class to handle stone groups in board"""

    def __init__(self):
        self.__stone_groups: List[StoneGroup] = []

    @property
    def stone_groups(self) -> List[StoneGroup]:
        return self.__stone_groups

    def __add_stone_to_groups(self, stone: Stone):
        """Adds a new stone to the corresponding group"""
        neighbor_groups: List[StoneGroup] = self.__get_neighbor_groups_of_color(stone, stone.color)

        # No neighbor group -> the stone is a new group
        if len(neighbor_groups) == 0:
            self.__add_group(StoneGroup([stone]))
            return

        # Has at least one neighbor group -> add stone to the first group
        neighbor_groups[0].add_stone(stone)

        # There is more than one neighbor group -> the stone fuses them into one
        if len(neighbor_groups) != 1:
            self.__fuse_groups(neighbor_groups)

    def __get_groups_of_color(self, color: Color) -> List[StoneGroup]:
        """Get all groups of a given color"""
        return list(filter(lambda group: group.color == color, self.__stone_groups))

    def __get_neighbor_groups_of_color(self, stone: Stone, color: Color) -> List[StoneGroup]:
        """Get the given stone's neighbor groups of given color"""
        groups: List[StoneGroup] = self.__get_groups_of_color(color)
        return list(filter(lambda group: group.is_attached(stone), groups))

    def __add_group(self, group: StoneGroup):
        """Add a new group"""
        self.__stone_groups.append(group)

    def __remove_groups(self, groups: List[StoneGroup]):
        """Remove a list of groups"""
        for group in groups:
            self.__stone_groups.remove(group)

    def __fuse_groups(self, groups: List[StoneGroup]):
        """Fuse given groups into one"""
        # Remove groups
        self.__remove_groups(groups)

        # Add new group with all their stones
        stones: List[Stone] = [stone for group in groups for stone in group.stones]
        self.__add_group(StoneGroup(stones))
