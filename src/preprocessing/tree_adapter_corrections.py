from typing import Dict

import sgf

from src.preprocessing.preprocessing_exception import PreprocessingException


def correct_only_comment_first_node(problem: sgf.GameTree):
    """Removes only comment first node from given problem"""
    # If only one branch, the first node is in problem.nodes second position (first has initial board properties)
    if len(problem.nodes) > 1:
        problem.root.nodes.pop(1)

    # If several branches, the first node is in first child
    problem.children[0].nodes.pop(0)
    return


def correct_only_comment_branch_node(branch: sgf.GameTree):
    """Removes only comment node from given branch"""
    branch.nodes.pop(0)


def check_only_comment_branch_node(branch: sgf.GameTree) -> bool:
    """Returns true if branch begins with an only comment node"""
    if not branch.nodes:
        return False

    properties: Dict[str, str] = branch.nodes[0].properties
    if "B" in properties or "W" in properties:  # Has stone, so not only comment
        return False

    return "C" in properties or "N" in properties  # Has comment


def has_fake_root(problem: sgf.GameTree) -> bool:
    """Returns true if given problem has a fake root"""
    # The fake root does not have properties for initial board stones
    return "AW" not in problem.root.properties and "AB" not in problem.root.properties


def correct_fake_root(problem: sgf.GameTree):
    """Removes fake root from given problem"""
    # If first not is fake, must have at least 2 nodes in first branch
    if len(problem.nodes) == 1:
        raise PreprocessingException("Found impossible fake root with only one node")

    problem.nodes.pop(0)


def has_first_empty_branch(problem: sgf.GameTree) -> bool:
    """Returns true if given problem has an empty first branch"""
    # Empty first branch only occurs if problem begins with several branches
    if len(problem.nodes) > 1:
        return False

    first_branch: sgf.GameTree = problem.children[0]

    # Empty first branches have only one node
    if len(first_branch.nodes) > 1:
        return False

    properties: Dict[str, str] = first_branch.nodes[0].properties

    # The only node does not have a stone property
    return "B" not in properties and "W" not in properties


def correct_first_empty_branch(problem: sgf.GameTree):
    """Removes first empty branch from given problem"""
    problem.children.pop(0)  # remove first branch
