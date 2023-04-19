from typing import Optional

from src.logic.move_data import MoveData, MoveType
from src.logic.piece_move_calculator import PieceMoveCalculator
from src.utils.enums import PieceType, enum_as_list


class PieceMoveCalculators:

    __instance : Optional['PieceMoveCalculators'] = None

    @staticmethod
    def get() -> 'PieceMoveCalculators':
        if PieceMoveCalculators.__instance is None:
            PieceMoveCalculators.__instance = PieceMoveCalculators()
        return PieceMoveCalculators.__instance

    def __init__(self) -> None:
        if not PieceMoveCalculators.__instance is None:
            raise SystemExit('Invalid initialisation of PieceMoveCalculators.')
        
        self.__data : dict[PieceType, PieceMoveCalculator] = {
            PieceType.QUEEN : PieceMoveCalculator((
                MoveData((1, 0), True, True),
                MoveData((1, 1), True, True)
            )),
            PieceType.KING : PieceMoveCalculator((
                MoveData((1, 0), True, False),
                MoveData((1, 1), True, False)
            )),
            PieceType.BISHOP : PieceMoveCalculator((
                MoveData((1, 1), True, True),
            )),
            PieceType.ROOK : PieceMoveCalculator((
                MoveData((1, 0), True, True),
            )),
            PieceType.KNIGHT : PieceMoveCalculator((
                MoveData((2, 1), True, False),
                MoveData((2, -1), True, False),
            )),
            PieceType.PAWN : PieceMoveCalculator((
                MoveData((-1, 0), False, False, (MoveType.MOVE,)),
                MoveData((-1, -1), False, False, (MoveType.ATTACK,)),
                MoveData((-1, 1), False, False, (MoveType.ATTACK,))
            ))
        }

        if not all(map(lambda p : p in self.__data.keys(), enum_as_list(PieceType))):
            raise SystemExit('Some piece types are undefined.')

    def get_calculator(
        self,
        piece_type : PieceType
    ) -> PieceMoveCalculator:
        return self.__data[piece_type]
