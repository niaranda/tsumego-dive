from __future__ import annotations

from typing import List, Tuple, Optional, Dict

from src.beans.board.color import Color
from src.beans.board.stone_capture_handler import StoneCaptureHandler

Pos = Tuple[int, int]
Stone = Tuple[Pos, Color]


class Board(StoneCaptureHandler):
    """Represents a Go board"""

    def __init__(self, unplaced_stones: Optional[List[Stone]] = None):
        """Creates a new Go board, optionally with a list of initial stones placed on it"""
        super().__init__()

        self.__placed_stones: Dict[Pos, Color] = {}

        # Place initial stones
        if unplaced_stones:
            self.place_stones(unplaced_stones)

    @property
    def placed_stones(self) -> Dict[Pos, Color]:
        return self.__placed_stones

    def get_placed_stone_positions(self) -> List[Pos]:
        return list(self.__placed_stones.keys())

    def place_stones(self, stones: List[Stone]):
        """Places a list of stones in the board"""
        for stone in stones:
            self.place_stone(stone)

    def place_stone(self, stone: Stone):
        """Places a stone in the board"""
        pos, color = stone
        self.__placed_stones[pos] = color

        # compute liberties and remove one liberty from neighbor stones
        self._compute_liberties(pos)
        self._remove_liberty_from_neighbors([pos])

        # Perform group capture
        self._capture_groups(stone)

        # Add stone to new group
        self._add_stone_to_groups(stone)

    def _remove_stones(self, positions: List[Pos]):
        for pos in positions:
            del self.__placed_stones[pos]
