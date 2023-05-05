from enum import auto

import pygame as pg
from src.engine.file_manager import FileManager
from src.engine.spritesheets.board_spritesheet import BoardColour
from src.engine.spritesheets.spritesheet import Spritesheet
from src.utils.enums import ArrayEnum
from src.utils.helpers import scale_rect


class CellHighlightType(ArrayEnum):
    MOVE = auto()  

class HighlightSpritesheet(Spritesheet):

    HIGHLIGHT_WIDTH = 16
    HIGHLIGHT_HEIGHT = 20

    def __init__(self, file_manager : FileManager) -> None:
        super().__init__(file_manager, 'highlights.png')

    @staticmethod
    def get_src_rect(
        colour_scheme : BoardColour,
        cell_highlight : CellHighlightType,
        scale : float = 1
    ) -> pg.Rect:
        r = pg.Rect(
            cell_highlight * HighlightSpritesheet.HIGHLIGHT_WIDTH,
            colour_scheme * HighlightSpritesheet.HIGHLIGHT_HEIGHT,
            HighlightSpritesheet.HIGHLIGHT_WIDTH,
            HighlightSpritesheet.HIGHLIGHT_HEIGHT
        )
        scale_rect(r, scale)
        return r
