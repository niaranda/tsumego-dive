from typing import List, Tuple

import numpy as np
from keras.models import load_model, Model

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Stone
from src.preprocessing.adapter.normalizer import Normalizer
from src.preprocessing.data_generation.preprocessing_data_generation import format_board_as_input

model: Model = load_model("app/model/dense_model.h5")

DIVE_COUNTER_TOP_N = {0: 1, 1: 3, 2: 5, 3: 10}


def predict(placed_stones: List[Stone], next_color: Color, dive_counter: int) -> Tuple[List[int], List[float]]:
    board = Board(placed_stones)

    normalizer = Normalizer(board, next_color)
    normalizer.normalize_board(board)

    board_data: np.ndarray = format_board_as_input(board).reshape(1, -1)
    probabilities: np.ndarray = model.predict(board_data)[0]

    n_top: int = __get_n_top(dive_counter)
    n_top_indexes = np.flip(probabilities.argsort())[:n_top]

    n_top_probabilities: np.ndarray = probabilities[n_top_indexes]
    n_top_prob_sum1: np.ndarray = n_top_probabilities / n_top_probabilities.sum()

    return n_top_indexes, np.round(n_top_prob_sum1, decimals=2)


def __get_n_top(dive_counter: int) -> int:
    if dive_counter not in DIVE_COUNTER_TOP_N.keys():
        return max(DIVE_COUNTER_TOP_N.values())
    return DIVE_COUNTER_TOP_N[dive_counter]
