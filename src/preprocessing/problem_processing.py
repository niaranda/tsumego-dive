from typing import Optional, Tuple

import numpy as np
import sgf

from src.beans.game_tree.game_tree import GameTree
from src.beans.gameplay_exception import GamePlayException
from src.preprocessing.error_handling import log_error
from src.preprocessing.input_data_generation import generate_input_data
from src.preprocessing.preprocessing_exception import PreprocessingException
from src.preprocessing.sgf_corrections import apply_corrections
from src.preprocessing.sgf_tree_parser import SgfTreeParser


def process_problem(problem_name: str) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """Processes one tsumego problem"""
    print(problem_name)
    problem: Optional[sgf.GameTree] = __parse_problem(problem_name)
    if problem is None:
        return None

    try:
        game_tree: GameTree = SgfTreeParser(problem).parse_tree()
        return generate_input_data(game_tree)

    except (GamePlayException, PreprocessingException) as e:
        log_error(e, problem_name)
        return None


def __parse_problem(problem_path: str) -> Optional[sgf.GameTree]:
    """Parses problem in given path"""
    with open(problem_path, encoding="GB2312", errors="ignore") as file:
        try:
            sgf_str: str = apply_corrections(file.read())
            return sgf.parse(sgf_str).children[0]  # only one problem per file
        except UnicodeDecodeError as e:
            log_error(e, problem_path)
            return None
        except sgf.ParseException as e:
            log_error(e, problem_path)
            return None
