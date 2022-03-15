import os
from typing import List, Tuple, Optional

import dotenv
import numpy as np
import pandas as pd

from src.preprocessing.processing.problem_processing import process_problem


def process_collection(collection_path: str, collection_number: int):
    """Processes a tsumego collection in given path"""
    problem_paths = __get_problem_paths(collection_path)

    student_moves, teacher_moves = __process_problems(problem_paths, collection_number)

    __save_to_csv(student_moves, teacher_moves)


def __save_to_csv(student_moves: np.ndarray, teacher_moves: np.ndarray):
    """Saves given data to csv files"""
    dotenv.load_dotenv(override=True)

    with open(os.environ["PRE_STUDENT_FILE"], "a") as f:
        f.write(pd.DataFrame(student_moves).to_csv(header=False, index=False, line_terminator="\n"))

    with open(os.environ["PRE_TEACHER_FILE"], "a") as f:
        f.write(pd.DataFrame(teacher_moves).to_csv(header=False, index=False, line_terminator="\n"))



def __process_problems(problem_paths: List[str], collection_number: int) -> Tuple[np.ndarray, np.ndarray]:
    """Returns data obtained by processing problems in given paths"""
    student_moves, teacher_moves = None, None

    num_problems = len(problem_paths)

    for problem_number in range(num_problems):
        problem_id: int = __generate_problem_id(collection_number, problem_number)

        problem_path = problem_paths[problem_number]

        if not __is_valid(problem_path):  # Validate path
            continue

        problem_result: Optional[Tuple[np.ndarray, Optional[np.ndarray]]] = process_problem(problem_path, problem_id)
        if problem_result is None:  # the problem had an irresolvable error
            continue

        if student_moves is None:  # first problem
            student_moves, teacher_moves = problem_result
            continue

        student_moves = np.vstack([student_moves, problem_result[0]])

        if teacher_moves is None:  # white moves can be None if there were no white moves in previous problems
            teacher_moves = problem_result[1]
            continue

        if problem_result[1] is not None:  # if this problem has white moves
            teacher_moves = np.vstack([teacher_moves, problem_result[1]])

    return student_moves, teacher_moves


def __generate_problem_id(collection_number: int, problem_number: int) -> int:
    return collection_number * 10000 + problem_number


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
