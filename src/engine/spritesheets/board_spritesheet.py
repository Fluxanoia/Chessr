import pygame as pg

from src.engine.file_manager import FileManager
from src.engine.spritesheets.spritesheet import Spritesheet
from src.utils.enums import (BoardColour, CellColour, PieceColour, PieceType,
                             ShadowType, Side, enum_as_list)
from src.utils.helpers import scale_rect


class BoardSpritesheet(Spritesheet):

    PIECE_WIDTH = 16
    PIECE_HEIGHT = 48

    SHADOW_WIDTH = 16
    SHADOW_HEIGHT = 7

    BOARD_WIDTH = 16
    BOARD_HEIGHT = 20

    def __init__(self, file_manager : FileManager) -> None:
        super().__init__(file_manager, 'sprites.png')

    @staticmethod
    def __get_width_of_pieces() -> int:
        return len(enum_as_list(PieceType)) * len(enum_as_list(Side)) * BoardSpritesheet.PIECE_WIDTH

    @staticmethod
    def __get_width_of_shadows() -> int:
        return BoardSpritesheet.SHADOW_WIDTH

    @staticmethod
    def get_piece_srcrect(
        colour : PieceColour,
        piece_type : PieceType,
        side : Side,
        scale : float = 1
    ) -> pg.Rect:
        side_count = len(enum_as_list(Side))
        r = pg.Rect(
            (piece_type * side_count + side) * BoardSpritesheet.PIECE_WIDTH,
            colour * BoardSpritesheet.PIECE_HEIGHT,
            BoardSpritesheet.PIECE_WIDTH,
            BoardSpritesheet.PIECE_HEIGHT
        )
        scale_rect(r, scale)
        return r
    
    @staticmethod
    def get_shadow_srcrect(shadow_type : ShadowType, scale : float = 1) -> pg.Rect:
        r = pg.Rect(
            BoardSpritesheet.__get_width_of_pieces(),
            shadow_type * BoardSpritesheet.SHADOW_HEIGHT,
            BoardSpritesheet.SHADOW_WIDTH,
            BoardSpritesheet.SHADOW_HEIGHT
        )
        scale_rect(r, scale)
        return r

    @staticmethod
    def get_board_srcrect(colour_scheme : BoardColour, cell_colour : CellColour, scale : float = 1) -> pg.Rect:
        base_x = BoardSpritesheet.__get_width_of_pieces() + BoardSpritesheet.__get_width_of_shadows()
        r = pg.Rect(
            base_x + cell_colour * BoardSpritesheet.BOARD_WIDTH,
            colour_scheme * BoardSpritesheet.BOARD_HEIGHT,
            BoardSpritesheet.BOARD_WIDTH,
            BoardSpritesheet.BOARD_HEIGHT
        )
        scale_rect(r, scale)
        return r
