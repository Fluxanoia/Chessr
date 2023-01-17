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
    
    def update(self, *args : list[Any]) -> None:
        position = self.__raw_position
        if self.__position_tween is not None:
            position = cast(FloatVector, self.__position_tween.value())
            if self.__position_tween.finished():
                self.__position_tween = self.__position_tween.get_chained()
        self.set_position(position, True)

    def set_position(self, xy : FloatVector, preserve_tween : bool = False) -> None:
        if self.rect is None:
            if self.src_rect is None:
                size = self.image.get_size() if not self.image is None else (0, 0)
            else:
                size = self.src_rect.size
            self.rect = pg.Rect((0, 0), size)

        self.__raw_position = xy
        
        xy = self._calculate_position(xy)
        if self.alive() and isinstance(self.group, GroupType):
            layer = self._calculate_layer(xy)
            Factory.get().group_manager.get_group(self.group).change_layer(self, layer)

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

    def _calculate_layer(self, xy : FloatVector) -> int:
        return int(xy[1])

    def _calculate_position(self, xy : FloatVector) -> FloatVector:
        return xy

    def point_intersects(self, point : FloatVector) -> bool:
        if self.rect is None:
            return False
        return self.rect.collidepoint(point)

    @property
    def group(self) -> Optional[GroupType]:
        return self.__group

    @group.setter
    def group(self, group : Optional[GroupType]) -> None:
        group_manager = Factory.get().group_manager
        if not self.__group is None:
            group_manager.get_group(self.__group).remove(self)
        self.__group = group
        if not self.__group is None:
            group_manager.get_group(self.__group).add(self)

    @property
    def src_rect(self) -> pg.rect.Rect:
        return self.source_rect

    @src_rect.setter
    def src_rect(self, src_rect : Optional[pg.Rect]) -> None:
        if src_rect is None:
            self.source_rect = None # type: ignore
        elif getattr(self, 'source_rect', None) is None:
            self.source_rect = src_rect
        else:
            self.source_rect.update(src_rect)
