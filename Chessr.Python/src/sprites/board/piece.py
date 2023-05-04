from typing import Any, Optional

import pygame as pg
from backend import PieceType, Player
from src.engine.factory import Factory
from src.engine.group_manager import GroupType
from src.engine.spritesheets.piece_spritesheet import PieceColour
from src.sprites.board.piece_shadow import PieceShadow
from src.sprites.sprite import ChessrSprite
from src.utils.enums import Anchor
from src.utils.helpers import FloatVector, clamp
from src.utils.tween import Tween, TweenType


class Piece(ChessrSprite):

    def __init__(
        self,
        xy : FloatVector,
        scale : float,
        colour : PieceColour,
        piece_type : PieceType,
        player : Player
    ):
        self.__piece_type = piece_type
        self.__player = player
        self.__colour = self.__fallback_colour = colour

        self.__scale = scale
        image = Factory.get().piece_spritesheet.get_sheet(scale)

        self.__lift : float = 0
        self.__lift_tween : Optional[Tween] = None

        self.__shadow = PieceShadow(xy, scale)
        self.__update_shadow_alpha()

        super().__init__(
            xy,
            GroupType.GAME_PIECE,
            None,
            image,
            self.__get_src_rect(scale),
            Anchor.BOTTOM_LEFT)

    def delete(self) -> None:
        self.__shadow.delete()
        super().delete()

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

    def change_type(self, piece_type : PieceType) -> None:
        self.__piece_type = piece_type
        self.src_rect = self.__get_src_rect()

    def highlight(self) -> None:
        self.__colour = PieceColour.RED
        self.src_rect = self.__get_src_rect()

    def unhighlight(self) -> None:
        self.__colour = self.__fallback_colour
        self.src_rect = self.__get_src_rect()

    def __get_src_rect(self, scale : Optional[float] = None) -> pg.Rect:
        scale = scale if not scale is None else self.__scale
        spritesheet = Factory.get().piece_spritesheet
        return spritesheet.get_src_rect(self.__colour, self.__piece_type, self.__player, scale)

    def __update_shadow_alpha(self) -> None:
        alpha = 255 * (1 - self.__lift / 60.0) if not self.__lift == 0 else 0
        self.__shadow.set_alpha(clamp(int(alpha), 0, 255))

    @property
    def player(self):
        return self.__player
