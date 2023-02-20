from enum import auto
from typing import cast

import pygame as pg

from src.engine.state.state import StateType
from src.utils.enums import ArrayEnum, enum_as_list


class GroupType(ArrayEnum):
    MAIN_MENU_UI_LOWER = auto()
    MAIN_MENU_UI_UPPER = auto()

    GAME_BOARD = auto()
    GAME_BOARD_HIGHLIGHT = auto()
    GAME_SHADOW = auto()
    GAME_PIECE = auto()
    GAME_UI_LOWER = auto()
    GAME_UI_UPPER = auto()

class GroupManager():

    def __init__(self) -> None:
        self.__groups : dict[GroupType, pg.sprite.LayeredDirty] = {}
        for g in self.__get_all_types():
            self.__groups[g] = pg.sprite.LayeredDirty()

    def update_groups(self, state_type : StateType) -> None:
        for g in self.__get_types(state_type):
            self.__groups[g].update()

    def draw_groups(self, screen : pg.surface.Surface, state_type : StateType) -> None:
        for g in self.__get_types(state_type):
            self.__groups[g].draw(screen)

    def get_group(self, group : GroupType) -> pg.sprite.LayeredDirty:
        return self.__groups[group]

    def get_sprites(self, group : GroupType) -> list[pg.sprite.Sprite]:
        return self.__groups[group].sprites()

    def __get_types(self, state_type : StateType) -> tuple[GroupType, ...]:
        if state_type == StateType.MAIN_MENU:
            return (
                GroupType.MAIN_MENU_UI_LOWER,
                GroupType.MAIN_MENU_UI_UPPER
            )
        if state_type == StateType.GAME:
            return (
                GroupType.GAME_BOARD,
                GroupType.GAME_BOARD_HIGHLIGHT,
                GroupType.GAME_SHADOW,
                GroupType.GAME_PIECE,
                GroupType.GAME_UI_LOWER,
                GroupType.GAME_UI_UPPER
            )
        raise SystemExit('Unexpected state type.')

    def __get_all_types(self) -> tuple[GroupType, ...]:
        types = list(map(lambda x : cast(GroupType, x), enum_as_list(GroupType)))
        types.sort()
        return tuple(types)
