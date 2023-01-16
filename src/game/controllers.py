from enum import auto
from typing import Optional

import pygame as pg

from src.game.board import Board, BoardEventType
from src.game.logic.piece_data_manager import (ManoeuvreCallback,
                                               PieceDataManager)
from src.utils.enums import ArrayEnum, CellColour
from src.utils.helpers import IntVector


class MoveType(ArrayEnum):
    NORMAL = auto()
    ATTACK = auto()
    MANOEUVRE = auto()

MoveDictionary = dict[MoveType, tuple[IntVector | tuple[IntVector, ManoeuvreCallback], ...]]

class ClassicController:

    def __init__(self, board : Board):
        self.__board = board

        self.__piece_data_manager = PieceDataManager()

        self.__moves : MoveDictionary = {}
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
                # TODO: Check the possible moves
                self.__board.move(self.__selected, gxy)
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

    def __get_all_moves(self, gxy : IntVector) -> MoveDictionary:
        moves, attacks = self.__piece_data_manager.get_normal_and_attack_cells(self.__board, gxy)
        special = self.__piece_data_manager.get_special_manoeuvres(self.__board, gxy)
        return {
            MoveType.NORMAL : moves,
            MoveType.ATTACK : attacks,
            MoveType.MANOEUVRE : special,
        }

    def __update_highlighting(self):
        if self.__selected is None:
            self.__clear_highlights()
        else:
            self.__moves = self.__get_all_moves(self.__selected)
            for i in range(self.__board.height):
                for j in range(self.__board.width):
                    cell = self.__board.at(i, j)
                    if cell is None:
                        continue

                    if (i, j) in self.__moves.get(MoveType.NORMAL, []):
                        cell.set_temporary_cell_colour(CellColour.MOVE)
                    elif (i, j) in self.__moves.get(MoveType.ATTACK, []):
                        cell.set_temporary_cell_colour(CellColour.DANGER)
                    elif (i, j) in map(lambda x : x[0], self.__moves.get(MoveType.MANOEUVRE, [])):
                        cell.set_temporary_cell_colour(CellColour.DEBUG)
                    else:
                        cell.revert_cell_colour()
    
    def __clear_highlights(self):
        for i in range(self.__board.height):
            for j in range(self.__board.width):
                cell = self.__board.at(i, j)
                if cell is None:
                    continue
                cell.revert_cell_colour()
