from enum import auto
from typing import Optional, cast

import pygame as pg

from src.engine.state_type import StateType
from src.utils.enums import ArrayEnum, enum_as_list


class GroupType(ArrayEnum):
    LOADING = auto()

    MAIN_MENU_UI = auto()
    
    BOARD_SELECTION_UI = auto()

    GAME_BOARD = auto()
    GAME_PIECE = auto()
    GAME_UI = auto()
    
class DrawingPriority(ArrayEnum):
    MINUS_ONE = auto()
    NORMAL = auto()
    PLUS_ONE = auto()

class GroupManager():

    def __init__(self) -> None:
        all_group_types = list(map(lambda x : cast(GroupType, x), enum_as_list(GroupType)))
        all_group_types.sort()
        self.__all_group_types = tuple(all_group_types)

        priorities = list(map(lambda x : cast(DrawingPriority, x), enum_as_list(DrawingPriority)))
        priorities.sort()
        self.__priorities = tuple(priorities)

        self.__group_types = {
            StateType.LOADING: (
                GroupType.LOADING,
            ),
            StateType.MAIN_MENU: (
                GroupType.MAIN_MENU_UI,
            ),
            StateType.BOARD_SELECTION: (
                GroupType.BOARD_SELECTION_UI,
            ),
            StateType.GAME: (
                GroupType.GAME_BOARD,
                GroupType.GAME_PIECE,
                GroupType.GAME_UI
            )
        }
        self.__groups : dict[GroupType, dict[DrawingPriority, pg.sprite.LayeredDirty]] = {}
        for t in self.__all_group_types:
            self.__groups[t] = {}
            for p in self.__priorities:
                self.__groups[t][p] = pg.sprite.LayeredDirty()

    def update_groups(self, state_type : StateType) -> None:
        for t in self.__group_types[state_type]:
            for p in self.__priorities:
                self.__groups[t][p].update()

    def draw_groups(self, screen : pg.surface.Surface, state_type : StateType) -> None:
        for t in self.__group_types[state_type]:
            for p in self.__priorities:
                self.__groups[t][p].draw(screen)

    def get_group(
        self,
        group : GroupType,
        drawing_priority : Optional[DrawingPriority]
    ) -> pg.sprite.LayeredDirty:
        drawing_priority = DrawingPriority.NORMAL if drawing_priority is None else drawing_priority
        return self.__groups[group][drawing_priority]
    
    def get_groups(
        self,
        group : GroupType
    ) -> tuple[pg.sprite.LayeredDirty, ...]:
        return tuple(self.__groups[group].values())
