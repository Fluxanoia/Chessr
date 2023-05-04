from enum import auto
from typing import Optional

from backend import PieceConfiguration
from src.logic.board_data import BoardData
from src.utils.enums import ArrayEnum


class StateType(ArrayEnum):
    LOADING = auto()
    MAIN_MENU = auto()
    BOARD_SELECTION = auto()
    GAME = auto()

class GameStateData:

    def __init__(self, piece_configuration : PieceConfiguration, board_data : Optional[BoardData]):
        self.__piece_configuration = piece_configuration
        self.__board_data = board_data

    @property
    def piece_configuration(self):
        return self.__piece_configuration

    @property
    def board_data(self):
        return self.__board_data