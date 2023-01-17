from typing import Optional

from src.game.board import Board
from src.utils.enums import Side
from src.utils.helpers import IntVector, add_vectors

Vectors = tuple[IntVector, ...]

class PieceData:

    def __init__(
        self,
        character : str,
        move_vectors : Vectors,
        revolve : bool,
        expand : bool,
        attack_vectors : Optional[Vectors] = None
    ):
        self.__char = character
        self.__expand = expand
        self.__revolve = revolve

        self.__move_vectors = move_vectors
        self.__attack_vectors = attack_vectors

        if revolve:
            self.__move_vectors = self.__revolve_vectors(self.__move_vectors)
            if self.__attack_vectors is not None:
                self.__attack_vectors = self.__revolve_vectors(self.__attack_vectors)

    def get_normal_moves(
        self,
        board : Board,
        side : Side,
        gxy : IntVector
    ) -> tuple[IntVector,...]:
        moves : list[IntVector] = []

        def check_cell(cell : IntVector, attack : bool) -> bool:
            board_cell = board.at(*cell)
            if board_cell is None:
                return False
            if not board_cell.get_piece() is None:
                if attack or self.__attack_vectors is None:
                    moves.append(cell)
                return False
            if not attack:
                moves.append(cell)
            return self.__expand

        def iterate_vectors(vectors : Vectors, attack : bool) -> None:
            for vector in vectors:
                cell = add_vectors(gxy, vector)
                while check_cell(cell, attack):
                    cell = add_vectors(cell, vector)

        move_vectors = self.side_transform_vectors(self.__move_vectors, side)
        attack_vectors = self.side_transform_vectors(self.__attack_vectors, side)

        iterate_vectors(move_vectors, False)
        iterate_vectors(attack_vectors, True)

        return tuple(moves)

    def side_transform_vector(self, vector : IntVector, side : Side) -> IntVector:
        return self.side_transform_vectors((vector,), side)[0]

    def side_transform_vectors(self, vectors : Optional[Vectors], side : Side) -> Vectors:
        if vectors is None:
            return tuple()
        do_flip = not self.__revolve and side == Side.BACK
        if do_flip:
            return self.__flip_vectors(vectors)
        return vectors

    def __revolve_vectors(self, vectors : Vectors) -> Vectors:
        revolved : list[IntVector] = []
        for v in vectors:
            revolved.append(v)
            for _ in range(3):
                i, j = revolved[-1]
                revolved.append((j, -i))
        return tuple(revolved)

    def __flip_vectors(self, vectors : Vectors) -> Vectors:
        flipped : list[IntVector] = []
        for (i, j) in vectors:
            flipped.append((-i, j))
        return tuple(flipped)

    @property
    def char(self) -> str:
        return self.__char
