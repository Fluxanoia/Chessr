from enum import auto
from src.enum import ArrayEnum

class Side(ArrayEnum):
    FRONT = auto()
    BACK = auto()

class PieceType(ArrayEnum):
    QUEEN = auto()
    KING = auto()
    BISHOP = auto()
    ROOK = auto()
    KNIGHT = auto()
    PAWN = auto()

class PieceColour(ArrayEnum):
    WHITE = auto()
    BLACK = auto()
    RED = auto()

class PieceTag(ArrayEnum):
    HAS_MOVED = auto()
    DOUBLE_MOVE = auto()

class ShadowType(ArrayEnum):
    LIGHT = auto()
    DARK = auto()

class BoardType(ArrayEnum):
    LIGHT = auto()
    DARK = auto()
    MOVE = auto()
    DANGER = auto()
    DEBUG = auto()

class BoardColour(ArrayEnum):
    BEIGE = auto()
    BLACK_WHITE = auto()