import sgf


def process_problem(problem_name: str):
    """Processes one tsumego problem"""
    problem = __parse_problem(problem_name)


def __parse_problem(problem_path: str) -> sgf.GameTree:
    """Parses problem in given path"""
    with open(problem_path, encoding="GB2312", errors="ignore") as file:
        return sgf.parse(file.read()).children[0]  # only one problem per file
