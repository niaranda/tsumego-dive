import re
from typing import List

from src.beans.board.color import Color
from src.preprocessing.preprocessing_exception import PreprocessingException


def apply_corrections(sgf: str) -> str:
    result = sgf.replace("\n", "")

    if __has_wrong_node_delimiters(result):
        result = __replace_node_delimiters(result)

    if __has_node_with_multiple_stone_placing(result):
        raise PreprocessingException("Unallowed multiple stone placing in one node")

    if __has_multiple_init_property(result, Color.BLACK):
        result = __unite_multiple_init_property(result, Color.BLACK)
    if __has_multiple_init_property(result, Color.WHITE):
        result = __unite_multiple_init_property(result, Color.WHITE)

    if __has_empty_board(result):
        raise PreprocessingException("Unallowed empty initial board")

    return result


def __has_empty_board(sgf: str) -> bool:
    return sgf.count("AB[") == 0 and sgf.count("AW[") == 0

def __has_wrong_node_delimiters(sgf: str) -> bool:
    return len(re.findall("\\([A-Z]{1,2}\\[", sgf)) != 0


def __replace_node_delimiters(sgf: str) -> str:
    wrong_portions: List[str] = re.findall("\\([A-Z]{1,2}\\[", sgf)
    corrections: List[str] = [portion.replace("(", "(;") for portion in wrong_portions]

    result = sgf
    for wrong_portion, correction in zip(wrong_portions, corrections):
        result = sgf.replace(wrong_portion, correction)
    return result


def __has_node_with_multiple_stone_placing(sgf: str) -> bool:
    nodes: List[str] = re.findall("\\(;.*?\\(;", sgf)  # branches
    if len(nodes) == 0:  # no branches
        nodes = re.findall("\\(;.*?;", sgf)
    if len(nodes) == 0:
        raise PreprocessingException("Empty problem")

    root_node: str = nodes[0]
    other_nodes: str = sgf.replace(root_node, "")
    return other_nodes.count("AW[") != 0 or other_nodes.count("AB[") != 0


def __has_multiple_init_property(sgf: str, color: Color) -> bool:
    property_name = __get_property_name(color)
    return sgf.count(property_name) > 1


def __get_property_name(color: Color) -> str:
    return "AB" if color == Color.BLACK else "AW"


def __unite_multiple_init_property(sgf: str, color: Color) -> str:
    property_name = __get_property_name(color)
    divided_properties: List[str] = re.findall(property_name + "(?:\\[[a-z]{2}\\])+", sgf)

    first_property = divided_properties[0]
    result = sgf
    for prop in divided_properties[1:]:
        result = result.replace(prop, "")

    positions: List[str] = [prop.replace(property_name, "") for prop in divided_properties[1:]]
    united_positions: str = "".join(positions)
    return result.replace(first_property, first_property + united_positions)
