from typing import Dict

import sgf

from src.preprocessing.preprocessing_exception import PreprocessingException


def correct_only_comment_tree_node(problem: sgf.GameTree):
    if len(problem.nodes) > 1:
        problem.root.nodes.pop(1)

    problem.children[0].nodes.pop(0)
    return


def correct_only_comment_branch_node(branch: sgf.GameTree):
    branch.nodes.pop(0)


def check_only_comment_branch_node(branch: sgf.GameTree) -> bool:
    if not branch.nodes:
        return False

    properties: Dict[str, str] = branch.nodes[0].properties
    if "B" in properties or "W" in properties:
        return False

    return "C" in properties or "N" in properties


def has_fake_root(problem: sgf.GameTree) -> bool:
    return "AW" not in problem.root.properties and "AB" not in problem.root.properties


def correct_fake_root(problem: sgf.GameTree):
    # root must have at least 2 nodes
    if len(problem.nodes) == 1:
        raise PreprocessingException("Found impossible fake root with only one node")

    problem.nodes.pop(0)


def has_first_empty_branch(problem: sgf.GameTree) -> bool:
    if len(problem.nodes) > 1:
        return False
    first_branch: sgf.GameTree = problem.children[0]
    if len(first_branch.nodes) > 1:
        return False
    properties: Dict[str, str] = first_branch.nodes[0].properties
    return "B" not in properties and "W" not in properties


def correct_first_empty_branch(problem: sgf.GameTree):
    problem.children.pop(0)  # remove first branch
