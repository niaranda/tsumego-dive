from typing import List, Tuple

from src.beans.board.stone import Color, Stone

Pos = Tuple[int, int]


class StoneGroup:
    def __init__(self, stones: List[Stone]):
        self.__stones: List[Stone] = stones
        if not self.__valid_state():
            raise Exception()

    def __str__(self) -> str:
        return str([str(stone) for stone in self.__stones])

    @property
    def stones(self):
        return self.__stones

    def add_stone(self, stone: Stone):
        if stone.color != self.get_color():
            raise Exception()
        self.stones.append(stone)

    def get_color(self) -> Color:
        return self.__stones[0].color

    def get_positions(self) -> List[Pos]:
        return [stone.pos for stone in self.__stones]

    def is_attached(self, stone: Stone):
        return any([group_stone.is_neighbor(stone) for group_stone in self.__stones])

    def has_liberties(self) -> bool:
        for stone in self.__stones:
            if stone.has_liberties():
                return True
        return False

    def __valid_state(self) -> bool:
        if len(self.__stones) == 0:
            return False
        return all([stone.color == self.get_color() for stone in self.__stones])
