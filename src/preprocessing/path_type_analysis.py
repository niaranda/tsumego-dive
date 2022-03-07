import json
from typing import List, Optional

import dotenv
from dotenv import dotenv_values

from src.beans.game_tree.game_node import GameNode, PathType
from src.preprocessing.preprocessing_exception import PreprocessingException

CORRECT_CLUES = json.loads(dotenv_values()["CORRECT_CLUES"])
WRONG_CLUES = json.loads(dotenv_values()["WRONG_CLUES"])


def _perform_path_type_propagation(leaves: List[GameNode], path_type: PathType):
    """Propagates given path type to all ancestors of given leaves"""
    nodes: List[GameNode] = __filter_by_path_type(leaves, path_type)
    for node in nodes:
        __propagate_path_type(node)


def _analyse_leaf_path_type(leaf: GameNode) -> PathType:
    """Returns path type after analysing given leaf node"""
    # Check for clues in comment
    correct, wrong = __has_correct_clue(leaf.comment), __has_wrong_clue(leaf.comment)

    # Get environment value for default type
    dotenv.load_dotenv(override=True)
    default_wrong = dotenv_values()["DEFAULT_WRONG"] == "True"

    if correct and wrong:  # Found both clues
        return PathType.DUAL

    if correct:  # Found correct
        return PathType.CORRECT

    if wrong:  # Found wrong
        return PathType.WRONG

    # No clue was found
    if default_wrong:
        return PathType.WRONG  # Default is wrong

    return PathType.CORRECT  # Default is correct


def __has_correct_clue(comment: str) -> bool:
    """True if correct clue found in given comment"""
    return any([comment.lower().find(clue.lower()) != -1 for clue in CORRECT_CLUES])


def __has_wrong_clue(comment: str) -> bool:
    """True if wrong clue found in given comment"""
    return any([comment.lower().find(clue.lower()) != -1 for clue in WRONG_CLUES])


def __filter_by_path_type(nodes: List[GameNode], path_type: PathType) -> List[GameNode]:
    """Returns list of nodes from given nodes filtered by given path type"""
    return list(filter(lambda node: node.path_type == path_type, nodes))


def __propagate_path_type(node):
    """Propagates the path type of given node to all its ancestors"""
    if node.is_root():
        return
    parent = node.parent
    parent.path_type = node.path_type
    __propagate_path_type(parent)


class PathTypeAnalyser:
    """Performs path type analysis"""

    @property
    def root(self) -> GameNode:
        pass

    def get_leaves(self) -> List[GameNode]:
        pass

    def _compute_path_types(self):
        """Analyses path types"""
        leaves: List[GameNode] = self.get_leaves()

        # Analyse leaves path types
        for leaf in leaves:
            leaf.path_type = _analyse_leaf_path_type(leaf)

        # Propagate path types upwards in correct order
        for path_type in (PathType.DUAL, PathType.WRONG, PathType.CORRECT):
            _perform_path_type_propagation(leaves, path_type)

        # There should be at least one correct path, so root should be correct
        if not self.root.is_correct():
            raise PreprocessingException("Path type analysis found no correct paths")
