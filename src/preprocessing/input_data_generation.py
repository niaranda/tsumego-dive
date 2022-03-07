import os
from typing import List, Optional, Tuple

import dotenv
import numpy as np

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Stone, Pos
from src.beans.game_tree.game_node import GameNode, PathType
from src.beans.game_tree.game_tree import GameTree
from src.preprocessing.preprocessing_exception import PreprocessingException


def truncate_csv_files():
    dotenv.load_dotenv(override=True)

    black_file = os.environ["BLACK_FILE"]
    white_file = os.environ["WHITE_FILE"]
    for file in [black_file, white_file]:
        if os.path.exists(file):
            mode = "w"
        else:
            mode = "x"
        with open(file, mode) as f:
            f.write("")


def generate_input_data(game_tree: GameTree) -> Tuple[np.ndarray, np.ndarray]:
    black_moves_data = __generate_data(None, game_tree.root, Color.BLACK, True)
    white_moves_data = __generate_data(None, game_tree.root, Color.WHITE, False)

    return black_moves_data, white_moves_data


def __generate_data(data: Optional[np.ndarray], game_node: GameNode, color: Color, get_path_type: bool) -> np.ndarray:
    if len(game_node.children) == 0:
        if color == Color.BLACK and data is None:
            raise PreprocessingException("Empty game")
        return data
    if game_node.children[0].stone.color == color:
        if data is None:
            data = __get_data_from_game_node(game_node, get_path_type)
        else:
            data = np.vstack([data, __get_data_from_game_node(game_node, get_path_type)])

    next_paths = __filter_valid_paths(game_node.children)
    for path in next_paths:
        data = __generate_data(data, path, color, get_path_type)
    return data


def __get_data_from_game_node(game_node: GameNode, get_path_type: bool) -> np.ndarray:
    board_data: np.ndarray = __format_board_as_input(game_node.board)

    moves: List[Stone] = __get_valid_moves(game_node.children)
    moves_data = np.array([__format_pos_as_input(stone.pos) for stone in moves]).reshape((-1, 1))

    num_moves = len(moves_data)
    problem_data = np.repeat(board_data, num_moves).reshape((num_moves, -1))

    if not get_path_type:
        return np.hstack([problem_data, moves_data])

    path_types: List[PathType] = __get_valid_moves_path_types(game_node.children)
    path_type_data = np.array([path_type == PathType.CORRECT for path_type in path_types]).reshape((-1, 1))
    return np.hstack([problem_data, moves_data, path_type_data])


def __format_board_as_input(board: Board) -> np.ndarray:
    board_input = np.zeros(shape=(19, 19), dtype=int)
    for pos, color in board.placed_stones.items():
        board_input[pos] = int(color.value)
    return board_input.flatten()


def __format_pos_as_input(position: Pos) -> int:
    row, col = position
    return row * 19 + col


def __get_valid_moves(children: List[GameNode]) -> List[Stone]:
    valid_paths = __filter_valid_paths(children)
    return [path.stone for path in valid_paths]


def __get_valid_moves_path_types(children: List[GameNode]) -> List[PathType]:
    valid_paths = __filter_valid_paths(children)
    return [path.path_type for path in valid_paths]


def __filter_valid_paths(children: List[GameNode]) -> List[GameNode]:
    return list(filter(lambda child: child.is_valid(), children))
