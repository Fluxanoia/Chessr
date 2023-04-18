from typing import Any

import pygame as pg

from src.engine.group_manager import GroupType
from src.engine.state import State, StateType
from src.sprites.ui.spinner import Spinner


class LoadingState(State):

    def __init__(self) -> None:
        super().__init__(StateType.LOADING)
        self.__spinner = Spinner((0, 0), GroupType.LOADING)
        self._update_view()

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

    def on_view_change(self, bounds : pg.rect.Rect):
        self.__spinner.set_position(bounds.center)

    def mouse_down(self, event : pg.event.Event) -> bool:
        return False
    
    def mouse_up(self, event : pg.event.Event) -> bool:
        return False

    def mouse_move(self, event : pg.event.Event) -> None:
        pass

#endregion
