from typing import Optional

import pygame as pg

from src.game.board import Board, BoardCell, BoardEventType
from src.game.logic.piece_data_manager import PieceDataManager
from src.game.sprites.hud_text import HudText
from src.game.sprites.piece import Piece
from src.utils.enums import CellHighlightType, LogicState, Side
from src.utils.helpers import IntVector, get_coord_text


class Controller:

    def __init__(self) -> None:
        self.__piece_data_manager = PieceDataManager()
        self.__board = Board(self.__piece_data_manager.get_moves)

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
            
            coords = get_coord_text(gxy, self.__board.height)
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
        self.__selected : Optional[IntVector] = None
        self.__piece_data_manager.load_board(self.__board)

        scale = self.__board.scale
        board_bounds = self.__board.pixel_bounds
        left, bottom = board_bounds.bottomleft

        turn_text_size = 24
        coord_text_size = 16
        buffer = 10

        left = left - buffer * scale 

        self.__turn_text = HudText((left, bottom), turn_text_size, scale)
        self.__turn_text.add_text(Side.FRONT, "WHITE", (240, 240, 240))
        self.__turn_text.add_text(Side.BACK, "BLACK", (5, 5, 5))
        self.__turn_text.set_text_by_key(self.__turn)

        bottom = bottom - turn_text_size * scale - buffer
        self.__coords_text : Optional[HudText] = HudText((left, bottom), coord_text_size, scale)
        
        bottom = bottom - coord_text_size * scale - buffer
        self.__state_text : Optional[HudText] = HudText((left, bottom), 24, scale)

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

        self.__update_highlighting()

    def __select(self, gxy : IntVector) -> None:
        if not self.__selected is None:
            self.__deselect()
        self.__selected = gxy
        cell = self.__board.at(*gxy)

        if not isinstance(cell, Optional[BoardCell]):
            raise SystemExit('Expected display cell.')            

        if not cell is None:
            cell.select()

    def __deselect(self) -> None:
        if self.__selected is None:
            return
        cell = self.__board.at(*self.__selected)
        
        if not isinstance(cell, Optional[BoardCell]):
            raise SystemExit('Expected display element.')    

        if not cell is None:
            cell.unselect()

        self.__selected = None

    def __execute_move(self, from_gxy : IntVector, to_gxy : IntVector) -> bool:
        moves = self.__piece_data_manager.get_valid_moves(self.__board, from_gxy)
        if not to_gxy in moves:
            return False

        self.__board.move(from_gxy, to_gxy)

        self.__turn = Side.BACK if self.__turn == Side.FRONT else Side.FRONT
        self.__turn_text.set_text_by_key(self.__turn)

        state = self.__piece_data_manager.get_state(self.__board, self.__turn)
        if not self.__state_text is None:
            if state == LogicState.NONE:
                self.__state_text.clear()
            else:
                text = "Unknown"
                if state == LogicState.CHECK:
                    text = "Check"
                elif state == LogicState.CHECKMATE:
                    text = "Checkmate"
                elif state == LogicState.STALEMATE:
                    text = "Stalemate"
                self.__state_text.set_text(text, (240, 240, 240))

        return True
    
    def __update_highlighting(self) -> None:
        if self.__selected is None:
            self.__clear_highlights()
            return
        
        moves = self.__piece_data_manager.get_valid_moves(self.__board, self.__selected)
        for i in range(self.__board.height):
            for j in range(self.__board.width):
                cell = self.__board.at(i, j)
                if cell is None:
                    continue

                piece = cell.piece
                if not isinstance(cell, BoardCell) \
                    or not isinstance(piece, Optional[Piece]):
                    raise SystemExit('Expected display element.')   

                if (i, j) in moves:
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
                if not isinstance(cell, BoardCell):
                    raise SystemExit('Expected display element.')   
                cell.unhighlight()
                piece = cell.piece
                if piece is None:
                    continue
                if not isinstance(piece, Piece):
                    raise SystemExit('Expected display element.')   
                piece.unhighlight()
