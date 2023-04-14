from typing import Any, Optional, cast

import pygame as pg

from src.engine.factory import Factory
from src.engine.group_manager import DrawingPriority, GroupType
from src.utils.enums import Anchor
from src.utils.helpers import FloatVector
from src.utils.tween import Tween, TweenType


class ChessrSprite(pg.sprite.DirtySprite):

    def __init__(
        self,
        xy : FloatVector,
        group : Optional[GroupType],
        drawing_priority : Optional[DrawingPriority],
        image : pg.surface.Surface,
        src_rect : Optional[pg.Rect] = None,
        scale : float = 1,
        anchor : Anchor = Anchor.TOP_LEFT
    ):
        super().__init__()

        self.rect = None
        self.__group = None
        self.__drawing_priority = drawing_priority

        self.dirty = 2
        self.group = group
        self.image = image
        self.src_rect = src_rect
        self.scale = scale

        self._anchor = anchor
        self.__position_tween : Optional[Tween] = None
        
        self.set_position(xy)
    
    def update(self, *args : list[Any]) -> None:
        position = self.__raw_position
        if self.__position_tween is not None:
            position = cast(FloatVector, self.__position_tween.values)
            if self.__position_tween.finished():
                self.__position_tween = self.__position_tween.get_chained()
        self.set_position(position, True)

    def delete(self) -> None:
        if not self.group is None:
            Factory.get().group_manager.get_group(self.group, self.drawing_priority).remove(self)

    def set_position(self, xy : FloatVector, preserve_tween : bool = False) -> None:
        self.rect = pg.Rect((0, 0), self._calculate_size())

        self.__raw_position = xy
        
        xy = self._calculate_position(xy)
        if self.alive() and isinstance(self.group, GroupType):
            layer = self._calculate_layer(xy)
            Factory.get().group_manager.get_group(self.group, self.__drawing_priority).change_layer(self, layer)

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
        x, y = xy
        w, h = self._calculate_size() if self.rect is None else self.rect.size
        if self._anchor == Anchor.TOP_LEFT:
            return xy
        if self._anchor == Anchor.TOP_RIGHT:
            return (x - w, y)
        if self._anchor == Anchor.BOTTOM_LEFT:
            return (x, y - h)
        if self._anchor == Anchor.BOTTOM_RIGHT:
            return (x - w, y - h)
        if self._anchor == Anchor.CENTER:
            return (x - w / 2, y - h / 2)
        raise SystemExit('Unexpected anchor value.')
    
    def _calculate_size(self) -> FloatVector:
        if self.src_rect is None:
            return self.image.get_size() if not self.image is None else (0, 0)
        else:
            return self.src_rect.size

    def point_intersects(self, point : FloatVector) -> bool:
        if self.rect is None:
            return False
        return self.rect.collidepoint(point)

    def __update_grouping(
        self,
        group : Optional[GroupType],
        drawing_priority : Optional[DrawingPriority]
    ):
        group_manager = Factory.get().group_manager
        if not self.__group is None:
            group_manager.get_group(self.__group, self.__drawing_priority).remove(self)
        self.__group = group
        self.__drawing_priority = drawing_priority
        if not self.__group is None:
            group_manager.get_group(self.__group, self.__drawing_priority).add(self)

#region User Input

    def mouse_down(self, _event : pg.event.Event) -> bool:
        return False
    
    def mouse_up(self, _event : pg.event.Event) -> bool:
        return False

    def mouse_move(self, _event : pg.event.Event) -> None:
        pass

#endregion

#region Properties

    @property
    def drawing_priority(self) -> Optional[DrawingPriority]:
        return self.__drawing_priority
    
    @drawing_priority.setter
    def drawing_priority(self, drawing_priority : Optional[DrawingPriority]) -> None:
        self.__update_grouping(self.__group, drawing_priority)

    @property
    def group(self) -> Optional[GroupType]:
        return self.__group

    @group.setter
    def group(self, group : Optional[GroupType]) -> None:
        self.__update_grouping(group, self.__drawing_priority)

    @property
    def src_rect(self) -> Optional[pg.rect.Rect]:
        return self.source_rect

    @src_rect.setter
    def src_rect(self, src_rect : Optional[pg.Rect]) -> None:
        if src_rect is None:
            self.source_rect = None # type: ignore
        elif getattr(self, 'source_rect', None) is None:
            self.source_rect = src_rect
        else:
            self.source_rect.update(src_rect)

    @property
    def pixel_bounds(self) -> Optional[pg.rect.Rect]:
        return self.rect

#endregion
