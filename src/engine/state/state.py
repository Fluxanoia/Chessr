from enum import auto
from typing import Callable

import pygame as pg

from src.utils.enums import ArrayEnum


class StateType(ArrayEnum):
    MAIN_MENU = auto()
    GAME = auto()

class State():

    def __init__(self, state_type : StateType) -> None:
        self.__state_type = state_type

    def provide_state_changer(self, state_changer : Callable[[StateType], None]):
        self.__state_changer = state_changer

    @property
    def state_type(self):
        return self.__state_type
    
    def change_state(self, state_type : StateType):
        self.__state_changer(state_type)
    
#region Game Loop Methods

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass 

    def update(self) -> None:
        pass
    
#endregion

#region User Input

    def mouse_down(self, _event : pg.event.Event) -> bool:
        return False
    
    def mouse_up(self, _event : pg.event.Event) -> bool:
        return False

    def mouse_move(self, _event : pg.event.Event) -> None:
        pass

#endregion
