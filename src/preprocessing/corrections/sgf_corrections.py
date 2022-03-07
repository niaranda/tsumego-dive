import re
from typing import List

from src.beans.board.color import Color
from src.preprocessing.errors.preprocessing_exception import PreprocessingException


def apply_corrections(sgf: str) -> str:
    """Returns sgf string after applying corrections"""
    # Remove line breaks to allow analysis
    result = sgf.replace("\n", "")

    # Check wrong delimiters
    if __has_wrong_node_delimiters(result):
        result = __replace_node_delimiters(result)

    # Check fatal error: node with multiple stone placing
    if __has_node_with_multiple_stone_placing(result):
        raise PreprocessingException("Unallowed multiple stone placing in one node")

    # Check multiple init properties
    if __has_multiple_init_property(result, Color.BLACK):
        result = __unite_multiple_init_property(result, Color.BLACK)
    if __has_multiple_init_property(result, Color.WHITE):
        result = __unite_multiple_init_property(result, Color.WHITE)

    # Check empty initial board
    if __has_empty_board(result):
        raise PreprocessingException("Unallowed empty initial board")

    return result


def __has_empty_board(sgf: str) -> bool:
    """True if initial board is empty. Must be called after checking multiple stone placing in nodes"""
    return sgf.count("AB[") == 0 and sgf.count("AW[") == 0


def __has_wrong_node_delimiters(sgf: str) -> bool:
    """True if sgf uses wrong node delimiters"""
    return len(re.findall("\\([A-Z]{1,2}\\[", sgf)) != 0


def __replace_node_delimiters(sgf: str) -> str:
    """Replaces wrong node delimiters with correct ones"""
    wrong_portions: List[str] = re.findall("\\([A-Z]{1,2}\\[", sgf)
    corrections: List[str] = [portion.replace("(", "(;") for portion in wrong_portions]

    result = sgf
    for wrong_portion, correction in zip(wrong_portions, corrections):
        result = sgf.replace(wrong_portion, correction)
    return result


def __has_node_with_multiple_stone_placing(sgf: str) -> bool:
    """True if sgf has at least one node with multiple stone placing"""
    nodes: List[str] = re.findall("\\(;.*?\\(;", sgf)  # branches

    if len(nodes) == 0:  # no branches
        nodes = re.findall("\\(;.*?;", sgf)

    if len(nodes) == 0:  # still no branches found -> problem is empty
        raise PreprocessingException("Empty problem")

    # Get all nodes except root
    root_node: str = nodes[0]
    other_nodes: str = sgf.replace(root_node, "")

    # Search for stone positioning in other nodes
    return other_nodes.count("AW[") != 0 or other_nodes.count("AB[") != 0


def __has_multiple_init_property(sgf: str, color: Color) -> bool:
    """True if sgf has multiple initial property for given color.
    Must be called after checking multiple stone placing in nodes"""
    property_name = __get_property_name(color)
    return sgf.count(property_name) > 1


def __get_property_name(color: Color) -> str:
    """Returns property name for given color positioning"""
    return "AB" if color == Color.BLACK else "AW"


def __unite_multiple_init_property(sgf: str, color: Color) -> str:
    """Returns sgf after uniting multiple initial properties for given color into one single property"""
    property_name = __get_property_name(color)

    # Get all properties to unite
    divided_properties: List[str] = re.findall(property_name + "(?:\\[[a-z]{2}\\])+", sgf)

    # Remove all but first property from sgf
    first_property = divided_properties[0]
    result = sgf
    for prop in divided_properties[1:]:
        result = result.replace(prop, "")

    # Join positions for all but first property
    positions: List[str] = [prop.replace(property_name, "") for prop in divided_properties[1:]]
    united_positions: str = "".join(positions)

    # Place joined positions after first property in sgf
    return result.replace(first_property, first_property + united_positions)
