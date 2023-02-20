from typing import Optional

import pygame as pg

from src.engine.factory import Factory
from src.engine.spritesheets.board_spritesheet import BoardSpritesheet
from src.game.logic.logic_cell import LogicCell
from src.game.sprites.board_cell_highlight import BoardCellHighlight
from src.game.sprites.piece import LogicPiece, Piece
from src.utils.enums import (BoardColour, CellColour, CellHighlightType,
                             PieceColour, PieceType, Side)
from src.utils.helpers import FloatVector, IntVector
from src.utils.sprite import ChessrSprite, GroupType


class BoardCell(ChessrSprite, LogicCell):

    def __init__(
        self,
        gxy : IntVector,
        xy : FloatVector,
        colour_scheme : BoardColour,
        colour : CellColour,
        scale : float,
        piece_scale : float
    ):
        LogicCell.__init__(self, gxy, None)
        self.__colour_scheme = colour_scheme
        self.__colour = colour

        image = Factory.get().board_spritesheet.get_sheet(scale)
        ChessrSprite.__init__(self, xy, GroupType.GAME_BOARD, image, self.__get_src_rect(scale), scale)

        self.__selected = False
        self.__highlight = BoardCellHighlight(xy, scale, self.__colour_scheme)

        self.__piece_scale = piece_scale

    def set_theme(self, colour_scheme : BoardColour, colour : CellColour) -> None:
        self.__colour_scheme = colour_scheme
        self.__colour = colour
        self.src_rect = self.__get_src_rect()

    def add_piece(self, colour : PieceColour, piece_type : PieceType, side : Side) -> None:
        if not self.piece is None:
            return
        self.set_piece(Piece(
            self.__get_piece_position(),
            self.__piece_scale,
            colour,
            piece_type,
            side))

    def set_piece(self, piece : Optional[LogicPiece]):
        self.__selected = False
        LogicCell.set_piece(self, piece)

        if piece is None:
            return

        if not isinstance(piece, Piece):
            self.__raise_display_cast_error()
        
        duration = 300
        piece.move(None, self.__get_piece_position(), duration)
        piece.lift(None, 0, duration)

    def select(self) -> None:
        if not isinstance(self.piece, Optional[Piece]):
            self.__raise_display_cast_error()

        if self.__selected:
            self.unselect()
        elif not self.piece is None:
            self.__selected = True
            rect_width = self.rect.w if not self.rect is None else 0
            self.piece.lift(None, rect_width / 2, 200)

    def unselect(self) -> None:
        if not isinstance(self.piece, Optional[Piece]):
            self.__raise_display_cast_error()
        
        if self.__selected and not self.piece is None:
            self.__selected = False
            duration = 100
            self.piece.move(None, self.__get_piece_position(), duration)
            self.piece.lift(None, 0, duration)

    def highlight(self, highlight_type : CellHighlightType) -> None:
        self.__highlight.set_theme(highlight_type, self.__colour_scheme)
        self.__highlight.set_visible(True)

    def unhighlight(self) -> None:
        self.__highlight.set_visible(False)

    def __get_src_rect(self, scale : Optional[float] = None) -> pg.Rect:
        scale = scale if not scale is None else self.scale
        spritesheet = Factory.get().board_spritesheet
        return spritesheet.get_board_srcrect(self.__colour_scheme, self.__colour, scale)

    def __get_piece_position(self) -> FloatVector:
        rect_x, rect_y, rect_width = 0, 0, 0
        if not self.rect is None:
            rect_x = self.rect.x
            rect_y = self.rect.y
            rect_width = self.rect.w
        offset = (rect_width - BoardSpritesheet.PIECE_WIDTH * self.__piece_scale) / 2
        return (rect_x + offset, rect_y + rect_width - offset)

    @staticmethod
    def __raise_display_cast_error():
        raise SystemExit('There was an attempt to set the piece of a display cell to a logic piece.')
