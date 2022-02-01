from typing import List, Optional

from src.beans.game_tree.game_node import GameNode
from src.preprocessing.path_type_analysis import compute_path_types


class GameTree:
    """Represents a game tree for a tsumego"""

    def __init__(self, root: GameNode):
        """Creates a new game tree with given node as root"""
        self.__root: GameNode = root

        # perform path type analysis
        compute_path_types(self)

    @property
    def root(self):
        return self.__root

    def get_leaves(self) -> List[GameNode]:
        """Get list of all leaves"""
        return list(filter(GameNode.is_leaf, self.get_nodes()))

    def get_nodes(self, node: Optional[GameNode] = None) -> List[GameNode]:
        """Recursively get list of all nodes in the tree"""
        if node is None:
            node = self.__root
        if node.is_leaf():
            return [node]

        nodes = [node]
        for child in node.children:
            nodes += self.get_nodes(child)
        return nodes
