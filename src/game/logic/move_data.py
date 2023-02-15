from enum import auto
from typing import Callable, Optional

from src.utils.enums import ArrayEnum
from src.utils.helpers import IntVector


class MoveType(ArrayEnum):
    MOVE = auto()
    ATTACK = auto()

Vectors = tuple[IntVector, ...]
ManoeuvreCallback = Callable[[IntVector, IntVector], None]

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

    def __get_flipped_vectors(self) -> Vectors:
        flipped : list[IntVector] = []
        for (i, j) in self.__vectors:
            flipped.append((-i, j))
        return tuple(flipped)

    @staticmethod
    def __revolve_vector(vector : IntVector) -> Vectors:
        revolved : list[IntVector] = [vector]
        for _ in range(3):
            i, j = revolved[-1]
            revolved.append((j, -i))
        return tuple(revolved)

class Move:

    def __init__(self, gxy : IntVector, move_type : MoveType, valid : bool):
        self.__gxy = gxy
        self.__move_type = move_type
        self.__valid = valid

    @property
    def gxy(self):
        return self.__gxy

    @property
    def move_type(self):
        return self.__move_type

    @property
    def valid(self):
        return self.__valid

class Moves:

    def __init__(self, moves : tuple[Move, ...]):
        self.__moves = moves
        self.__callbacks : tuple[tuple[IntVector, ManoeuvreCallback], ...] = tuple()

    def get_moves(self, move_type : MoveType, valid : bool) -> Vectors:
        filtered_moves = filter(
            lambda x : x.move_type == move_type and x.valid == valid,
            self.__moves)
        return tuple(map(lambda x : x.gxy, filtered_moves))

    def add_move(self, move : Move, callback : ManoeuvreCallback):
        self.__moves = (*self.__moves, move)
        self.__callbacks = (*self.__callbacks, (move.gxy, callback))

    def trigger_callbacks(self, from_gxy : IntVector, to_gxy : IntVector):
        for (gxy, callback) in self.__callbacks:
            if not gxy == to_gxy:
                continue
            callback(from_gxy, to_gxy)

