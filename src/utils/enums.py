from enum import EnumMeta, IntEnum, auto


class ArrayEnum(IntEnum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[int]) -> int:
        return count

class CountEnum(IntEnum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[int]) -> int:
        return count + 1

class MouseButton(CountEnum):
    LEFT = auto()
    MIDDLE = auto()
    RIGHT = auto()
    SCROLL_UP = auto()
    SCROLL_DOWN = auto()

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

class CellColour(ArrayEnum):
    LIGHT = auto()
    DARK = auto()
    MOVE = auto()
    DANGER = auto()
    DEBUG = auto()

class BoardColour(ArrayEnum):
    BEIGE = auto()
    BLACK_WHITE = auto()

def enum_as_list(enum : EnumMeta) -> list[str]:
    return [getattr(enum, name) for name in dir(enum) if not name.startswith('_')]
