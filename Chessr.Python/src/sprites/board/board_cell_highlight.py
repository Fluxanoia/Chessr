from typing import Optional

import pygame as pg
from src.engine.factory import Factory
from src.engine.group_manager import DrawingPriority, GroupType
from src.engine.spritesheets.board_spritesheet import BoardColour
from src.engine.spritesheets.highlight_spritesheet import CellHighlightType
from src.sprites.sprite import ChessrSprite
from src.utils.helpers import FloatVector


class BoardCellHighlight(ChessrSprite):

    def __init__(self, xy : FloatVector, scale : float, board_colour : BoardColour) -> None:
        self.__type : CellHighlightType = CellHighlightType.MOVE
        self.__board_colour = board_colour

        self.__scale = scale
        image = Factory.get().highlight_spritesheet.get_sheet(scale)

        super().__init__(xy, GroupType.GAME_BOARD, DrawingPriority.PLUS_ONE, image, self.__get_src_rect(scale))

        self.set_visible(False)

    def set_theme(self, highlight_type : CellHighlightType, board_colour : BoardColour) -> None:
        self.__type = highlight_type
        self.__board_colour = board_colour
        self.src_rect = self.__get_src_rect()

    def set_visible(self, visible : bool) -> None:
        self.visible = int(visible)

    def __get_src_rect(self, scale : Optional[float] = None) -> pg.Rect:
        scale = scale if not scale is None else self.__scale
        spritesheet = Factory.get().highlight_spritesheet
        return spritesheet.get_src_rect(self.__board_colour, self.__type, scale)
