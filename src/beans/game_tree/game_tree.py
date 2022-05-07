from typing import List, Dict

from src.beans.board.color import Color
from src.beans.board.stone import Pos, Stone
from src.beans.game_tree.game_node import GameNode
from src.beans.game_tree.path_type_analysis import PathTypeAnalyser


def _generate_stone_pos_sgf_with_color(init_stones: List[Stone], color: Color) -> List[str]:
    stones: List[Stone] = list(filter(lambda stone: stone.color == color, init_stones))
    positions: List[Pos] = [stone.pos for stone in stones]
    return [_generate_sgf_pos(pos) for pos in positions]


def _generate_sgf_pos(pos: Pos) -> str:
    row, col = pos
    return "[" + chr(row + 97) + chr(col + 97) + "]"


def _generate_node_sgf(node: GameNode) -> str:
    stone = node.stone

    comment = ""
    if node.comment != "" and node.comment != "unknown":
        comment = "C[" + node.comment.capitalize() + "]"

    return ";" + stone.color.name[0] + _generate_sgf_pos(stone.pos) + comment + _generate_children_sgf(node)


def _generate_children_sgf(node: GameNode):
    if node.is_leaf():
        return ""

    children: List[GameNode] = node.children

    if len(children) == 1:
        return _generate_node_sgf(children[0])

    sgf = ""
    for child in children:
        sgf += "(" + _generate_node_sgf(child) + ")"

    return sgf


class GameTree(PathTypeAnalyser):
    """Represents a game tree for a tsumego"""

    def __init__(self, root: GameNode):
        """Creates a new game tree with given node as root and performs path type analysis"""
        self.__root: GameNode = root

        # perform path type analysis
        self._compute_path_types()

    @property
    def root(self):
        return self.__root

    def get_leaves(self) -> List[GameNode]:
        """Returns list of all leaves"""
        return list(filter(GameNode.is_leaf, self.get_nodes()))

    def get_nodes(self) -> List[GameNode]:
        """Returns list of all nodes in the tree"""
        return self.__get_descendants(self.__root)

    def generate_sgf(self) -> str:
        init_node = ";GM[1]FF[4]SZ[19]HA[0]KM[0]"
        initial_stones_sgf: str = self.__generate_initial_stones_sgf()

        children_sgf: str = _generate_children_sgf(self.root)

        return "(" + init_node + initial_stones_sgf + children_sgf + ")"

    def __generate_initial_stones_sgf(self) -> str:
        stones_dict: Dict[Pos, Color] = self.root.board.placed_stones
        init_stones: List[Stone] = [Stone(pos, color) for pos, color in stones_dict.items()]

        white_pos_str: List[str] = _generate_stone_pos_sgf_with_color(init_stones, Color.WHITE)
        white_sgf = "AW" + "".join(white_pos_str) if len(white_pos_str) != 0 else ""

        black_pos_str: List[str] = _generate_stone_pos_sgf_with_color(init_stones, Color.BLACK)
        black_sgf = "AB" + "".join(black_pos_str) if len(black_pos_str) != 0 else ""

        return white_sgf + black_sgf

    def __get_descendants(self, node: GameNode) -> List[GameNode]:
        """Returns list of descendants to given node"""
        if node.is_leaf():
            return [node]

        nodes = [node]
        for child in node.children:
            nodes += self.__get_descendants(child)
        return nodes
