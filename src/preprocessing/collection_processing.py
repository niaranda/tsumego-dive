import os
from typing import List

from problem_processing import process_problem


def process_collection(collection_path: str):
    """Processes a tsumego collection in given path"""
    problem_paths = __get_problem_paths(collection_path)
    for problem_path in problem_paths:
        process_problem(problem_path)


def __get_problem_paths(collection_path: str) -> List[str]:
    """Gets list of paths to problems contained in given collection path"""
    problem_paths = []
    for root, dirs, files in os.walk(f"../../raw_data/{collection_path}"):
        for name in files:
            problem_paths.append(os.path.join(root, name))
    return problem_paths
