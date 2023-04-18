from typing import Any

import pygame as pg

from src.engine.group_manager import GroupType
from src.engine.state import State, StateType
from src.sprites.ui.button import Button
from src.sprites.ui.text import Text
from src.utils.enums import Anchor


class MainMenuState(State):

    def __init__(self) -> None:
        super().__init__(StateType.MAIN_MENU)

        self.__title_text = Text(
            (0, 0),
            108,
            Anchor.TOP_LEFT,
            GroupType.MAIN_MENU_UI
        )
        self.__title_text.set_text('Chessr', (240, 240, 240))

        self.__button = Button(
            (0, 0),
            'Play',
            lambda : self.change_state(StateType.BOARD_SELECTION),
            36,
            Anchor.TOP_LEFT,
            GroupType.MAIN_MENU_UI,
            300)
        
        self._update_view()

#region Game Loop Methods

    def start(self, data : Any) -> None:
        pass

    def stop(self) -> None:
        pass

    def update(self) -> None:
        pass
    
#endregion

#region Events

    def on_view_change(self, bounds : pg.rect.Rect):
        buffer = 50
        left = bounds.left + buffer
        self.__title_text.set_position((left, bounds.top + buffer))
        self.__button.set_position((left, bounds.top + 300))

    def mouse_down(self, event : pg.event.Event) -> bool:
        return self.__button.mouse_down(event)
    
    def mouse_up(self, event : pg.event.Event) -> bool:
        return self.__button.mouse_up(event)

    def mouse_move(self, event : pg.event.Event) -> None:
        self.__button.mouse_move(event)

#endregion
