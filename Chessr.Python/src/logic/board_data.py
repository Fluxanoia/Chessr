from typing import Iterable, Optional

from backend import Piece, Player
from src.logic.piece_data import PieceData


class BoardData:

    def __init__(
        self,
        valid : bool,
        width : int,
        height : int,
        starting_turn : Player,
        name : str,
        description : str,
        pieces : Iterable[PieceData]
    ):
        self.__valid = valid
        self.__width = width
        self.__height = height
        self.__starting_turn = starting_turn
        self.__name = name
        self.__description = description
        self.__pieces = tuple(pieces)

    @property
    def valid(self):
        return self.__valid

    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height
    
    @property
    def starting_turn(self):
        return self.__starting_turn
    
    @property
    def name(self):
        return self.__name
    
    @property
    def description(self):
        return self.__description

    @property
    def pieces(self):
        return self.__pieces
    
    @property
    def grid(self):
        x : list[list[Optional[Piece]]] = []
        for i in range(self.height):
            rank : list[Optional[Piece]] = []
            for j in range(self.width):
                piece = next((Piece(x.type, x.player) for x in self.__pieces if x.gxy == (i, j)), None)
                rank.append(piece)
            x.append(rank)
        return x
