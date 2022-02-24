from typing import List, Dict

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Pos, Stone

CORNERS = [(0, 0), (0, 18), (18, 18), (18, 0)]
BORDERS = [(0, 9), (9, 18), (18, 9), (9, 0)]


def __get_distance(pos1: Pos, pos2: Pos) -> int:
    row1, col1 = pos1
    row2, col2 = pos2
    return (row1 - row2) ** 2 + (col1 - col2) ** 2


def __get_closer_reference(position: Pos, references: List[Pos]) -> Pos:
    distances: List[int] = [__get_distance(position, reference) for reference in references]
    return references[distances.index(min(distances))]


def __get_main_reference(board: Board, references: List[Pos]) -> Pos:
    positions: List[Pos] = list(board.placed_stones.keys())
    closer_corners = [__get_closer_reference(pos, references) for pos in positions]
    counts = [closer_corners.count(corner) for corner in references]
    return references[counts.index(max(counts))]


def _determine_color_inversion(first_stone: Stone) -> bool:
    return first_stone.color == Color.WHITE


def _determine_board_rotations(init_board: Board) -> int:
    main_corner = __get_main_reference(init_board, CORNERS)
    return CORNERS.index(main_corner)


def _determine_board_reflexion(init_board: Board) -> bool:
    main_corner = __get_main_reference(init_board, CORNERS)
    main_border = __get_main_reference(init_board, BORDERS)
    corner_index, border_index = CORNERS.index(main_corner), BORDERS.index(main_border)
    return corner_index != border_index


def _perform_stone_color_inversion(stone: Stone) -> Stone:
    return Stone(stone.pos, stone.color.get_other())


def _perform_stone_rotation(stone: Stone) -> Stone:
    return Stone(_perform_pos_rotation(stone.pos), stone.color)


def _perform_pos_rotation(pos: Pos) -> Pos:
    row, col = pos
    trans_row, trans_col = row - 9, col - 9
    rot_trans_row, rot_trans_col = -trans_col, trans_row
    return rot_trans_row + 9, rot_trans_col + 9


def _perform_stone_reflection(stone: Stone) -> Stone:
    return Stone(_perform_pos_reflection(stone.pos), stone.color)


def _perform_pos_reflection(pos: Pos) -> Pos:
    row, col = pos
    return col, row


def _perform_board_color_inversion(board: Board):
    for pos, color in board.placed_stones.items():
        board.placed_stones[pos] = color.get_other()
    for group in board.stone_groups:
        group.inverse_color()


def _perform_board_rotation(board: Board):
    new_placed_stones = {}
    for pos, color in board.placed_stones.items():
        new_placed_stones[_perform_pos_rotation(pos)] = color
    board.placed_stones = new_placed_stones

    stone_liberties: Dict[Pos, int] = {}
    for pos, count in board.stone_liberties.items():
        stone_liberties[_perform_pos_rotation(pos)] = count
    board.stone_liberties = stone_liberties

    for group in board.stone_groups:
        positions = group.positions
        group.positions = [_perform_pos_rotation(pos) for pos in positions]


def _perform_board_reflexion(board: Board):
    new_placed_stones = {}
    for pos, color in board.placed_stones.items():
        new_placed_stones[_perform_pos_reflection(pos)] = color
    board.placed_stones = new_placed_stones

    stone_liberties: Dict[Pos, int] = {}
    for pos, count in board.stone_liberties.items():
        stone_liberties[_perform_pos_reflection(pos)] = count
    board.stone_liberties = stone_liberties

    for group in board.stone_groups:
        positions = group.positions
        group.positions = [_perform_pos_reflection(pos) for pos in positions]


class Normalizer:
    def __init__(self, init_board: Board, first_stone: Stone):
        self.__color_inversion: bool = _determine_color_inversion(first_stone)
        self.__board_rotations: int = _determine_board_rotations(init_board)
        self.__board_reflection: bool = _determine_board_reflexion(init_board)

    def normalize_stone(self, stone: Stone) -> Stone:
        new_stone = stone
        if self.__color_inversion:
            new_stone = _perform_stone_color_inversion(stone)
        for _ in range(self.__board_rotations):
            new_stone = _perform_stone_rotation(new_stone)
        if self.__board_reflection:
            new_stone = _perform_stone_reflection(new_stone)
        return new_stone

    def normalize_board(self, board: Board):
        if self.__color_inversion:
            _perform_board_color_inversion(board)
        for _ in range(self.__board_rotations):
            _perform_board_rotation(board)
        if self.__board_reflection:
            _perform_board_reflexion(board)
