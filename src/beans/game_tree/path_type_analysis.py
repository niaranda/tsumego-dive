from typing import List, Optional

from src.beans.game_tree.game_node import GameNode, PathType

CORRECT_CLUES = ["Correct", "Success", "正解"]
WRONG_CLUES = ["Wrong", "Incorrect", "Failure", "失败", "shi bai"]


def _perform_path_type_propagation(leaves: List[GameNode], path_type: PathType):
    # Propagates path type to all ancestors of given leaves
    nodes: List[GameNode] = __filter_by_path_type(leaves, path_type)
    for node in nodes:
        __propagate_path_type(node)


def _analyse_leaf_path_type(leaf: GameNode) -> PathType:
    correct, wrong = __has_correct_clue(leaf.comment), __has_wrong_clue(leaf.comment)

    if correct and wrong:
        return PathType.DUAL
    if wrong:
        return PathType.WRONG
    return PathType.CORRECT  # if no clue was found, the path is considered correct


def __has_correct_clue(comment: Optional[str]) -> bool:
    if not comment:
        return False
    return any([comment.lower().find(clue.lower()) != -1 for clue in CORRECT_CLUES])


def __has_wrong_clue(comment: Optional[str]) -> bool:
    if not comment:
        return False
    return any([comment.lower().find(clue.lower()) != -1 for clue in WRONG_CLUES])


def __filter_by_path_type(nodes: List[GameNode], path_type: PathType) -> List[GameNode]:
    return list(filter(lambda node: node.path_type == path_type, nodes))


def __propagate_path_type(node):
    if node.is_root():
        return
    parent = node.parent
    parent.path_type = node.path_type
    __propagate_path_type(parent)


class PathTypeAnalyser:

    @property
    def root(self) -> GameNode:
        pass

    def get_leaves(self) -> List[GameNode]:
        pass

    def _compute_path_types(self):
        """Analyses path types for given game tree"""
        leaves: List[GameNode] = self.get_leaves()

        for leaf in leaves:
            leaf.path_type = _analyse_leaf_path_type(leaf)

        # Propagate path types upwards in correct order
        for path_type in (PathType.DUAL, PathType.WRONG, PathType.CORRECT):
            _perform_path_type_propagation(leaves, path_type)

        if not self.root.is_correct():
            raise Exception("Path type analysis found no correct paths")
