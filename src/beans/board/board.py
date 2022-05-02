from __future__ import annotations

from copy import copy, deepcopy
from typing import List, Optional, Dict

from src.beans.board.color import Color
from src.beans.board.stone import Stone, Pos
from src.beans.board.stone_capture_handler import StoneCaptureHandler
from src.beans.board.stone_group import StoneGroup
from src.beans.gameplay_exception import GamePlayException


class Board(StoneCaptureHandler):
    """Represents a Go board"""

    def __init__(self, unplaced_stones: Optional[List[Stone]] = None):
        """Creates a new Go board, optionally with a list of initial stones placed on it"""
        self.__placed_stones: Dict[Pos, Color] = {}

        # Place initial stones
        if unplaced_stones:
            for pos, color in unplaced_stones:
                self.__placed_stones[pos] = color

        super().__init__(unplaced_stones)

    def __eq__(self, other: Board) -> bool:
        return self.__placed_stones == other.placed_stones

    def __deepcopy__(self, memodict={}) -> Board:
        new_board = Board()
        new_board.placed_stones = copy(self.__placed_stones)
        new_board.stone_groups = deepcopy(self.stone_groups)
        new_board.stone_liberties = copy(self.stone_liberties)
        return new_board

    @property
    def placed_stones(self) -> Dict[Pos, Color]:
        return self.__placed_stones

    @placed_stones.setter
    def placed_stones(self, stones: Dict[Pos, Color]):
        self.__placed_stones = stones

    def place_stones(self, stones: List[Stone]):
        """Places a list of stones in the board"""
        for stone in stones:
            self.place_stone(stone)

    def place_stone(self, stone: Stone):
        """Places a stone in the board"""
        pos, color = stone

        if pos in self.__placed_stones:
            raise GamePlayException(f"Adding {color} stone to position {pos} already containing a stone")

        self.__placed_stones[pos] = color

        # compute liberties and remove one liberty from neighbor stones
        self._compute_liberties(pos)
        self._remove_liberty_from_neighbors([pos])

        # Add stone to new group
        self._add_stone_to_groups(stone)

        # Perform group capture
        self._capture_groups(stone)

        # Check suicide rule
        if self.__stone_suicided(pos):
            raise GamePlayException(f"Broke suicide rule when placing stone in {pos}")

    def get_forbidden_moves(self, color: Color) -> List[Pos]:
        all_moves: List[Stone] = [Stone((row, col), color) for row in range(19) for col in range(19)]
        forbidden_moves: List[Stone] = list(filter(lambda move: self.__is_forbidden_move(move), all_moves))
        return [move.pos for move in forbidden_moves]

    def _remove_stones(self, positions: List[Pos]):
        """Removes stones from the board. Overrides StoneCaptureHandler method"""
        for pos in positions:
            del self.__placed_stones[pos]

    def _get_neighbor_stone_positions(self, position: Pos) -> List[Pos]:
        """Returns list of neighbor positions containing stones. Overrides StoneLibertiesHandler method"""
        neighbor_positions = self._get_neighbor_positions(position)
        return list(filter(lambda pos: pos in neighbor_positions, self._get_placed_stone_positions()))

    def _get_neighbor_positions(self, position: Pos) -> List[Pos]:
        """Returns list of neighbor positions. Overrides StoneLibertiesHandler method"""
        row, col = position
        positions: List[Pos] = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        return list(filter(lambda pos: 0 <= pos[0] <= 18 and 0 <= pos[1] <= 18, positions))

    def __stone_suicided(self, position: Pos) -> bool:
        """True if the stone placed in position committed suicide"""
        container_group: StoneGroup = self._get_group_containing(position)
        return not self._has_liberties(container_group)

    def _get_placed_stone_positions(self) -> List[Pos]:
        """Returns list of occupied positions. Overrides StoneLibertiesHandler method"""
        return list(self.__placed_stones.keys())

    def __is_forbidden_move(self, move: Stone) -> bool:
        # Not empty
        if move.pos in self.placed_stones:
            return True

        # Has liberties
        if self._compute_liberties(move.pos) != 0:
            return False

        # Check suicide rule
        dummy_board = deepcopy(self)
        try:
            dummy_board.place_stone(move)
            return False
        except Exception:
            return True
