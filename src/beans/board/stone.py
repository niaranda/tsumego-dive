from typing import Tuple, NamedTuple

from src.beans.board.color import Color

Pos = Tuple[int, int]


class Stone(NamedTuple):
    pos: Pos
    color: Color
