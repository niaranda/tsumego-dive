from typing import List, Tuple

import numpy as np

from src.beans.board.board_point import BoardPoint
from src.beans.board.stone import Color, Stone

Pos = Tuple[int, int]


class Board:
    """Represents a Go board"""

    def __init__(self):
        self.__grid = np.empty((19, 19), dtype=BoardPoint)
        for index, _ in np.ndenumerate(self.__grid):
            self.__grid[index] = BoardPoint(index)

    def get_stones(self) -> List[Stone]:
        stones: List[Stone] = []
        board_point: BoardPoint
        for _, board_point in np.ndenumerate(self.__grid):
            if not board_point.is_empty():
                stones.append(board_point.stone)
        return stones

    def place_stones(self, positions: List[Pos], color: Color):
        """Places a stone in the board"""
        for pos in positions:
            point = self.__get_board_point(pos)
            point.place_stone(color)

    def __get_board_point(self, pos: Pos) -> BoardPoint:
        return self.__grid[pos]
