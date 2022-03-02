import re
from typing import List

from src.beans.board.color import Color


def apply_corrections(sgf: str) -> str:
    result = sgf.replace("\n", "")

    if __has_multiple_init_property(result, Color.BLACK):
        result = __unite_multiple_init_property(result, Color.BLACK)
    if __has_multiple_init_property(result, Color.WHITE):
        result = __unite_multiple_init_property(result, Color.WHITE)

    return result


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
