from functools import reduce
from typing import Optional

from src.utils.enums import PieceType, enum_as_list
from src.utils.helpers import IntVector


class Notation:
    
    __instance : Optional['Notation'] = None

    @staticmethod
    def get() -> 'Notation':
        if Notation.__instance is None:
            Notation.__instance = Notation()
        return Notation.__instance

    def __init__(self) -> None:
        if not Notation.__instance is None:
            raise SystemExit('Invalid initialisation of Notation.')
        
        self.__chars = {
            PieceType.QUEEN : 'Q',
            PieceType.KING : 'K',
            PieceType.BISHOP : 'B',
            PieceType.ROOK : 'R',
            PieceType.KNIGHT : 'N',
            PieceType.PAWN : 'P',
        }

        if not all(map(lambda p : p in self.__chars.keys(), enum_as_list(PieceType))):
            raise SystemExit('Some piece types are undefined.')
        
    def get_piece_type(
        self,
        c : str
    ) -> Optional[PieceType]:
        for piece_type, char in self.__chars.items():
            if char == c:
                return piece_type
        return None

    def get_char(self, piece_type : PieceType):
        return self.__chars[piece_type]
    
    def get_coordinate_from_notation(self, notation : str, board_height : int) -> Optional[IntVector]:
        row = ''
        column = ''
        for char in notation:
            alpha = char.isalpha()
            if (not char.isdigit() and not alpha) \
                or (alpha and len(row) > 0):
                return None
            if char.isalpha():
                column += char
            else:
                row += char

        if len(row) == 0 or len(column) == 0:
            return None
         
        i = board_height - int(row)
        j = reduce(lambda r, x: r * 26 + x, map(lambda x : ord(x.lower()) - ord('a'), column), 0)
        return (i, j)

    def get_notation_from_coordinate(self, gxy : IntVector, board_height : int) -> Optional[str]:
        i, j = gxy
        return self.get_file_from_coordinate(j) + self.get_rank_from_coordinate(i, board_height)
    
    def get_file_from_coordinate(self, column : int):
        if column < 0:
            return '?'
        column += 1
        file = ''
        while column > 0:
            r = (column - 1) % 26
            file = chr(ord('a') + r) + file
            column = (column - r) // 26
        return file
    
    def get_rank_from_coordinate(self, row : int, board_height : int):
        return str(board_height - row)
