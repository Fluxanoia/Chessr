from typing import Callable

import pygame as pg

from src.engine.group_manager import GroupType
from src.logic.board import Board
from src.sprites.board.board_cell import BoardCell
from src.sprites.ui.button import Button
from src.utils.enums import Anchor, PendingMoveType, PieceType
from src.utils.helpers import IntVector


class PendingMoveAction:

    def __init__(
        self,
        action : PendingMoveType,
        finalise : Callable[[], None],
        cancel : Callable[[], None]
    ) -> None:
        self.__action = action
        self.__finalise = finalise
        self.__cancel = cancel

    @property
    def action(self):
        return self.__action

    def delete(self):
        pass

    def _finalise(self):
        self.__finalise()

    def _cancel(self):
        self.__cancel()

#region User Input

    def mouse_down(self, _event : pg.event.Event) -> bool:
        return False
    
    def mouse_up(self, _event : pg.event.Event) -> bool:
        return False

    def mouse_move(self, _event : pg.event.Event) -> None:
        pass

#endregion

    @staticmethod
    def get_action(
        move_type : PendingMoveType,
        board : Board,
        from_gxy : IntVector,
        to_gxy : IntVector,
        finalise : Callable[[], None],
        cancel : Callable[[], None]
    ) -> 'PendingMoveAction':
        if move_type == PendingMoveType.PIECE_PROMOTION:
            return PiecePromotionMoveAction(board, from_gxy, to_gxy, finalise, cancel)
        raise SystemExit(f'Unexpected pending move type, \'{move_type}\'.')

class PiecePromotionMoveAction(PendingMoveAction):

    def __init__(
        self,
        board : Board,
        from_gxy : IntVector,
        to_gxy : IntVector,
        finalise: Callable[[], None],
        cancel: Callable[[], None]
    ) -> None:
        super().__init__(PendingMoveType.PIECE_PROMOTION, finalise, cancel)

        cell = board.at(
            min(from_gxy[0], to_gxy[0]),
            max(from_gxy[1], to_gxy[1]))
        
        if cell is None or not isinstance(cell, BoardCell):
            raise SystemExit('Expected display element.')   

        pixel_bounds = cell.pixel_bounds
        buffer = 10 * board.scale
        x = 0 if pixel_bounds is None else pixel_bounds.right + buffer
        y = 0 if pixel_bounds is None else pixel_bounds.top

        buttons : list[Button] = []

        def add_button(piece_type : PieceType, text : str, ix : int, iy : int):
            def finalise_with_piece_setting():
                cell = board.at(*from_gxy)
                if cell is None or cell.piece is None:
                    self._cancel()
                    return
                cell.piece.change_type(piece_type)
                self._finalise()
            buttons.append(Button(
                (x + ix * board.scale * 24, y + iy * board.scale * 24),
                text,
                finalise_with_piece_setting,
                12,
                board.scale,
                Anchor.TOP_LEFT,
                GroupType.GAME_UI))
            
        add_button(PieceType.QUEEN, "Q", 0, 0)
        add_button(PieceType.ROOK, "R", 1, 0)
        add_button(PieceType.KNIGHT, "K", 0, 1)
        add_button(PieceType.BISHOP, "B", 1, 1)

        self.__interface = buttons
        
    def delete(self):
        for sprite in self.__interface:
            sprite.delete()
        
    def mouse_down(self, event : pg.event.Event) -> bool:
        for sprite in self.__interface:
            if sprite.mouse_down(event):
                return True
        return False
    
    def mouse_up(self, event : pg.event.Event) -> bool:
        for sprite in self.__interface:
            if not sprite.mouse_up(event):
                self._cancel()
                continue
            return True
        return False

    def mouse_move(self, event : pg.event.Event) -> None:
        for sprite in self.__interface:
            sprite.mouse_move(event)
