from typing import Optional

import sgf

from src.preprocessing.error_handling import log_error


def process_problem(problem_name: str):
    """Processes one tsumego problem"""
    problem = __parse_problem(problem_name)


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
