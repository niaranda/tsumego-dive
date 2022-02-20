from typing import Tuple, List

from src.beans.board.board_point import BoardPoint
from src.beans.board.stone import Stone
from src.beans.board.stone_group import StoneGroup
from src.beans.board.stone_group_handler import StoneGroupHandler
from src.beans.board.stone_liberties_handler import StoneLibertiesHandler

Pos = Tuple[int, int]


class StoneCaptureHandler(StoneGroupHandler, StoneLibertiesHandler):
    """Class to compute stone capture"""

    def get_point(self, pos: Pos) -> BoardPoint:
        pass

    def _remove_stones(self, captured_stones):
        pass

    def _capture_groups(self, stone: Stone):
        """Captures groups after given stone is placed"""
        # Remove neighbor groups with no liberties left
        captured_groups: List[StoneGroup] = self.__get_groups_captured_by(stone)
        self._remove_groups(captured_groups)

        # Remove stones in the captured groups from the board
        captured_stones: List[Stone] = [stone for group in captured_groups for stone in group.stones]
        self._remove_stones(captured_stones)

        # Add one liberty to all affected stones
        self._update_neighbor_liberties(captured_stones, 1)

    def __get_groups_captured_by(self, stone: Stone) -> List[StoneGroup]:
        """Get groups left without liberties after stone placement"""
        neighbor_groups: List[StoneGroup] = self._get_neighbor_groups_of_color(stone, stone.color.get_other())
        return list(filter(lambda group: not group.has_liberties(), neighbor_groups))
