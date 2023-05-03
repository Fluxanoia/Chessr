from enum import auto

import pygame as pg
from src.engine.file_manager import FileManager
from src.engine.spritesheets.spritesheet import Spritesheet
from src.utils.enums import ArrayEnum
from src.utils.helpers import scale_rect


class CellColour(ArrayEnum):
    LIGHT = auto()
    DARK = auto()

class BoardColour(ArrayEnum):
    BEIGE = auto()
    BLACK_WHITE = auto()

class BoardSpritesheet(Spritesheet):

    BOARD_WIDTH = 16
    BOARD_HEIGHT = 20

    def __init__(self, file_manager : FileManager) -> None:
        super().__init__(file_manager, 'board.png')

    @staticmethod
    def get_src_rect(
        colour_scheme : BoardColour,
        cell_colour : CellColour,
        scale : float = 1
    ) -> pg.Rect:
        r = pg.Rect(
            cell_colour * BoardSpritesheet.BOARD_WIDTH,
            colour_scheme * BoardSpritesheet.BOARD_HEIGHT,
            BoardSpritesheet.BOARD_WIDTH,
            BoardSpritesheet.BOARD_HEIGHT
        )
        scale_rect(r, scale)
        return r
