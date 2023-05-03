from typing import Iterable

from backend import Player
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
