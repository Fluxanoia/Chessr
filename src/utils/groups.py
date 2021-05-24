from enum import auto
import pygame as pg
from src.utils.enum import ArrayEnum, enum_as_list
from src.utils.tweens import Tween, TweenType
from src.utils.globals import Singleton, instance

class GroupType(ArrayEnum):
    BOARD = auto()
    SHADOW = auto()
    PIECE = auto()
    UI = auto()

class Groups(Singleton):

    def __init__(self):
        super().__init__()
        self.__groups = {}
        for g in enum_as_list(GroupType):
            self.__groups[g] = pg.sprite.LayeredDirty()

    def update(self):
        types = enum_as_list(GroupType)
        types.sort()
        for g in types:
            self.__groups[g].update()

    def draw(self, screen):
        types = enum_as_list(GroupType)
        types.sort()
        for g in types:
            self.__groups[g].draw(screen)

    def get_group(self, group): return self.__groups[group]
    def get_sprites(self, group): return self.__groups[group].sprites()

class FluxSprite(pg.sprite.DirtySprite):

    # Before running __init__, subclasses should define:
    #   group
    #   image (for sizing, otherwise size manually)

    # These should be defined at some point:
    #   scale

    # Optionally, you can also define:
    #   layer_transform(self, xy)
    #   position_transform(self, xy)

    def __init__(self, xy, srcrect = None):
        super().__init__()
        self.dirty = 2
        self.srcrect = srcrect
        instance(Groups).get_group(self._group).add(self)

        size = self.image.get_size() if self.srcrect is None else self.source_rect.size
        self.rect = pg.Rect((0, 0), size)
        self.set_position(xy)

        self._position_tween = None

    def layer_transform(self, xy):
        return xy[1]
    def position_transform(self, xy):
        return xy

    def set_position(self, xy, preserve_tween = False):
        self._position = xy
        layer = self.layer_transform(xy)
        xy = self.position_transform(xy)
        if self.alive():
            instance(Groups).get_group(self._group).change_layer(self, layer)
        self.rect.x, self.rect.y = xy[0], xy[1]
        if not preserve_tween:
            self._position_tween = None

    def tween_position(self, tween):
        self._position_tween = tween
        self._position_tween.restart()
    def move(self, start, end, duration, _type = TweenType.EASE_OUT_SINE, pause = 0):
        if start is None:
            start = self._position
        self.tween_position(Tween(_type, start, end, duration, pause))

    def update(self, force_position = False):
        if self._position_tween is not None:
            self.set_position(self._position_tween.value(), True)
            if self._position_tween.finished():
                self._position_tween = self._position_tween.get_chained()
        elif force_position:
            self.set_position(self._position, True)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    @property
    def group(self):
        return self._group
    @group.setter
    def group(self, group):
        self._group = group

    @property
    def scale(self):
        return self._scale
    @scale.setter
    def scale(self, scale):
        self._scale = scale

    @property
    def srcrect(self):
        return self.source_rect
    @srcrect.setter
    def srcrect(self, srcrect):
        if srcrect is None:
            self.source_rect = None
        elif getattr(self, 'source_rect', None) is None:
            self.source_rect = srcrect
        else:
            self.source_rect.update(srcrect)
