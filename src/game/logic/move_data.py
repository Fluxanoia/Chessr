from enum import auto
from typing import Optional

from src.utils.enums import ArrayEnum
from src.utils.helpers import IntVector


class MoveType(ArrayEnum):
    MOVE = auto()
    ATTACK = auto()

class MoveData:

    def __init__(
        self,
        vector : IntVector,
        revolve : bool,
        expand : bool,
        types : Optional[tuple[MoveType]] = None
    ):
        self.__vectors = self.__revolve_vector(vector) if revolve else tuple([vector])
        self.__expand = expand
        self.__types = (MoveType.MOVE, MoveType.ATTACK) if types is None else types

    def get_vectors(self, flip : bool):
        return self.__get_flipped_vectors() if flip else self.__vectors

    @property
    def expand(self):
        return self.__expand

    @property
    def types(self):
        return self.__types

    def __get_flipped_vectors(self) -> tuple[IntVector, ...]:
        flipped : list[IntVector] = []
        for (i, j) in self.__vectors:
            flipped.append((-i, j))
        return tuple(flipped)

    @staticmethod
    def __revolve_vector(vector : IntVector) -> tuple[IntVector, ...]:
        revolved : list[IntVector] = [vector]
        for _ in range(3):
            i, j = revolved[-1]
            revolved.append((j, -i))
        return tuple(revolved)
