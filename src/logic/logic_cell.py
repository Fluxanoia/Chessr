from typing import Optional

from src.sprites.piece import LogicPiece
from src.utils.helpers import IntVector


class LogicCell():

    def __init__(self, gxy : IntVector, piece : Optional[LogicPiece], dirty : bool = True):
        self.__gxy = gxy
        self.__piece = piece
        self.__dirty = dirty

    def is_dirty(self):
        return self.__dirty
    
    def clean(self):
        self.__dirty = False

    def set_piece(self, piece : Optional[LogicPiece]) -> None:
        self.__piece = piece
        self.__dirty = True

    def take_piece_from(self, cell : "LogicCell"):
        if cell.piece is None:
            return
        if not self.__piece is None:
            self.remove_piece()
        self.set_piece(cell.piece)
        cell.set_piece(None)

    def remove_piece(self):
        if self.__piece is None:
            return
        self.__piece.delete()
        self.set_piece(None)

    def copy(self) -> "LogicCell":
        piece = None if self.__piece is None else self.__piece.copy()
        return LogicCell(self.__gxy, piece, self.__dirty)

    @property
    def gxy(self) -> IntVector:
        return self.__gxy
    
    @property
    def piece(self) -> Optional[LogicPiece]:
        return self.__piece