from enum import auto
from typing import Optional

import pygame as pg

from src.game.board import Board, BoardEventType
from src.game.logic.piece_data_manager import (ManoeuvreCallback,
                                               PieceDataManager)
from src.game.logic.piece_tag import PieceTag, PieceTagType
from src.utils.enums import ArrayEnum, CellColour
from src.utils.helpers import IntVector


class MoveType(ArrayEnum):
    NORMAL = auto()
    ATTACK = auto()
    MANOEUVRE = auto()

Moves = tuple[tuple[IntVector], tuple[tuple[IntVector, ManoeuvreCallback]]]

class ClassicController:

    def __init__(self, board : Board):
        self.__board = board

        self.__piece_data_manager = PieceDataManager()

        self.__moves : Moves = (tuple(), tuple())
        self.__selected : Optional[IntVector] = None

    def mouse_down(self, event : pg.event.Event) -> None:
        self.__board.mouse_down(event)
    
    def mouse_up(self, event : pg.event.Event) -> None:
        self.__board.mouse_up(event)

    def update(self) -> None:
        board_event = self.__board.pop_event()
        while not board_event is None:
            if board_event.type is BoardEventType.CLICK:
                gxy = board_event.grid_position
                self.__click(gxy)
            board_event = self.__board.pop_event()
    
    def start(self):
        self.__piece_data_manager.load_board(self.__board)

    def __click(self, gxy : Optional[IntVector]):
        if gxy is None:
            self.__deselect()
            return
        else:
            click_piece = self.__board.piece_at(*gxy)
            if gxy == self.__selected:
                self.__deselect()
            elif not click_piece is None:
                self.__deselect()
                self.__select(gxy)
            elif not self.__selected is None:
                self.__execute_move(self.__selected, gxy)
                self.__selected = None

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

    def __execute_move(self, from_gxy : IntVector, to_gxy : IntVector):
        # TODO: Check the possible moves
        self.__board.move(from_gxy, to_gxy)
        moved_piece = self.__board.piece_at(*to_gxy)
        if not moved_piece is None and not moved_piece.has_tag(PieceTagType.HAS_MOVED):
            moved_piece.add_tag(PieceTag.get_tag(PieceTagType.HAS_MOVED))

        for (xy, callback) in self.__moves[1]:
            if not xy == to_gxy:
                continue
            callback(from_gxy, to_gxy)

    def __update_highlighting(self):
        if self.__selected is None:
            self.__clear_highlights()
        else:
            self.__moves = self.__piece_data_manager.get_moves(self.__board, self.__selected)

            for i in range(self.__board.height):
                for j in range(self.__board.width):
                    cell = self.__board.at(i, j)
                    if cell is None:
                        continue

                    if (i, j) in self.__moves[0]:
                        cell.set_temporary_cell_colour(CellColour.MOVE)
                    else:
                        cell.revert_cell_colour()
    
    def __clear_highlights(self):
        for i in range(self.__board.height):
            for j in range(self.__board.width):
                cell = self.__board.at(i, j)
                if cell is None:
                    continue
                cell.revert_cell_colour()
