from enum import EnumMeta, IntEnum, auto

#region Enum Classes and Functions

class ArrayEnum(IntEnum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[int]) -> int:
        return count

class CountEnum(IntEnum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[int]) -> int:
        return count + 1

def enum_as_list(enum : EnumMeta) -> list[str]:
    return [getattr(enum, name) for name in dir(enum) if not name.startswith('_')]

#endregion

#region Generic Enums

class Anchor(ArrayEnum):
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()
    CENTER = auto()

class Direction(ArrayEnum):
    TOP = auto()
    BOTTOM = auto()
    LEFT = auto()
    RIGHT = auto()

class ViewState(ArrayEnum):
    INVISIBLE = auto()
    VISIBLE = auto()

#endregion

#region Input Enums

class MouseButton(CountEnum):
    LEFT = auto()
    MIDDLE = auto()
    RIGHT = auto()
    SCROLL_UP = auto()
    SCROLL_DOWN = auto()

#endregion
