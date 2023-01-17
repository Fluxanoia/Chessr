from enum import auto
from typing import cast

import pygame as pg

from src.utils.enums import ArrayEnum, enum_as_list


class GroupType(ArrayEnum):
    BOARD = auto()
    BOARD_HIGHLIGHT = auto()
    SHADOW = auto()
    PIECE = auto()
    UI = auto()

class GroupManager():

    def __init__(self) -> None:
        self.__groups : dict[GroupType, pg.sprite.LayeredDirty] = {}
        for g in self.__get_types():
            self.__groups[g] = pg.sprite.LayeredDirty()

    def update_groups(self) -> None:
        for g in self.__get_types():
            self.__groups[g].update()

    def draw_groups(self, screen : pg.surface.Surface) -> None:
        for g in self.__get_types():
            self.__groups[g].draw(screen)

    def get_group(self, group : GroupType) -> pg.sprite.LayeredDirty:
        return self.__groups[group]

    def get_sprites(self, group : GroupType) -> list[pg.sprite.Sprite]:
        return self.__groups[group].sprites()

    def __get_types(self) -> tuple[GroupType]:
        types = list(map(lambda x : cast(GroupType, x), enum_as_list(GroupType)))
        types.sort()
        return tuple(types)
