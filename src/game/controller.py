from threading import Thread
from typing import Optional

import pygame as pg

from src.game.board import Board, BoardCell, BoardEventType
from src.game.logic.piece_data_manager import PieceDataManager
from src.game.sprites.hud_text import HudText
from src.game.sprites.piece import Piece
from src.utils.enums import (Anchor, CellHighlightType, Direction, LogicState,
                             Side, ViewState)
from src.utils.helpers import IntVector, get_coord_text

PROCESSING = -1

class Controller:

    def __init__(self) -> None:
        self.__piece_data_manager = PieceDataManager()
        self.__board = Board(self.__piece_data_manager.supply_moves)

        scale = self.__board.scale
        self.__turn_text = HudText(
            (0, 0), 24, scale, Anchor.BOTTOM_RIGHT, ViewState.INVISIBLE, Direction.RIGHT)
        self.__turn_text.add_text(Side.FRONT, "WHITE", (240, 240, 240))
        self.__turn_text.add_text(Side.BACK, "BLACK", (240, 240, 240))

        self.__state_text : HudText = HudText(
            (0, 0), 24, scale, Anchor.TOP_LEFT, ViewState.INVISIBLE, Direction.TOP)
        self.__state_text.add_text(PROCESSING, "Processing...", (240, 240, 240))
        self.__state_text.add_text(LogicState.CHECK, "Check", (240, 240, 240))
        self.__state_text.add_text(LogicState.CHECKMATE, "Checkmate", (240, 240, 240))
        self.__state_text.add_text(LogicState.STALEMATE, "Stalemate", (240, 240, 240))

        self.__coords_text : HudText = HudText(
            (0, 0), 16, scale, Anchor.BOTTOM_LEFT, ViewState.INVISIBLE, Direction.LEFT)
    
#region Game Loop Methods

    def start(self) -> None:
        self.__state : LogicState = LogicState.NONE
        self.__processing_thread : Optional[Thread] = None
        self.__selected : Optional[IntVector] = None

        self.__turn = self.__piece_data_manager.load_board(self.__board, '4x5 micro.board')

        scale = self.__board.scale
        board_bounds = self.__board.pixel_bounds
        left, bottom = board_bounds.bottomleft
        right = board_bounds.right
        buffer = 10 * scale

        self.__turn_text.set_position((left - buffer, bottom))
        self.__coords_text.set_position((right + buffer, bottom))
        self.__state_text.set_position((left, bottom + buffer))

        self.__coords_text.set_state(ViewState.INVISIBLE)
        self.__state_text.set_state(ViewState.INVISIBLE)

        self.__turn_text.set_text_by_key(self.__turn)
        self.__turn_text.set_state(ViewState.VISIBLE)
        self.__process_state()

    def update(self) -> None:
        if not self.__processing_thread is None \
            and not self.__processing_thread.is_alive():
            self.__processing_thread = None
            if self.__state == LogicState.NONE:
                self.__state_text.do_slide(ViewState.INVISIBLE)
            else:
                self.__state_text.set_text_with_slide_by_key(self.__state)

        board_event = self.__board.pop_event()
        while not board_event is None:
            if board_event.type is BoardEventType.CLICK:
                gxy = board_event.grid_position
                self.__click(gxy)
            board_event = self.__board.pop_event()
    
#endregion

#region User Input

    def mouse_down(self, event : pg.event.Event) -> None:
        self.__board.mouse_down(event)
    
    def mouse_up(self, event : pg.event.Event) -> None:
        self.__board.mouse_up(event)

    def mouse_move(self, _event : pg.event.Event) -> None:
        gxy = self.__board.at_pixel_position(pg.mouse.get_pos())
        if gxy is None:
            if not self.__coords_text.is_tweening_to(ViewState.INVISIBLE):
                self.__coords_text.do_slide(ViewState.INVISIBLE, pause=500)
        else:
            coords = get_coord_text(gxy, self.__board.height)
            self.__coords_text.set_text(coords, (240, 240, 240))
            if not self.__coords_text.is_tweening_to(ViewState.VISIBLE):
                self.__coords_text.do_slide(ViewState.VISIBLE)

#endregion

#region Private Game Logic Methods

    def __click(self, gxy : Optional[IntVector]) -> None:
        if gxy is None:
            self.__deselect()
        else:
            click_piece = self.__board.piece_at(*gxy)
            if gxy == self.__selected:
                self.__deselect()
            elif not click_piece is None and click_piece.side == self.__turn:
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

        if self.__is_processing():
            return
        
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
        if self.__is_processing():
            return False

        moves = self.__board.moves_at(*from_gxy)
        if moves is None:
            return False
        
        valid_moves = map(lambda x : x.gxy, moves.get_valid_moves())
        if not to_gxy in valid_moves:
            return False

        self.__board.move(from_gxy, to_gxy)
        
        self.__turn = Side.BACK if self.__turn == Side.FRONT else Side.FRONT
        self.__turn_text.set_text_with_slide_by_key(self.__turn)

        self.__process_state()

        return True
    
    def __process_state(self):
        if self.__state_text.is_visible():
            self.__state_text.set_text_with_slide_by_key(PROCESSING)
        else:
            self.__state_text.set_text_by_key(PROCESSING)
            self.__state_text.do_slide(ViewState.VISIBLE, pause=200)

        def process():
            self.__state = self.__piece_data_manager.get_state(self.__board, self.__turn)
        self.__processing_thread = Thread(target=process)
        self.__processing_thread.start()

    def __update_highlighting(self) -> None:
        if self.__selected is None or self.__is_processing():
            self.__clear_highlights()
            return
        
        moves = self.__board.moves_at(*self.__selected)
        if moves is None:
            self.__clear_highlights()
            return
        
        valid_moves = tuple(map(lambda x : x.gxy, moves.get_valid_moves()))
        for i in range(self.__board.height):
            for j in range(self.__board.width):
                cell = self.__board.at(i, j)
                if cell is None:
                    continue

                piece = cell.piece
                if not isinstance(cell, BoardCell) \
                    or not isinstance(piece, Optional[Piece]):
                    raise SystemExit('Expected display element.')   

                if (i, j) in valid_moves:
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

    def __is_processing(self) -> bool:
        return not self.__processing_thread is None or self.__board.is_dirty()

#endregion
