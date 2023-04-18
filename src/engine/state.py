from typing import Any, Callable

import pygame as pg

from src.engine.factory import Factory
from src.engine.state_type import StateType


class State():

    def __init__(self, state_type : StateType) -> None:
        self.__state_type = state_type

    def provide_state_changer(self, state_changer : Callable[[StateType, Any], None]):
        self.__state_changer = state_changer

    def provide_bounds_getter(self, bounds_getter : Callable[[], pg.rect.Rect]):
        self.__bounds_getter = bounds_getter

    @property
    def state_type(self):
        return self.__state_type
    
    def change_state(self, state_type : StateType, data : Any = None):
        self.__state_changer(state_type, data)
    
#region Game Loop Methods

    def load(self) -> None:
        pass

    def start(self, data : Any) -> None:
        pass

    def stop(self) -> None:
        pass 

    def update(self) -> None:
        pass

#endregion

#region Events

    def _update_view(self):
        self.on_view_change(Factory.get().camera.bounds)

    def on_view_change(self, bounds : pg.rect.Rect):
        pass

    def mouse_down(self, _event : pg.event.Event) -> bool:
        return False
    
    def mouse_up(self, _event : pg.event.Event) -> bool:
        return False

    def mouse_move(self, _event : pg.event.Event) -> None:
        pass

#endregion
