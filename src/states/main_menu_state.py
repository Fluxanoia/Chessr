from typing import Any

import pygame as pg

from src.engine.group_manager import GroupType
from src.engine.state import State, StateType
from src.sprites.ui.button import Button
from src.sprites.ui.text import Text
from src.utils.enums import Anchor, Direction, ViewState


class MainMenuState(State):

    def __init__(self) -> None:
        super().__init__(StateType.MAIN_MENU)

        scale = 3
        self.__title_text = Text(
            (50, 50),
            32,
            scale,
            Anchor.TOP_LEFT,
            GroupType.MAIN_MENU_UI,
            None,
            ViewState.INVISIBLE,
            Direction.LEFT
        )
        self.__title_text.set_text("Chessr", (240, 240, 240))

        def action():
            self.__title_text.do_slide(
                ViewState.INVISIBLE,
                callback=lambda : self.change_state(StateType.BOARD_SELECTION))

        self.__button = Button(
            (50, 250),
            "Play",
            action,
            12,
            scale,
            Anchor.BOTTOM_LEFT,
            GroupType.MAIN_MENU_UI)

#region Game Loop Methods

    def start(self, data : Any) -> None:
        self.__title_text.do_slide(ViewState.VISIBLE, pause=200)

    def stop(self) -> None:
        pass

    def update(self) -> None:
        pass
    
#endregion

#region User Input

    def mouse_down(self, event : pg.event.Event) -> bool:
        return self.__button.mouse_down(event)
    
    def mouse_up(self, event : pg.event.Event) -> bool:
        return self.__button.mouse_up(event)

    def mouse_move(self, event : pg.event.Event) -> None:
        self.__button.mouse_move(event)

#endregion
