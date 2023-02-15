from typing import Optional

import pygame as pg

from src.game.board import Board, BoardEventType
from src.game.logic.move_data import MoveType
from src.game.logic.piece_data_manager import PieceDataManager
from src.game.logic.piece_tag import PieceTag, PieceTagType
from src.game.sprites.hud_text import HudText
from src.utils.enums import CellHighlightType, Side
from src.utils.helpers import IntVector, get_coord_text


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
        self.__piece_data_manager.update_moves(self.__board)

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
        moves_object = self.__board.moves_at(*from_gxy)
        piece_to_move = self.__board.piece_at(*from_gxy)
        if moves_object is None or piece_to_move is None:
            return False
        
        moves = self.get_valid_moves(from_gxy)
        if not to_gxy in moves:
            return False

        self.__board.move(from_gxy, to_gxy)
        if not piece_to_move.has_tag(PieceTagType.HAS_MOVED):
            piece_to_move.add_tag(PieceTag.get_tag(PieceTagType.HAS_MOVED))

        moves_object.trigger_callbacks(from_gxy, to_gxy)
        
        self.__board.update_tags()
        self.__piece_data_manager.update_moves(self.__board)

#        state = self.__piece_data_manager.get_state(self.__board, self.__turn)
#        print(self.__turn, "check:", state.check)
#        print(self.__turn, "checkmate:", state.checkmate, "\n")

        self.__turn = Side.BACK if self.__turn == Side.FRONT else Side.FRONT
        self.__turn_text.set_text_by_key(self.__turn)


        return True
    
    def __update_highlighting(self) -> None:
        if self.__selected is None:
            self.__clear_highlights()
            return
        
        moves = self.get_valid_moves(self.__selected)
        for i in range(self.__board.height):
            for j in range(self.__board.width):
                cell = self.__board.at(i, j)
                if cell is None:
                    continue

                piece = cell.get_piece()

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
                cell.unhighlight()
                piece = cell.get_piece()
                if piece is None:
                    continue
                piece.unhighlight()

    def get_valid_moves(self, gxy : IntVector) -> tuple[IntVector, ...]:
        moves_object = self.__board.moves_at(*gxy)
        piece = self.__board.piece_at(*gxy)
        if moves_object is None or piece is None:
            return tuple()

        moves = moves_object.get_moves(MoveType.MOVE, True)
        attacks = moves_object.get_moves(MoveType.ATTACK, True)

        for attack in attacks:
            piece_to_take = self.__board.piece_at(*attack)
            if piece_to_take is None or piece_to_take.side == piece.side:
                continue

            moves = (*moves, attack)

        return moves
