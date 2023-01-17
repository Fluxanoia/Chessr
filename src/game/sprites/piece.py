from typing import Any, Optional

import pygame as pg

from src.engine.factory import Factory
from src.game.logic.piece_tag import PieceTag, PieceTagType
from src.game.sprite import ChessrSprite, GroupType
from src.game.sprites.piece_shadow import PieceShadow
from src.utils.enums import PieceColour, PieceType, Side
from src.utils.helpers import FloatVector, clamp
from src.utils.tween import Tween, TweenType


class Piece(ChessrSprite):

    def __init__(
        self,
        xy : FloatVector,
        scale : float,
        colour : PieceColour,
        piece_type : PieceType,
        side : Side
    ):
        self.__colour = colour
        self.__type = piece_type
        self.__side = side
        self.__tags : list[PieceTag] = []

        image = Factory.get().board_spritesheet.get_sheet(scale)

        self.__lift : float = 0
        self.__lift_tween : Optional[Tween] = None

        self.__shadow = PieceShadow(xy, scale)
        self.update_shadow_alpha()

        super().__init__(xy, GroupType.PIECE, image, self.get_src_rect(scale), scale)

    def update(self, *args : list[Any]) -> None:
        if not self.__lift_tween is None:
            self.__lift = self.__lift_tween.get_single_value()
            self.update_shadow_alpha()
            if self.__lift_tween.finished():
                self.__lift_tween = None
        super().update()

    def calculate_position(self, xy : FloatVector) -> FloatVector:
        rect_height = self.rect.h if not self.rect is None else 0
        return (xy[0], xy[1] - rect_height - self.__lift)

    def set_position(self, xy : FloatVector, preserve_tween : bool = False):
        super().set_position(xy, preserve_tween)
        self.__shadow.set_position(xy, preserve_tween)
        if not preserve_tween:
            self.__lift_tween = None

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

    def set_data(self, colour : PieceColour, piece_type : PieceType, side : Side):
        self.__colour = colour
        self.__type = piece_type
        self.__side = side
        self.src_rect = self.get_src_rect()

    def get_src_rect(self, scale : Optional[float] = None) -> pg.Rect:
        scale = scale if not scale is None else self.scale
        spritesheet = Factory.get().board_spritesheet
        return spritesheet.get_piece_srcrect(self.__colour, self.__type, self.__side, scale)

    def update_shadow_alpha(self):
        alpha = 255 * (1 - self.__lift / 60.0) if not self.__lift == 0 else 0
        self.__shadow.set_alpha(clamp(int(alpha), 0, 255))

    def add_tag(self, tag : PieceTag):
        self.__tags.append(tag)

    def has_tag(self, tag_type : PieceTagType):
        return tag_type in map(lambda x : x.type, self.__tags)

    @property
    def type(self) -> PieceType:
        return self.__type
    
    @property
    def side(self) -> Side:
        return self.__side
