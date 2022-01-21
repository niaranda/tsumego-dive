from typing import Optional

import sgf

from src.beans.game_tree.game_tree import GameTree
from src.preprocessing.sgf_tree_parsing import parse_sgf_tree
from src.preprocessing.error_handling import log_error


def process_problem(problem_name: str):
    """Processes one tsumego problem"""
    problem: Optional[sgf.GameTree] = __parse_problem(problem_name)
    if problem is None:
        return

    game_tree: GameTree = parse_sgf_tree(problem)

    # TODO


def __parse_problem(problem_path: str) -> Optional[sgf.GameTree]:
    """Parses problem in given path"""
    with open(problem_path, encoding="GB2312", errors="ignore") as file:
        try:
            return sgf.parse(file.read()).children[0]  # only one problem per file
        except UnicodeDecodeError as e:
            log_error(e, problem_path)
            return None
        except sgf.ParseException as e:
            log_error(e, problem_path)
            return None
