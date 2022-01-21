from src.beans.game_tree.game_node import GameNode


class GameTree:
    def __init__(self, root: GameNode):
        self.__root: GameNode = root

    @property
    def root(self):
        return self.__root
