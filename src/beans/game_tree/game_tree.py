from typing import List

from src.beans.game_tree.game_node import GameNode
from src.beans.game_tree.path_type_analysis import PathTypeAnalyser


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

    def __get_descendants(self, node: GameNode) -> List[GameNode]:
        """Returns list of descendants to given node"""
        if node.is_leaf():
            return [node]

        nodes = [node]
        for child in node.children:
            nodes += self.__get_descendants(child)
        return nodes
