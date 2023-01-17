from typing import Optional

import pygame as pg

from src.engine.factory import Factory
from src.engine.spritesheets.board_spritesheet import BoardSpritesheet
from src.game.sprite import ChessrSprite, GroupType
from src.game.sprites.board_cell_highlight import BoardCellHighlight
from src.game.sprites.piece import Piece
from src.utils.enums import (BoardColour, CellColour, CellHighlightType,
                             PieceColour, PieceType, Side)
from src.utils.helpers import FloatVector, IntVector


class BoardCell(ChessrSprite):

    def __init__(
        self,
        gxy : IntVector,
        xy : FloatVector,
        colour_scheme : BoardColour,
        colour : CellColour,
        scale : float,
        piece_scale : float
    ):
        self.__grid_position = gxy
        self.__colour_scheme = colour_scheme
        self.__colour = colour

        image = Factory.get().board_spritesheet.get_sheet(scale)
        super().__init__(xy, GroupType.BOARD, image, self.__get_src_rect(scale), scale)

        self.__selected = False
        self.__highlight = BoardCellHighlight(xy, scale, self.__colour_scheme)

        self.__piece_scale = piece_scale
        self.__piece : Optional[Piece] = None

    def set_theme(self, colour_scheme : BoardColour, colour : CellColour) -> None:
        self.__colour_scheme = colour_scheme
        self.__colour = colour
        self.src_rect = self.__get_src_rect()

    def get_piece(self) -> Optional[Piece]:
        return self.__piece

    def add_piece(self, colour : PieceColour, piece_type : PieceType, side : Side) -> None:
        if not self.__piece is None:
            return
        self.__piece = Piece(self.__get_piece_position(), self.__piece_scale, colour, piece_type, side)

    def remove_piece(self, delete_sprite : bool = False) -> None:
        self.__selected = False
        if delete_sprite and not self.__piece is None and not self.__piece.group is None:
            Factory.get().group_manager.get_group(self.__piece.group).remove(self.__piece)
        self.__piece = None

    def select(self) -> None:
        if self.__selected:
            self.unselect()
        elif not self.__piece is None:
            self.__selected = True
            rect_width = self.rect.w if not self.rect is None else 0
            self.__piece.lift(None, rect_width / 2, 200)

    def unselect(self) -> None:
        if self.__selected and not self.__piece is None:
            self.__selected = False
            duration = 100
            self.__piece.move(None, self.__get_piece_position(), duration)
            self.__piece.lift(None, 0, duration)

    def transfer_from(self, cell : 'BoardCell') -> None:
        new_piece = cell.get_piece()
        if new_piece is None:
            return
        
        if not self.__piece is None:
            self.remove_piece()

        cell.remove_piece()
        self.__piece = new_piece

        duration = 300
        self.__piece.move(None, self.__get_piece_position(), duration)
        self.__piece.lift(None, 0, duration)

    def highlight(self, highlight_type : CellHighlightType) -> None:
        self.__highlight.set_theme(highlight_type, self.__colour_scheme)
        self.__highlight.set_visible(True)

    def unhighlight(self) -> None:
        self.__highlight.set_visible(False)

    @property
    def grid_position(self) -> IntVector:
        return self.__grid_position

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
