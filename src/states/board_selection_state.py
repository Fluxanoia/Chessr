from typing import Any, Optional

import pygame as pg

from src.engine.factory import Factory
from src.engine.group_manager import GroupType
from src.engine.state import State, StateType
from src.logic.board_data import BoardData
from src.logic.board_loader import BoardLoader
from src.sprites.ui.button import Button
from src.sprites.ui.text import Text
from src.utils.enums import Anchor, Direction, ViewState


class BoardSelectionState(State):

    def __init__(self) -> None:
        super().__init__(StateType.BOARD_SELECTION)

        scale = 3
        self.__title_text = Text(
            (50, 50),
            32,
            scale,
            Anchor.TOP_LEFT,
            GroupType.BOARD_SELECTION_UI,
            None,
            ViewState.INVISIBLE,
            Direction.LEFT
        )
        self.__title_text.set_text("Board Selection", (240, 240, 240))

        buttons : list[Button] = []

        board_loader = BoardLoader()
        board_data : list[BoardData] = []
        paths = Factory.get().file_manager.get_board_paths()
        for path in paths:
            board_data.append(board_loader.load_board(path))
        self.__board_data = tuple(board_data)

        def set_data(data : BoardData):
            self.__chosen_board_data = data

        buttons.extend(
            map(lambda x : Button(
                (50, 250 + x[0] * scale * 20),
                x[1].name,
                lambda : set_data(x[1]),
                6,
                scale,
                Anchor.BOTTOM_LEFT,
                GroupType.BOARD_SELECTION_UI),
            enumerate(self.__board_data)))

        self.__chosen_board_data : Optional[BoardData] = None

        def action():
            self.__title_text.do_slide(
                ViewState.INVISIBLE,
                callback=lambda : self.change_state(StateType.GAME, self.__chosen_board_data))

        buttons.append(Button(
            (250, 250),
            "Continue",
            action,
            12,
            scale,
            Anchor.BOTTOM_LEFT,
            GroupType.BOARD_SELECTION_UI))
        
        self.__buttons = tuple(buttons)

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
        for button in self.__buttons:
            if button.mouse_down(event):
                return True
        return False
    
    def mouse_up(self, event : pg.event.Event) -> bool:
        for button in self.__buttons:
            if button.mouse_up(event):
                return True
        return False

    def mouse_move(self, event : pg.event.Event) -> None:
        for button in self.__buttons:
            button.mouse_move(event)

#endregion
