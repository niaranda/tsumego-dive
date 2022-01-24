from typing import List

from src.beans.game_tree.game_node import GameNode, PathType
from src.beans.game_tree.game_tree import GameTree

CORRECT_CLUES = ["Correct", "Success", "正解"]
WRONG_CLUES = ["Wrong", "Incorrect", "Failure", "失败", "shi bai"]


def compute_path_types(game_tree: GameTree):
    leaves: List[GameNode] = game_tree.get_leaves()

    for leaf in leaves:
        leaf.path_type = __analyse_leaf_path_type(leaf)

    for path_type in (PathType.DUAL, PathType.WRONG, PathType.CORRECT):
        __perform_path_type_propagation(leaves, path_type)

    if not game_tree.root.is_correct():
        raise Exception()


def __analyse_leaf_path_type(leaf: GameNode) -> PathType:
    correct, wrong = __has_correct_clue(leaf.comment), __has_wrong_clue(leaf.comment)

    if not correct and not wrong:
        return PathType.UNKNOWN
    if correct and wrong:
        return PathType.DUAL
    if correct:
        return PathType.CORRECT
    return PathType.WRONG


def __has_correct_clue(comment: str) -> bool:
    return any([comment.find(clue) != -1 for clue in CORRECT_CLUES])


def __has_wrong_clue(comment: str) -> bool:
    return any([comment.find(clue) != -1 for clue in WRONG_CLUES])


def __perform_path_type_propagation(leaves: List[GameNode], path_type: PathType):
    nodes: List[GameNode] = __filter_by_path_type(leaves, path_type)
    while nodes:
        for node in nodes:
            node.path_type = path_type
            if not node.is_root():
                nodes.append(node.parent)


def __filter_by_path_type(nodes: List[GameNode], path_type: PathType) -> List[GameNode]:
    return list(filter(lambda node: node.path_type == path_type, nodes))
