from enum import auto

from src.utils.enums import ArrayEnum


class StateType(ArrayEnum):
    LOADING = auto()
    MAIN_MENU = auto()
    BOARD_SELECTION = auto()
    GAME = auto()
