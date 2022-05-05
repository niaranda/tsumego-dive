import os
from typing import List, Optional, Tuple

import dotenv
import numpy as np

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Stone, Pos
from src.beans.game_tree.game_node import GameNode, PathType
from src.beans.game_tree.game_tree import GameTree
from src.preprocessing.adapter.normalizer import Normalizer
from src.preprocessing.errors.preprocessing_exception import PreprocessingException


def truncate_csv_files():
    """Truncates csv files"""
    dotenv.load_dotenv(override=True)

    student_file = os.environ["PRE_STUDENT_FILE"]
    teacher_file = os.environ["PRE_TEACHER_FILE"]
    for file in [student_file, teacher_file]:
        if os.path.exists(file):
            mode = "w"
        else:
            mode = "x"
        with open(file, mode) as f:
            f.write("")


def generate_preprocessing_data(game_tree: GameTree, problem_id: int) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """Returns data collected from given game tree"""
    student_moves_data = __generate_data(None, game_tree.root, Color.BLACK, True)  # Cannot be None
    teacher_moves_data = __generate_data(None, game_tree.root, Color.WHITE, False)  # Can be None

    student_data = __add_problem_id_column(student_moves_data, problem_id)

    teacher_data = teacher_moves_data
    if teacher_moves_data is not None:
        teacher_data = __add_problem_id_column(teacher_moves_data, problem_id)

    return student_data, teacher_data


def __add_problem_id_column(moves_data: np.ndarray, problem_id: int) -> np.ndarray:
    problem_id_column = np.repeat(problem_id, moves_data.shape[0]).reshape(-1, 1)
    return np.hstack([moves_data, problem_id_column])


def __generate_data(data: Optional[np.ndarray], game_node: GameNode, color: Color, get_path_type: bool) -> np.ndarray:
    """Returns given color data by adding given game node data to first argument.
    If get_path_type is True, a path type column is generated"""
    if len(game_node.children) == 0:
        if color == Color.BLACK and data is None:  # If the first black node has no children, the game is empty
            raise PreprocessingException("Empty game")
        return data

    if game_node.children[0].stone.color == color:  # Check this node is from given color
        # Generate data and add to previous if not None
        if data is None:
            data = __get_data_from_game_node(game_node, get_path_type)
        else:
            data = np.vstack([data, __get_data_from_game_node(game_node, get_path_type)])

    # Get next valid paths and continue data generation
    next_paths = __filter_valid_paths(game_node.children)
    for path in next_paths:
        data = __generate_data(data, path, color, get_path_type)

    return data


def __get_data_from_game_node(game_node: GameNode, get_path_type: bool) -> np.ndarray:
    """Returns data from given game node. If get_path_type is True, a path type column is generated"""
    # Perform board normalization again
    # This is necessary because shape might change during the problem resolution
    normalizer = Normalizer(game_node.board)
    normalizer.normalize_board(game_node.board)

    board_data: np.ndarray = format_board_as_input(game_node.board)

    # Get valid moves data
    moves: List[Stone] = __get_valid_moves(game_node.children)
    normalized_moves: List[Stone] = [normalizer.normalize_stone(move) for move in moves]
    moves_data = np.array([__format_pos_as_input(stone.pos) for stone in normalized_moves]).reshape((-1, 1))

    # Repeat board data to create one row per move
    num_moves = len(moves_data)
    problem_data = np.tile(board_data, (num_moves, 1))

    if not get_path_type:
        return np.hstack([problem_data, moves_data])

    # Get path types data
    path_types: List[PathType] = __get_valid_moves_path_types(game_node.children)
    path_type_data = np.array([path_type == PathType.CORRECT for path_type in path_types]).reshape((-1, 1))
    return np.hstack([problem_data, moves_data, path_type_data])


def format_board_as_input(board: Board) -> np.ndarray:
    """Generates data from given board"""
    board_input = np.zeros(shape=(19, 19), dtype=int)  # empty board data
    for pos, color in board.placed_stones.items():
        board_input[pos] = int(color.value)  # add placed stones
    return board_input.flatten()


def __format_pos_as_input(position: Pos) -> int:
    """Formats given position as integer"""
    row, col = position
    return row * 19 + col


def __get_valid_moves(nodes: List[GameNode]) -> List[Stone]:
    """Returns valid moves from given list of nodes"""
    valid_paths = __filter_valid_paths(nodes)
    return [path.stone for path in valid_paths]


def __get_valid_moves_path_types(nodes: List[GameNode]) -> List[PathType]:
    """Returns list of path types of valid moves from given list of nodes"""
    valid_paths = __filter_valid_paths(nodes)
    return [path.path_type for path in valid_paths]


def __filter_valid_paths(nodes: List[GameNode]) -> List[GameNode]:
    """Filters valid paths from given list of nodes"""
    return list(filter(lambda child: child.is_valid(), nodes))
