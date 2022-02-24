from __future__ import annotations

from typing import List, Optional

from src.beans.board.color import Color
from src.beans.board.stone import Stone, Pos
from src.beans.board.stone_group import StoneGroup
from src.preprocessing.preprocessing_exception import PreprocessingException


class StoneGroupHandler:
    """Class to handle stone groups in board"""

    def __init__(self, stones: Optional[List[Stone]]):
        self.__stone_groups: List[StoneGroup] = []
        if stones:
            for stone in stones:
                self._add_stone_to_groups(stone)

    @property
    def stone_groups(self) -> List[StoneGroup]:
        return self.__stone_groups

    @stone_groups.setter
    def stone_groups(self, groups: List[StoneGroup]):
        self.__stone_groups = groups

    def _add_stone_to_groups(self, stone: Stone):
        """Adds a new stone to the corresponding group"""
        pos, color = stone
        neighbor_groups: List[StoneGroup] = self._get_neighbor_groups_of_color(pos, color)

        # No neighbor group -> the stone is a new group
        if len(neighbor_groups) == 0:
            self.__add_group(StoneGroup([pos], color))
            return

        # Has at least one neighbor group -> add stone to the first group
        neighbor_groups[0].add_position(pos)

        # There is more than one neighbor group -> the stone fuses them into one
        if len(neighbor_groups) != 1:
            self.__fuse_groups(neighbor_groups)

    def _get_neighbor_groups_of_color(self, position: Pos, color: Color) -> List[StoneGroup]:
        """Get the given stone's neighbor groups of given color"""
        groups: List[StoneGroup] = self.__get_groups_of_color(color)
        return list(filter(lambda group: group.is_attached(position), groups))

    def _remove_groups(self, groups: List[StoneGroup]):
        """Remove a list of groups"""
        for group in groups:
            self.__stone_groups.remove(group)

    def _get_group_containing(self, position: Pos) -> StoneGroup:
        for group in self.__stone_groups:
            if position in group.positions:
                return group
        raise PreprocessingException(f"Added stone in {position} is not contained in any group")

    def __get_groups_of_color(self, color: Color) -> List[StoneGroup]:
        """Get all groups of a given color"""
        return list(filter(lambda group: group.color == color, self.__stone_groups))

    def __add_group(self, group: StoneGroup):
        """Add a new group"""
        self.__stone_groups.append(group)

    def __fuse_groups(self, groups: List[StoneGroup]):
        """Fuse given groups into one"""
        # Remove groups
        self._remove_groups(groups)

        # Add new group with all their positions
        positions: List[Pos] = [pos for group in groups for pos in group.positions]
        self.__add_group(StoneGroup(positions, groups[0].color))
