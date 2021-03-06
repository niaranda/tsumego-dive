from typing import Dict

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Pos

GRID_LINE_START = 1 / 21
GRID_LINE_END = 20 / 21
GRID_LINE_WIDTH = 1.3
GRID_LINE_COLOR = "black"
STONE_SIZE = 12
WHITE_STONE_EDGE_COLOR = "black"
BLACK_STONE_EDGE_COLOR = "gray"
BACKGROUND_IMAGE: np.ndarray = plt.imread("../../images/board_background.jpg")


def draw_board(board: Board):
    """Draws given board"""
    fig: Figure
    ax: Axes
    fig, ax = plt.subplots()

    # Draw grid
    for i in range(19):
        ax.axhline(-i, GRID_LINE_START, GRID_LINE_END, linewidth=GRID_LINE_WIDTH, color=GRID_LINE_COLOR)
        ax.axvline(i, GRID_LINE_START, GRID_LINE_END, linewidth=GRID_LINE_WIDTH, color=GRID_LINE_COLOR)

    fig.set_dpi(150)
    ax.set_axis_off()

    # Draw stones
    __draw_stones(ax, board)

    # Add background and show
    ax.imshow(BACKGROUND_IMAGE, extent=(-1, 19, -19, 1))
    plt.show()


def __draw_stones(ax: Axes, board: Board):
    stones: Dict[Pos, Color] = board.placed_stones
    for pos, color in stones.items():
        ax.plot(
            pos[1], -pos[0], marker='o', markersize=STONE_SIZE,
            markeredgecolor=__get_edge_color(color), markerfacecolor=__get_face_color(color)
        )


def __get_face_color(color: Color) -> str:
    return color.name.lower()


def __get_edge_color(color: Color) -> str:
    if color == Color.WHITE:
        return WHITE_STONE_EDGE_COLOR
    return BLACK_STONE_EDGE_COLOR
