from backend import PieceType, Player
from src.utils.helpers import IntVector


class PieceData:

    def __init__(self, piece_type : PieceType, player : Player, gxy : IntVector):
        self.__type = piece_type
        self.__player = player
        self.__gxy = gxy

    @property
    def type(self):
        return self.__type

    @property
    def player(self):
        return self.__player

    @property
    def gxy(self):
        return self.__gxy
