from typing import List, Tuple, Optional

import numpy as np

from src.beans.board.board_point import BoardPoint
from src.beans.board.stone import Stone
from src.beans.board.stone_capture_handler import StoneCaptureHandler

Pos = Tuple[int, int]


class Board(StoneCaptureHandler):
    """Represents a Go board"""

    def __init__(self, stones: Optional[List[Stone]] = None):
        """Creates a new Go board, optionally with a list of initial stones placed on it"""
        super().__init__()

        # Initialize grid of board points
        self.__grid = np.empty((19, 19), dtype=BoardPoint)
        for index, _ in np.ndenumerate(self.__grid):
            self.__grid[index] = BoardPoint(index)

        # Place initial stones
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
        """Returns list of all stones placed in the board"""
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
        point = self._get_point(stone.pos)
        point.stone = stone

        # compute liberties and remove one liberty from neighbor stones
        self._compute_liberties(stone)
        self._update_neighbor_liberties([stone], -1)

        # Perform group capture
        self._capture_groups(stone)

        # Add stone to new group
        self._add_stone_to_groups(stone)

    def _get_point(self, pos: Pos) -> BoardPoint:
        return self.__grid[pos]

    def _remove_stones(self, stones):
        board_points: List[BoardPoint] = [self._get_point(stone.pos) for stone in stones]
        for point in board_points:
            point.remove_stone()
