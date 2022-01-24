from typing import List, Optional

from src.beans.game_tree.game_node import GameNode


class GameTree:
    def __init__(self, root: GameNode):
        self.__root: GameNode = root

    @property
    def root(self):
        return self.__root

    def get_leaves(self) -> List[GameNode]:
        return list(filter(GameNode.is_leaf, self.get_nodes()))

    def get_nodes(self, node: Optional[GameNode] = None) -> List[GameNode]:
        if node is None:
            node = self.__root
        if node.is_leaf():
            return [node]

        nodes = [node]
        for child in node.children:
            nodes += self.get_nodes(child)
        return nodes
