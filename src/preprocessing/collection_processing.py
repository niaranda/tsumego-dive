import os
from typing import List, Tuple

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
    dotenv.load_dotenv(override=True)

    with open(os.environ["BLACK_FILE"], "a") as f:
        f.write(pd.DataFrame(black_moves).to_csv(header=False))

    with open(os.environ["WHITE_FILE"], "a") as f:
        f.write(pd.DataFrame(white_moves).to_csv(header=False))


def __process_problems(problem_paths: List[str]) -> Tuple[np.ndarray, np.ndarray]:
    black_moves, white_moves = None, None

    for problem_path in problem_paths:
        if not __is_valid(problem_path):
            continue

        problem_result = process_problem(problem_path)
        if problem_result is None:
            continue

        if black_moves is None:
            black_moves, white_moves = problem_result
            continue

        black_moves = np.vstack([black_moves, problem_result[0]])
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
    return "skip" not in problem_path and ".sgf" in problem_path
