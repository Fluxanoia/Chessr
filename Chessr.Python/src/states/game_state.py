from threading import Thread
from typing import Any, Callable, Optional

import pygame as pg
from backend import ChessEngine, Consequence, MoveProperty, Player
from backend import State as BackendState
from src.engine.group_manager import GroupType
from src.engine.spritesheets.highlight_spritesheet import CellHighlightType
from src.engine.state import State, StateType
from src.engine.state_type import GameStateData
from src.logic.board_applier import BoardApplier
from src.logic.pending_move_action import PendingMoveAction
from src.sprites.board.board import Board, BoardEventType
from src.sprites.ui.button import Button
from src.sprites.ui.text import Text
from src.utils.enums import Anchor, Direction, ViewState
from src.utils.helpers import IntVector

PROCESSING = -1

class GameState(State):

    def __init__(self) -> None:
        super().__init__(StateType.GAME)

        self.__board_applier : BoardApplier
        self.__board : Board
        
        self.__turn_text : Text
        self.__state_text : Text
        self.__coords_text : Text
        self.__back_button : Button

        self.__engine : ChessEngine
        self.__consequences : Optional[list[Consequence]] = None
        self.__pending_move_action : Optional[PendingMoveAction] = None
        self.__processing_thread : Optional[Thread] = None
        self.__selected : Optional[IntVector] = None

#region Game Loop Methods

    def load(self) -> None:
        self.__board_applier = BoardApplier()
        self.__board = Board()

        self.__turn_text = Text(
            (0, 0),
            36,
            Anchor.BOTTOM_RIGHT,
            GroupType.GAME_UI,
            None,
            ViewState.INVISIBLE,
            Direction.RIGHT)
        self.__turn_text.add_text(Player.WHITE, 'WHITE', (240, 240, 240))
        self.__turn_text.add_text(Player.BLACK, 'BLACK', (240, 240, 240))

        self.__state_text = Text(
            (0, 0),
            36,
            Anchor.TOP_LEFT,
            GroupType.GAME_UI,
            None,
            ViewState.INVISIBLE,
            Direction.TOP)
        self.__state_text.add_text(PROCESSING, 'Processing...', (240, 240, 240))
        self.__state_text.add_text(BackendState.CHECK, 'Check', (240, 240, 240))
        self.__state_text.add_text(BackendState.CHECKMATE, 'Checkmate', (240, 240, 240))
        self.__state_text.add_text(BackendState.STALEMATE, 'Stalemate', (240, 240, 240))

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
        if not isinstance(data, GameStateData) or data.board_data is None:
            raise SystemExit('The GameState requires certain data to initialise.')

        board_data = data.board_data

        self.__pending_move_action = None 
        self.__processing_thread = None
        self.__selected = None

        self.__board_applier.apply_board(self.__board, board_data)
        self._update_view()

        self.__coords_text.set_state(ViewState.INVISIBLE)
        self.__state_text.set_state(ViewState.INVISIBLE)

        self.__engine = ChessEngine(data.piece_configuration)
        
        def process():
            self.__engine.start(board_data.grid, board_data.starting_turn)

        self.__process_backend(process)

    def update(self) -> None:
        if not self.__processing_thread is None \
            and not self.__processing_thread.is_alive():
            self.__processing_thread = None

            if not self.__consequences is None:
                self.__board.apply_consequences(self.__consequences)
                self.__consequences = None

            self.__clear_pending_action()
            self.__deselect()
            self.__update_highlighting()
            self.__turn_text.set_text_with_slide_by_key(self.__engine.get_current_player())

            self.__turn_text.set_text_by_key(self.__engine.get_current_player())
            self.__turn_text.set_state(ViewState.VISIBLE)

            state = self.__engine.get_state()
            if state == BackendState.NONE:
                self.__state_text.do_slide(ViewState.INVISIBLE)
            else:
                self.__state_text.set_text_with_slide_by_key(state)

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
            coords = self.__engine \
                .get_piece_configuration() \
                .get_notation_from_coordinate(gxy, self.__board.height)
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
            elif not click_piece is None and click_piece.player == self.__engine.get_current_player():
                self.__select(gxy)
            elif not self.__selected is None \
                and (click_piece is None or not click_piece.player == self.__engine.get_current_player()):
                self.__execute_move(self.__selected, gxy)

        self.__update_highlighting()

    def __select(self, gxy : IntVector) -> None:
        if not self.__selected is None:
            self.__deselect()

        if self.__is_processing():
            return
        
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

    def __execute_move(self, from_gxy : IntVector, to_gxy : IntVector) -> None:
        if self.__is_pending_action() or self.__is_processing():
            return

        moves = tuple(x for x in self.__engine.get_current_moves() if x.moves_from(from_gxy))
        move = next((x for x in moves if x.moves_to(to_gxy)), None)
        if move is None:
            return

        def process():
            self.__consequences = self.__engine.make_move(move)

        if not move.property is MoveProperty.PROMOTION:
            self.__process_backend(process)
        else:
            self.__pending_move_action = PendingMoveAction.get_action(
                move,
                lambda : self.__process_backend(process),
                self.__clear_pending_action,
                (10, 10),
                self.__board.scale
            )
    
    def __process_backend(self, process : Callable[[], None]):
        if self.__state_text.is_visible():
            self.__state_text.set_text_with_slide_by_key(PROCESSING)
        else:
            self.__state_text.set_text_by_key(PROCESSING)
            self.__state_text.do_slide(ViewState.VISIBLE, pause=200)
        
        self.__processing_thread = Thread(target=process)
        self.__processing_thread.daemon = True
        self.__processing_thread.start()

    def __update_highlighting(self) -> None:
        if self.__is_pending_action():
            return

        if self.__selected is None or self.__is_processing():
            self.__clear_highlights()
            return
        
        moves = tuple(x for x in self.__engine.get_current_moves() if x.moves_from(self.__selected))
        for i in range(self.__board.height):
            for j in range(self.__board.width):
                cell = self.__board.at(i, j)
                if cell is None:
                    continue

                piece = cell.piece
                if any(map(lambda x : x.moves_to((i, j)), moves)):
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
                piece = cell.piece
                if piece is None:
                    continue
                piece.unhighlight()

    def __is_processing(self) -> bool:
        return not self.__processing_thread is None
    
    def __clear_pending_action(self):
        if not self.__pending_move_action is None:
            self.__pending_move_action.delete()
            self.__pending_move_action = None
    
    def __is_pending_action(self) -> bool:
        return not self.__pending_move_action is None

#endregion
