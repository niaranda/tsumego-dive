import os
from typing import List, Optional, Tuple

import dotenv
import numpy as np

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Stone, Pos
from src.beans.game_tree.game_node import GameNode
from src.beans.game_tree.game_tree import GameTree
from src.preprocessing.preprocessing_exception import PreprocessingException


def truncate_csv_files():
    dotenv.load_dotenv()

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


def __generate_data(data: Optional[np.ndarray], game_node: GameNode, color: Color, filter_correct: bool) -> np.ndarray:
    if len(game_node.children) == 0:
        if data is None:
            raise PreprocessingException("Empty game")
        return data
    if game_node.children[0].stone.color == color:
        if data is None:
            data = __get_data_from_game_node(game_node, filter_correct)
        else:
            data = np.vstack([data, __get_data_from_game_node(game_node, filter_correct)])

    if filter_correct:
        next_paths = __filter_correct_paths(game_node.children)
    else:
        next_paths = __filter_valid_paths(game_node.children)
    for path in next_paths:
        data = __generate_data(data, path, color, filter_correct)
    return data


def __get_data_from_game_node(game_node: GameNode, filter_correct: bool) -> np.ndarray:
    board_data: np.ndarray = __format_board_as_input(game_node.board)

    if filter_correct:
        moves: List[Stone] = __get_correct_moves(game_node.children)
    else:
        moves: List[Stone] = __get_valid_moves(game_node.children)

    moves_data = np.array([__format_pos_as_input(stone.pos) for stone in moves]).reshape((-1, 1))

    num_moves = len(moves_data)
    problem_data = np.repeat(board_data, num_moves).reshape((num_moves, -1))

    return np.hstack([problem_data, moves_data])


def __format_board_as_input(board: Board) -> np.ndarray:
    board_input = np.zeros(shape=(19, 19), dtype=int)
    for pos, color in board.placed_stones.items():
        board_input[pos] = int(color.value)
    return board_input.flatten()


def __format_pos_as_input(position: Pos) -> int:
    row, col = position
    return row * 19 + col


def __get_correct_moves(children: List[GameNode]) -> List[Stone]:
    correct_paths = __filter_correct_paths(children)
    return [path.stone for path in correct_paths]


def __get_valid_moves(children: List[GameNode]) -> List[Stone]:
    valid_paths = __filter_valid_paths(children)
    return [path.stone for path in valid_paths]


def __filter_correct_paths(children: List[GameNode]) -> List[GameNode]:
    return list(filter(lambda child: child.is_correct(), children))


def __filter_valid_paths(children: List[GameNode]) -> List[GameNode]:
    return list(filter(lambda child: child.is_valid(), children))
