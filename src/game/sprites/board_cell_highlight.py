from typing import Optional

import pygame as pg

from src.engine.factory import Factory
from src.game.sprite import ChessrSprite, GroupType
from src.utils.enums import BoardColour, CellHighlightType
from src.utils.helpers import FloatVector


class BoardCellHighlight(ChessrSprite):

    def __init__(self, xy : FloatVector, scale : float, board_colour : BoardColour) -> None:
        self.__type : CellHighlightType = CellHighlightType.MOVE
        self.__board_colour = board_colour

        image = Factory.get().board_spritesheet.get_sheet(scale)

        super().__init__(xy, GroupType.BOARD_HIGHLIGHT, image, self.__get_src_rect(scale), scale)

        self.set_visible(False)

    def set_theme(self, highlight_type : CellHighlightType, board_colour : BoardColour) -> None:
        self.__type = highlight_type
        self.__board_colour = board_colour
        self.src_rect = self.__get_src_rect()

    def set_visible(self, visible : bool) -> None:
        self.visible = int(visible)

    def __get_src_rect(self, scale : Optional[float] = None) -> pg.Rect:
        if scale is None:
            scale = self.scale
        spritesheet = Factory.get().board_spritesheet
        return spritesheet.get_cell_highlight_srcrect(self.__board_colour, self.__type, scale)
