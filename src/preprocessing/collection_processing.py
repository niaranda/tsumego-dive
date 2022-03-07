import os
from typing import List, Tuple, Optional

import dotenv
import numpy as np
import pandas as pd

from problem_processing import process_problem


def process_collection(collection_path: str):
    """Processes a tsumego collection in given path"""
    problem_paths = __get_problem_paths(collection_path)
    black_moves, white_moves = __process_problems(problem_paths)

    __save_to_csv(black_moves, white_moves)


def __save_to_csv(black_moves: np.ndarray, white_moves: np.ndarray):
    """Saves given data to csv files"""
    dotenv.load_dotenv(override=True)

    with open(os.environ["BLACK_FILE"], "a") as f:
        f.write(pd.DataFrame(black_moves).to_csv(header=False, index=False, line_terminator="\n"))

    with open(os.environ["WHITE_FILE"], "a") as f:
        f.write(pd.DataFrame(white_moves).to_csv(header=False, index=False, line_terminator="\n"))


def __process_problems(problem_paths: List[str]) -> Tuple[np.ndarray, np.ndarray]:
    """Returns data obtained by processing problems in given paths"""
    black_moves, white_moves = None, None

    for problem_path in problem_paths:
        if not __is_valid(problem_path):  # Validate path
            continue

        problem_result: Optional[Tuple[np.ndarray, Optional[np.ndarray]]] = process_problem(problem_path)
        if problem_result is None:  # the problem had an irresolvable error
            continue

        if black_moves is None:  # first problem
            black_moves, white_moves = problem_result
            continue

        black_moves = np.vstack([black_moves, problem_result[0]])

        if white_moves is None:  # white moves can be None if there were no white moves in previous problems
            white_moves = problem_result[1]
            continue

        if problem_result[1] is not None:  # if this problem has white moves
            white_moves = np.vstack([white_moves, problem_result[1]])

    return black_moves, white_moves


def __get_problem_paths(collection_path: str) -> List[str]:
    """Gets list of paths to problems contained in given collection path"""
    problem_paths = []
    for root, dirs, files in os.walk(f"../../raw_data/{collection_path}"):
        for name in files:
            problem_paths.append(os.path.join(root, name))
    return problem_paths


def __is_valid(problem_path: str) -> bool:
    """Checks if given problem path is valid"""
    return "skip" not in problem_path and ".sgf" in problem_path.lower()
