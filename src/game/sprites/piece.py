from typing import Any, Optional

import pygame as pg

from src.engine.factory import Factory
from src.game.logic.logic_piece import LogicPiece
from src.game.sprite import ChessrSprite, GroupType
from src.game.sprites.piece_shadow import PieceShadow
from src.utils.enums import Anchor, PieceColour, PieceType, Side
from src.utils.helpers import FloatVector, clamp
from src.utils.tween import Tween, TweenType


class Piece(ChessrSprite, LogicPiece):

    def __init__(
        self,
        xy : FloatVector,
        scale : float,
        colour : PieceColour,
        piece_type : PieceType,
        side : Side
    ):
        LogicPiece.__init__(self, piece_type, side)
        self.__colour = self.__fallback_colour = colour

        image = Factory.get().board_spritesheet.get_sheet(scale)

        self.__lift : float = 0
        self.__lift_tween : Optional[Tween] = None

        self.__shadow = PieceShadow(xy, scale)
        self.__update_shadow_alpha()

        ChessrSprite.__init__(self, xy, GroupType.PIECE, image, self.__get_src_rect(scale), scale, Anchor.BOTTOM_LEFT)

    def delete(self) -> None:
        if not self.group is None:
            Factory.get().group_manager.get_group(self.group).remove(self)
        self.__shadow.delete()
        LogicPiece.delete(self)

    def update(self, *args : list[Any]) -> None:
        if not self.__lift_tween is None:
            self.__lift = self.__lift_tween.value
            self.__update_shadow_alpha()
            if self.__lift_tween.finished():
                self.__lift_tween = None
        super().update()

    def set_position(self, xy : FloatVector, preserve_tween : bool = False) -> None:
        super().set_position(xy, preserve_tween)
        self.__shadow.set_position(xy, preserve_tween)
        if not preserve_tween:
            self.__lift_tween = None

    def _calculate_position(self, xy : FloatVector) -> FloatVector:
        x, y = xy
        return super()._calculate_position((x, y - self.__lift))

    def lift(
        self,
        start : Optional[float],
        end : float,
        duration : int,
        tween_type : TweenType = TweenType.EASE_OUT_SINE,
        pause : int = 0
    ) -> None:
        self.__lift_tween = Tween(
            tween_type,
            self.__lift if start is None else 0,
            end,
            duration,
            pause)
        self.__lift_tween.restart()

    def highlight(self) -> None:
        self.__colour = PieceColour.RED
        self.src_rect = self.__get_src_rect()

    def unhighlight(self) -> None:
        self.__colour = self.__fallback_colour
        self.src_rect = self.__get_src_rect()

    def __get_src_rect(self, scale : Optional[float] = None) -> pg.Rect:
        scale = scale if not scale is None else self.scale
        spritesheet = Factory.get().board_spritesheet
        return spritesheet.get_piece_srcrect(self.__colour, self.type, self.side, scale)

    def __update_shadow_alpha(self) -> None:
        alpha = 255 * (1 - self.__lift / 60.0) if not self.__lift == 0 else 0
        self.__shadow.set_alpha(clamp(int(alpha), 0, 255))
