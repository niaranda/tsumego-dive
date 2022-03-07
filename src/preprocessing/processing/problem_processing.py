from typing import Optional, Tuple

import numpy as np
import sgf

from src.beans.game_tree.game_tree import GameTree
from src.beans.gameplay_exception import GamePlayException
from src.preprocessing.errors.error_handling import log_error
from src.preprocessing.data_generation.input_data_generation import generate_input_data
from src.preprocessing.errors.preprocessing_exception import PreprocessingException
from src.preprocessing.corrections.sgf_corrections import apply_corrections
from src.preprocessing.adapter.tree_adapter import TreeAdapter


def process_problem(problem_path: str) -> Optional[Tuple[np.ndarray, Optional[np.ndarray]]]:
    """Returns result of processing one tsumego problem in given path"""
    print(problem_path)
    problem: Optional[sgf.GameTree] = __parse_problem(problem_path)

    if problem is None:  # The problem has incorrect format
        return None

    try:
        # Perform tree adaptation
        game_tree: GameTree = TreeAdapter(problem).parse_tree()

        # Generate data from tree
        return generate_input_data(game_tree)

    except (GamePlayException, PreprocessingException) as e:
        log_error(e, problem_path)
        return None


def __parse_problem(problem_path: str) -> Optional[sgf.GameTree]:
    """Parses problem in given path"""
    with open(problem_path, encoding="GB2312", errors="ignore") as file:
        try:
            # Apply pre sgf parsing corrections
            sgf_str: str = apply_corrections(file.read())

            # Parse corrected string
            return sgf.parse(sgf_str).children[0]  # there is only one problem per file

        except (UnicodeDecodeError, sgf.ParseException, PreprocessingException) as e:
            log_error(e, problem_path)
            return None
