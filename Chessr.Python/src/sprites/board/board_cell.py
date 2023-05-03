from typing import Optional

import pygame as pg
from backend import PieceType, Player
from src.engine.factory import Factory
from src.engine.group_manager import GroupType
from src.engine.spritesheets.board_spritesheet import BoardColour, CellColour
from src.engine.spritesheets.highlight_spritesheet import CellHighlightType
from src.engine.spritesheets.piece_spritesheet import (PieceColour,
                                                       PieceSpritesheet)
from src.sprites.board.board_cell_highlight import BoardCellHighlight
from src.sprites.board.piece import Piece
from src.sprites.sprite import ChessrSprite
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
        self.__gxy = gxy
        self.__colour_scheme = colour_scheme
        self.__colour = colour
        self.__scale = scale
        self.__piece_scale = piece_scale
        
        self.__piece : Optional[Piece] = None

        self.__selected = False
        self.__highlight = BoardCellHighlight(xy, scale, self.__colour_scheme)

        image = Factory.get().board_spritesheet.get_sheet(scale)
        super().__init__(xy, GroupType.GAME_BOARD, None, image, self.__get_src_rect(scale))
 
    def delete(self):
        if self.__piece is not None:
            self.__piece.delete()
        self.__highlight.delete()
        super().delete()

    def set_position(self, xy : FloatVector, preserve_tween : bool = False) -> None:
        super().set_position(xy, preserve_tween)
        self.__highlight.set_position(xy, preserve_tween)

        if self.__piece is None:
            return

        self.__piece.set_position(self.__get_piece_position(), preserve_tween)

    def set_theme(self, colour_scheme : BoardColour, colour : CellColour) -> None:
        self.__colour_scheme = colour_scheme
        self.__colour = colour
        self.src_rect = self.__get_src_rect()

    def add_piece(self, colour : PieceColour, piece_type : PieceType, player : Player) -> None:
        if not self.__piece is None:
            return
        self.set_piece(Piece(
            self.__get_piece_position(),
            self.__piece_scale,
            colour,
            piece_type,
            player))

    def set_piece(self, piece : Optional[Piece]):
        self.__selected = False
        self.__piece = piece

        if piece is None:
            return

        duration = 300
        piece.move(None, self.__get_piece_position(), duration)
        piece.lift(None, 0, duration)

    def take_piece_from(self, cell : "BoardCell"):
        if cell.piece is None:
            return
        if not self.__piece is None:
            self.remove_piece()
        self.set_piece(cell.piece)
        cell.set_piece(None)

    def remove_piece(self):
        if self.__piece is None:
            return
        self.__piece.delete()
        self.set_piece(None)

    def select(self) -> None:
        if self.__selected:
            self.unselect()
        elif not self.__piece is None:
            self.__selected = True
            rect_width = self.dst_rect.w if not self.dst_rect is None else 0
            self.__piece.lift(None, rect_width / 2, 200)

    def unselect(self) -> None:
        if self.__selected and not self.__piece is None:
            self.__selected = False
            duration = 100
            self.__piece.move(None, self.__get_piece_position(), duration)
            self.__piece.lift(None, 0, duration)

    def highlight(self, highlight_type : CellHighlightType) -> None:
        self.__highlight.set_theme(highlight_type, self.__colour_scheme)
        self.__highlight.set_visible(True)

    def unhighlight(self) -> None:
        self.__highlight.set_visible(False)

    def __get_src_rect(self, scale : Optional[float] = None) -> pg.Rect:
        scale = scale if not scale is None else self.__scale
        spritesheet = Factory.get().board_spritesheet
        return spritesheet.get_src_rect(self.__colour_scheme, self.__colour, scale)

    def __get_piece_position(self) -> FloatVector:
        rect_x, rect_y, rect_width = 0, 0, 0
        if not self.dst_rect is None:
            rect_x = self.dst_rect.x
            rect_y = self.dst_rect.y
            rect_width = self.dst_rect.w
        offset = (rect_width - PieceSpritesheet.PIECE_WIDTH * self.__piece_scale) / 2
        return (rect_x + offset, rect_y + rect_width - offset)
    
    @property
    def gxy(self):
        return self.__gxy
    
    @property
    def piece(self):
        return self.__piece
