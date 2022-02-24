from typing import List, Optional

from src.beans.board.stone import Stone, Pos
from src.beans.board.stone_group import StoneGroup
from src.beans.board.stone_group_handler import StoneGroupHandler
from src.beans.board.stone_liberties_handler import StoneLibertiesHandler


class StoneCaptureHandler(StoneLibertiesHandler, StoneGroupHandler):
    """Class to compute stone capture"""

    def __init__(self, stones: Optional[List[Stone]]):
        StoneLibertiesHandler.__init__(self, stones)
        StoneGroupHandler.__init__(self, stones)

    def _remove_stones(self, captured_stones):
        pass

    def _capture_groups(self, stone: Stone):
        """Captures groups after given stone is placed"""
        # Remove neighbor groups with no liberties left
        captured_groups: List[StoneGroup] = self.__get_groups_captured_by(stone)
        if captured_groups is None:
            return

        self._remove_groups(captured_groups)

        # Remove stones in the captured groups from the board
        captured_positions: List[Pos] = [pos for group in captured_groups for pos in group.positions]
        self._remove_stones(captured_positions)
        self._remove_liberties_count(captured_positions)

        # Add one liberty to all affected stones
        self._add_liberty_to_neighbors(captured_positions)

    def __get_groups_captured_by(self, stone: Stone) -> List[StoneGroup]:
        """Get groups left without liberties after stone placement"""
        pos, color = stone
        neighbor_groups: List[StoneGroup] = self._get_neighbor_groups_of_color(pos, color.get_other())
        return list(filter(lambda group: not self._has_liberties(group), neighbor_groups))
