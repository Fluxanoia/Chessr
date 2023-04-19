from threading import Thread
from typing import Any, Optional

import pygame as pg

from src.engine.group_manager import GroupType
from src.engine.state import State, StateType
from src.logic.board_applier import BoardApplier
from src.logic.board_data import BoardData
from src.logic.move_logic import MoveLogic
from src.logic.notation import Notation
from src.logic.pending_move_action import PendingMoveAction
from src.sprites.board.board import Board, BoardCell, BoardEventType
from src.sprites.board.piece import Piece
from src.sprites.ui.button import Button
from src.sprites.ui.text import Text
from src.utils.enums import (Anchor, CellHighlightType, Direction, LogicState,
                             Side, ViewState)
from src.utils.helpers import IntVector

PROCESSING = -1

class GameState(State):

    def __init__(self) -> None:
        super().__init__(StateType.GAME)

        self.__board_applier : BoardApplier
        self.__move_logic : MoveLogic
        self.__turn : Side
        self.__board : Board
        
        self.__turn_text : Text
        self.__state_text : Text
        self.__coords_text : Text
        self.__back_button : Button

        self.__state : LogicState = LogicState.NONE
        self.__pending_move_action : Optional[PendingMoveAction] = None
        self.__processing_thread : Optional[Thread] = None
        self.__selected : Optional[IntVector] = None

#region Game Loop Methods

    def load(self) -> None:
        self.__board_applier = BoardApplier()
        self.__move_logic = MoveLogic()
        self.__board = Board(self.__move_logic.supply_moves)

        self.__turn_text = Text(
            (0, 0),
            36,
            Anchor.BOTTOM_RIGHT,
            GroupType.GAME_UI,
            None,
            ViewState.INVISIBLE,
            Direction.RIGHT)
        self.__turn_text.add_text(Side.FRONT, 'WHITE', (240, 240, 240))
        self.__turn_text.add_text(Side.BACK, 'BLACK', (240, 240, 240))

        self.__state_text = Text(
            (0, 0),
            36,
            Anchor.TOP_LEFT,
            GroupType.GAME_UI,
            None,
            ViewState.INVISIBLE,
            Direction.TOP)
        self.__state_text.add_text(PROCESSING, 'Processing...', (240, 240, 240))
        self.__state_text.add_text(LogicState.CHECK, 'Check', (240, 240, 240))
        self.__state_text.add_text(LogicState.CHECKMATE, 'Checkmate', (240, 240, 240))
        self.__state_text.add_text(LogicState.STALEMATE, 'Stalemate', (240, 240, 240))

        self.__coords_text = Text(
            (0, 0),
            36,
            Anchor.BOTTOM_LEFT,
            GroupType.GAME_UI,
            None,
            ViewState.INVISIBLE,
            Direction.LEFT)
        
        self.__back_button = Button(
            (0, 0),
            'Back',
            lambda : self.change_state(StateType.MAIN_MENU),
            36,
            Anchor.TOP_LEFT,
            GroupType.GAME_UI)

        self._update_view()

    def start(self, data : Any) -> None:
        if not isinstance(data, BoardData):
            raise SystemExit('The GameState requires board data to initialise.')

        self.__state = LogicState.NONE
        self.__pending_move_action = None 
        self.__processing_thread = None
        self.__selected = None

        self.__turn = data.starting_turn
        self.__board_applier.apply_board(self.__board, data)
        self._update_view()

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

#region Events

    def on_view_change(self, bounds : pg.rect.Rect):
        buffer = 50
        self.__back_button.set_position((bounds.left + buffer, bounds.top + buffer))
        self.__board.set_position(*bounds.center)

        left, bottom = self.__board.bounds.bottomleft
        right = self.__board.bounds.right

        self.__turn_text.set_position((left - buffer, bottom))
        self.__coords_text.set_position((right + buffer, bottom))
        self.__state_text.set_position((left, bottom + buffer))

    def mouse_down(self, event : pg.event.Event) -> bool:
        if not self.__pending_move_action is None \
            and self.__pending_move_action.mouse_down(event):
            return True
        if self.__back_button.mouse_down(event):
            return True
        return self.__board.mouse_down(event)
    
    def mouse_up(self, event : pg.event.Event) -> bool:
        if not self.__pending_move_action is None \
            and self.__pending_move_action.mouse_up(event):
            return True
        
        if self.__back_button.mouse_up(event):
            return True
        
        return self.__board.mouse_up(event)

    def mouse_move(self, event : pg.event.Event) -> None:
        if not self.__pending_move_action is None:
            self.__pending_move_action.mouse_move(event)

        self.__back_button.mouse_move(event)
        gxy = self.__board.at_pixel_position(pg.mouse.get_pos())
        if gxy is None:
            if not self.__coords_text.is_tweening_to(ViewState.INVISIBLE):
                pause = 500 if self.__coords_text.is_completely_visible() else 0
                self.__coords_text.do_slide(ViewState.INVISIBLE, pause=pause)
        else:
            coords = Notation.get().get_notation_from_coordinate(gxy, self.__board.height)
            if coords is not None:
                self.__coords_text.set_text(coords.upper(), (240, 240, 240))
                if not self.__coords_text.is_tweening_to(ViewState.VISIBLE):
                    self.__coords_text.do_slide(ViewState.VISIBLE)

#endregion

#region Private Game Logic Methods

    def __click(self, gxy : Optional[IntVector]) -> None:
        if self.__is_pending_action():
            return

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
                self.__execute_move(self.__selected, gxy)

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

    def __execute_move(self, from_gxy : IntVector, to_gxy : IntVector) -> None:
        if self.__is_pending_action() or self.__is_processing():
            return

        moves = self.__board.moves_at(*from_gxy)
        if moves is None:
            return
        
        valid_move = next((x for x in moves.get_valid_moves() if x.gxy == to_gxy), None)
        if valid_move is None:
            return
        
        def clear_action():
            if not self.__pending_move_action is None:
                self.__pending_move_action.delete()
                self.__pending_move_action = None

        def finalise():
            clear_action()
            self.__board.move(from_gxy, to_gxy)
            self.__deselect()
            self.__update_highlighting()
        
            self.__turn = Side.BACK if self.__turn == Side.FRONT else Side.FRONT
            self.__turn_text.set_text_with_slide_by_key(self.__turn)

            self.__process_state()

        if valid_move.pending_action is None:
            finalise()
        else:
            self.__pending_move_action = PendingMoveAction.get_action(
                valid_move.pending_action,
                self.__board,
                from_gxy,
                to_gxy,
                finalise,
                clear_action
            )
    
    def __process_state(self):
        if self.__state_text.is_visible():
            self.__state_text.set_text_with_slide_by_key(PROCESSING)
        else:
            self.__state_text.set_text_by_key(PROCESSING)
            self.__state_text.do_slide(ViewState.VISIBLE, pause=200)

        def process():
            self.__state = self.__move_logic.get_state(self.__board, self.__turn)
        self.__processing_thread = Thread(target=process)
        self.__processing_thread.daemon = True
        self.__processing_thread.start()

    def __update_highlighting(self) -> None:
        if self.__is_pending_action():
            return

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
    
    def __is_pending_action(self) -> bool:
        return not self.__pending_move_action is None

#endregion
