from __future__ import annotations

from enum import Enum


class Color(Enum):
    """Represents a stone color"""
    BLACK = 1
    WHITE = -1

    def __str__(self):
        return self.name

    def get_other(self):
        """Get the other color"""
        return Color.BLACK if self == Color.WHITE else Color.WHITE
