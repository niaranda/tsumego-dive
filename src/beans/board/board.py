from typing import List, Tuple, Optional

import numpy as np

from src.beans.board.board_point import BoardPoint
from src.beans.board.stone import Stone

Pos = Tuple[int, int]


class Board:
    """Represents a Go board"""

    def __init__(self, stones: Optional[List[Stone]] = None):
        self.__grid = np.empty((19, 19), dtype=BoardPoint)
        for index, _ in np.ndenumerate(self.__grid):
            self.__grid[index] = BoardPoint(index)
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

    def __get_point(self, pos: Pos) -> BoardPoint:
        return self.__grid[pos]
