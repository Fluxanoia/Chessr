from typing import Callable

import pygame as pg
from backend import Move, MoveProperty, PieceType
from src.engine.group_manager import GroupType
from src.sprites.ui.button import Button
from src.utils.enums import Anchor
from src.utils.helpers import IntVector


class PendingMoveAction:

    def __init__(
        self,
        action : MoveProperty,
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
        move : Move,
        finalise : Callable[[], None],
        cancel : Callable[[], None],
        ui_xy : IntVector,
        ui_scale : float
    ) -> 'PendingMoveAction':
        if move.property is MoveProperty.PROMOTION:
            return PiecePromotionMoveAction(move, finalise, cancel, ui_xy, ui_scale)
        raise SystemExit(f'Unexpected pending move type, \'{move.property}\'.')

class PiecePromotionMoveAction(PendingMoveAction):

    def __init__(
        self,
        move : Move,
        finalise: Callable[[], None],
        cancel: Callable[[], None],
        ui_xy : IntVector,
        ui_scale : float
    ) -> None:
        super().__init__(MoveProperty.PROMOTION, finalise, cancel)

        x, y = ui_xy

        buttons : list[Button] = []

        def add_button(piece_type : PieceType, text : str, ix : int, iy : int):
            def finalise_with_piece_setting():
                move.set_promotion_type(piece_type)
                self._finalise()
            buttons.append(Button(
                (x + ix * ui_scale * 24, y + iy * ui_scale * 24),
                text,
                finalise_with_piece_setting,
                12,
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
