from enum import auto
from typing import Optional, cast

import pygame as pg

from src.engine.state_type import StateType
from src.utils.enums import ArrayEnum, enum_as_list


class GroupType(ArrayEnum):
    MAIN_MENU_UI = auto()
    
    BOARD_SELECTION_UI = auto()

    GAME_BOARD = auto()
    GAME_PIECE = auto()
    GAME_UI = auto()

    @staticmethod
    def get_group_types(state_type : StateType):
        if state_type == StateType.MAIN_MENU:
            return (
                GroupType.MAIN_MENU_UI,
            )
        if state_type == StateType.BOARD_SELECTION:
            return (
                GroupType.BOARD_SELECTION_UI,
            )
        if state_type == StateType.GAME:
            return (
                GroupType.GAME_BOARD,
                GroupType.GAME_PIECE,
                GroupType.GAME_UI
            )
        raise SystemExit('Unexpected state type.')
    
class DrawingPriority(ArrayEnum):
    MINUS_ONE = auto()
    NORMAL = auto()
    PLUS_ONE = auto()

class GroupManager():

    def __init__(self) -> None:
        priorities = self.__get_all_priorities()
        self.__groups : dict[GroupType, dict[DrawingPriority, pg.sprite.LayeredDirty]] = {}
        for t in self.__get_all_types():
            self.__groups[t] = {}
            for p in priorities:
                self.__groups[t][p] = pg.sprite.LayeredDirty()

    def update_groups(self, state_type : StateType) -> None:
        for t in GroupType.get_group_types(state_type):
            for p in self.__get_all_priorities():
                self.__groups[t][p].update()

    def draw_groups(self, screen : pg.surface.Surface, state_type : StateType) -> None:
        for t in GroupType.get_group_types(state_type):
            for p in self.__get_all_priorities():
                self.__groups[t][p].draw(screen)

    def get_group(
        self,
        group : GroupType,
        drawing_priority : Optional[DrawingPriority]
    ) -> pg.sprite.LayeredDirty:
        drawing_priority = DrawingPriority.NORMAL if drawing_priority is None else drawing_priority
        return self.__groups[group][drawing_priority]

    def get_sprites(self, group_type : GroupType) -> dict[DrawingPriority, list[pg.sprite.Sprite]]:
        sprites : dict[DrawingPriority, list[pg.sprite.Sprite]] = {}
        for priority in self.__get_all_priorities():
            sprites[priority] = self.__groups[group_type][priority].sprites()
        return sprites
    
    def get_flattened_sprites(self, group_type : GroupType) -> list[pg.sprite.Sprite]:
        flattened : list[pg.sprite.Sprite] = []
        sprites = self.get_sprites(group_type)
        for p in self.__get_all_priorities():
            flattened.extend(sprites[p])
        return flattened

    def __get_all_types(self) -> tuple[GroupType, ...]:
        types = list(map(lambda x : cast(GroupType, x), enum_as_list(GroupType)))
        types.sort()
        return tuple(types)
    
    def __get_all_priorities(self) -> tuple[DrawingPriority, ...]:
        priorities = list(map(lambda x : cast(DrawingPriority, x), enum_as_list(DrawingPriority)))
        priorities.sort()
        return tuple(priorities)
