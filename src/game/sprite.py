from typing import Any, Optional, cast

import pygame as pg

from src.engine.factory import Factory
from src.engine.group_manager import GroupType
from src.utils.helpers import FloatVector
from src.utils.tween import Tween, TweenType


class ChessrSprite(pg.sprite.DirtySprite):

    def __init__(
        self,
        xy : FloatVector,
        group : Optional[GroupType],
        image : pg.surface.Surface,
        src_rect : Optional[pg.Rect] = None,
        scale : float = 1
    ):
        super().__init__()

        self.rect = None
        self.__group = None

        self.dirty = 2
        self.group = group
        self.image = image
        self.src_rect = src_rect
        self.scale = scale

        self.__position_tween : Optional[Tween] = None
        
        self.set_position(xy)

    def calculate_layer(self, xy : FloatVector) -> int:
        return int(xy[1])
    def calculate_position(self, xy : FloatVector):
        return xy

    def set_position(self, xy : FloatVector, preserve_tween : bool = False) -> None:
        self.__raw_position = xy
        xy = self.calculate_position(xy)
        if self.alive() and isinstance(self.group, GroupType):
            layer = self.calculate_layer(xy)
            Factory.get().group_manager.get_group(self.group).change_layer(self, layer)

        if self.rect is None:
            if self.src_rect is None:
                size = self.image.get_size() if not self.image is None else (0, 0)
            else:
                size = self.src_rect.size
            self.rect = pg.Rect((0, 0), size)

        self.rect.x, self.rect.y = int(xy[0]), int(xy[1])
        
        if not preserve_tween:
            self.__position_tween = None

    def tween_position(self, tween : Tween) -> None:
        self.__position_tween = tween
        self.__position_tween.restart()

    def move(
        self,
        start : Optional[FloatVector],
        end : FloatVector,
        duration : int,
        tween_type : TweenType = TweenType.EASE_OUT_SINE,
        pause : int = 0
    ) -> None:
        if start is None:
            start = self.__raw_position
        self.tween_position(Tween(tween_type, start, end, duration, pause))

    def update(self, *args : list[Any]) -> None:
        if self.__position_tween is not None:
            tween_value = cast(FloatVector, self.__position_tween.value())
            self.set_position(tween_value, True)
            if self.__position_tween.finished():
                self.__position_tween = self.__position_tween.get_chained()

    def point_intersects(self, point : FloatVector) -> bool:
        if self.rect is None:
            return False
        return self.rect.collidepoint(point)

    @property
    def group(self) -> Optional[GroupType]:
        return self.__group

    @group.setter
    def group(self, group : Optional[GroupType]):
        group_manager = Factory.get().group_manager
        if not self.__group is None:
            group_manager.get_group(self.__group).remove(self)
        self.__group = group
        if not self.__group is None:
            group_manager.get_group(self.__group).add(self)

    @property
    def src_rect(self):
        return self.source_rect

    @src_rect.setter
    def src_rect(self, src_rect : Optional[pg.Rect]):
        if src_rect is None:
            self.source_rect = None # type: ignore
        elif getattr(self, 'source_rect', None) is None:
            self.source_rect = src_rect
        else:
            self.source_rect.update(src_rect)
