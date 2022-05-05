import os
from multiprocessing import Lock
from typing import List, Dict

import numpy as np
import tensorflow
from keras.models import load_model, Model

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Stone
from src.preprocessing.adapter.normalizer import Normalizer
from src.preprocessing.data_generation.preprocessing_data_generation import format_board_as_input

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
DIVE_COUNTER_TOP_N = {0: 1, 1: 3, 2: 5, 3: 10}
mutex = Lock()


def predict(placed_stones: List[Stone], next_color: Color, dive_counter: int) -> Dict[int, str]:
    board = Board(placed_stones)

    normalizer = Normalizer(board, next_color)
    normalizer.normalize_board(board)

    board_data: np.ndarray = format_board_as_input(board).reshape(1, -1)

    model: Model = load_model("model/dense_model.h5")

    with mutex:
        probabilities: np.ndarray = model.predict(board_data)[0]

    n_top: int = __get_n_top(dive_counter)
    n_top_indexes: np.ndarray = np.flip(probabilities.argsort())[:n_top]

    n_top_probabilities: np.ndarray = probabilities[n_top_indexes]
    n_top_prob_sum1: np.ndarray = n_top_probabilities / n_top_probabilities.sum()

    n_top_index_list: List[int] = list([int(index) for index in n_top_indexes])
    n_top_prob_list: List[float] = list(np.round(n_top_prob_sum1, decimals=2))
    n_top_prob_list_str: List[str] = [str(prob) for prob in n_top_prob_list]

    return dict(zip(n_top_index_list, n_top_prob_list_str))


def __get_n_top(dive_counter: int) -> int:
    if dive_counter not in DIVE_COUNTER_TOP_N.keys():
        return max(DIVE_COUNTER_TOP_N.values())
    return DIVE_COUNTER_TOP_N[dive_counter]
