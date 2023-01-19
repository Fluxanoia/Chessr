from enum import auto
from typing import Optional

import pygame as pg

from src.game.board import Board, BoardEventType
from src.game.logic.piece_data_manager import (ManoeuvreCallback,
                                               PieceDataManager)
from src.game.logic.piece_tag import PieceTag, PieceTagType
from src.game.sprites.hud_text import HudText
from src.utils.enums import ArrayEnum, CellHighlightType, Side
from src.utils.helpers import IntVector


class MoveType(ArrayEnum):
    NORMAL = auto()
    ATTACK = auto()
    MANOEUVRE = auto()

Moves = tuple[tuple[IntVector], tuple[tuple[IntVector, ManoeuvreCallback]]]

class ClassicController:

    def __init__(self, board : Board) -> None:
        self.__board = board
        self.__piece_data_manager = PieceDataManager()

    def mouse_down(self, event : pg.event.Event) -> None:
        self.__board.mouse_down(event)
    
    def mouse_up(self, event : pg.event.Event) -> None:
        self.__board.mouse_up(event)

    def mouse_move(self, _event : pg.event.Event) -> None:
        if not self.__coords_text is None:
            gxy = self.__board.at_pixel_position(pg.mouse.get_pos())
            if gxy is None:
                self.__coords_text.clear()
                return
            
            i, j = gxy
            coords = chr(ord('A') + j) + str(self.__board.height - i)
            self.__coords_text.set_text(coords, (240, 240, 240))

    def update(self) -> None:
        board_event = self.__board.pop_event()
        while not board_event is None:
            if board_event.type is BoardEventType.CLICK:
                gxy = board_event.grid_position
                self.__click(gxy)
            board_event = self.__board.pop_event()
    
    def start(self) -> None:
        self.__turn : Side = Side.FRONT
        self.__moves : Moves = (tuple(), tuple())
        self.__selected : Optional[IntVector] = None
        self.__piece_data_manager.load_board(self.__board)

        scale = self.__board.scale
        board_bounds = self.__board.pixel_bounds
        left, bottom = board_bounds.bottomleft

        turn_text_size = 24
        buffer = 10

        self.__turn_text = HudText((left - buffer * scale, bottom), turn_text_size, scale)
        self.__turn_text.add_text(Side.FRONT, "WHITE", (240, 240, 240))
        self.__turn_text.add_text(Side.BACK, "BLACK", (5, 5, 5))
        self.__turn_text.set_text_by_key(self.__turn)

        self.__coords_text : Optional[HudText] = HudText((left - buffer * scale, bottom - 24 * scale - buffer), 16, scale)

    def __click(self, gxy : Optional[IntVector]) -> None:
        if gxy is None:
            self.__deselect()
            return
        else:
            click_piece = self.__board.piece_at(*gxy)
            if gxy == self.__selected:
                self.__deselect()
            elif not click_piece is None and click_piece.side == self.__turn:
                self.__deselect()
                self.__select(gxy)
            elif not self.__selected is None \
                and (click_piece is None or not click_piece.side == self.__turn):
                if self.__execute_move(self.__selected, gxy):
                    self.__selected = None
                else:
                    self.__deselect()

        if self.__selected is None:
            self.__moves = (tuple(), tuple())
            self.__clear_highlights()
        else:
            self.__moves = self.__piece_data_manager.get_moves(self.__board, self.__selected)
            self.__update_highlighting()

    def __select(self, gxy : IntVector) -> None:
        if not self.__selected is None:
            self.__deselect()
        self.__selected = gxy
        cell = self.__board.at(*gxy)
        if not cell is None:
            cell.select()

    def __deselect(self) -> None:
        if self.__selected is None:
            return
        cell = self.__board.at(*self.__selected)
        if not cell is None:
            cell.unselect()
        self.__selected = None

    def __execute_move(self, from_gxy : IntVector, to_gxy : IntVector) -> bool:
        if not to_gxy in self.__moves[0]:
            return False

        self.__board.move(from_gxy, to_gxy)
        moved_piece = self.__board.piece_at(*to_gxy)
        if not moved_piece is None and not moved_piece.has_tag(PieceTagType.HAS_MOVED):
            moved_piece.add_tag(PieceTag.get_tag(PieceTagType.HAS_MOVED))

        for (xy, callback) in self.__moves[1]:
            if not xy == to_gxy:
                continue
            callback(from_gxy, to_gxy)
        
        self.__board.update_tags()

        self.__turn = Side.BACK if self.__turn == Side.FRONT else Side.FRONT
        self.__turn_text.set_text_by_key(self.__turn)

        return True

    def __update_highlighting(self) -> None:
        for i in range(self.__board.height):
            for j in range(self.__board.width):
                cell = self.__board.at(i, j)
                if cell is None:
                    continue

                piece = cell.get_piece()

                if (i, j) in self.__moves[0]:
                    if piece is None:
                        cell.highlight(CellHighlightType.MOVE)
                    else:
                        piece.highlight()
                else:
                    if not piece is None:
                        piece.unhighlight()
                    cell.unhighlight()
    
    def __clear_highlights(self) -> None:
        for i in range(self.__board.height):
            for j in range(self.__board.width):
                cell = self.__board.at(i, j)
                if cell is None:
                    continue
                cell.unhighlight()
                piece = cell.get_piece()
                if piece is None:
                    continue
                piece.unhighlight()

