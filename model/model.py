import os
from typing import List

import numpy as np
from keras.models import load_model, Model

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Stone, Pos
from src.preprocessing.adapter.normalizer import Normalizer
from src.preprocessing.data_generation.preprocessing_data_generation import format_board_as_input

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
DIVE_COUNTER_TOP_N = {0: 1, 1: 3, 2: 5, 3: 10}

model: Model = load_model("model/cnn_model.h5")


def predict(placed_stones: List[Stone], next_color: Color, dive_counter: int) -> List[int]:
    board = Board(placed_stones)

    normalizer = Normalizer(board, next_color)
    normalizer.normalize_board(board)

    board_data: np.ndarray = format_board_as_input(board).reshape(1, 19, 19, 1).astype("float")

    probabilities: np.ndarray = model.predict(board_data)[0]

    forbidden_moves: List[Pos] = board.get_forbidden_moves(next_color)
    forbidden_indexes: List[int] = [row * 19 + col for row, col in forbidden_moves]

    n_top: int = __get_n_top(dive_counter)
    sorted_indexes: np.ndarray = np.flip(probabilities.argsort())

    sorted_valid_indexes: np.ndarray = sorted_indexes[~np.isin(sorted_indexes, forbidden_indexes)]

    n_top_indexes: np.ndarray = sorted_valid_indexes[:n_top]

    n_top_index_list: List[int] = list([int(index) for index in n_top_indexes])
    n_top_index_list: List[int] = __denormalize_indexes(n_top_index_list, normalizer)

    return n_top_index_list


def __get_n_top(dive_counter: int) -> int:
    if dive_counter not in DIVE_COUNTER_TOP_N.keys():
        return max(DIVE_COUNTER_TOP_N.values())
    return DIVE_COUNTER_TOP_N[dive_counter]


def __denormalize_indexes(indexes: List[int], normalizer: Normalizer) -> List[int]:
    positions: List[Pos] = [(int(index / 19), index % 19) for index in indexes]
    denorm_positions: List[Pos] = normalizer.denormalize_positions(positions)

    return [row * 19 + col for row, col in denorm_positions]
