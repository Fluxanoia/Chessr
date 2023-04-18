from typing import Any, Optional

import pygame as pg

from src.engine.factory import Factory
from src.engine.group_manager import GroupType
from src.engine.state import State, StateType
from src.logic.board_data import BoardData
from src.logic.board_loader import BoardLoader
from src.sprites.ui.button import Button
from src.sprites.ui.text import Text
from src.utils.enums import Anchor, ViewState


class BoardSelectionState(State):

    def __init__(self) -> None:
        super().__init__(StateType.BOARD_SELECTION)

#region Game Loop Methods

    def load(self) -> None:
        board_loader = BoardLoader()
        board_data : list[BoardData] = []
        paths = Factory.get().file_manager.get_board_paths()

        for path in paths:
            board_data.append(board_loader.load_board(path))

        self.__board_data = tuple(board_data)

        def set_chosen_data_action(data : BoardData):
            self.__chosen_board_data = data

        self.__chosen_board_data : Optional[BoardData] = None
        self.__board_data_buttons = tuple(
            map(lambda x : Button(
                (0, 0),
                x.name,
                lambda : set_chosen_data_action(x),
                36,
                Anchor.TOP_LEFT,
                GroupType.BOARD_SELECTION_UI,
                400),
            self.__board_data))

        self.__title_text = Text(
            (0, 0),
            108,
            Anchor.TOP_LEFT,
            GroupType.BOARD_SELECTION_UI
        )
        self.__title_text.set_text('Board Selection', (240, 240, 240))

        def continue_action():
            self.__title_text.do_slide(
                ViewState.INVISIBLE,
                callback=lambda : self.change_state(StateType.GAME, self.__chosen_board_data))

        self.__continue_button = Button(
            (0, 0),
            'Continue',
            continue_action,
            36,
            Anchor.BOTTOM_RIGHT,
            GroupType.BOARD_SELECTION_UI,
            200)
        
        self._update_view()

    def start(self, data : Any) -> None:
        self.__title_text.do_slide(ViewState.VISIBLE, pause=200)

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
        for (i, button) in enumerate(self.__board_data_buttons):
            button.set_position((left, bounds.top + 300 + i * 85))
        self.__continue_button.set_position((bounds.right - buffer, bounds.bottom - buffer))

    def mouse_down(self, event : pg.event.Event) -> bool:
        for button in self.__board_data_buttons:
            if button.mouse_down(event):
                return True
        return self.__continue_button.mouse_down(event)
    
    def mouse_up(self, event : pg.event.Event) -> bool:
        for button in self.__board_data_buttons:
            if button.mouse_up(event):
                return True
        return self.__continue_button.mouse_up(event)

    def mouse_move(self, event : pg.event.Event) -> None:
        for button in self.__board_data_buttons:
            button.mouse_move(event)
        self.__continue_button.mouse_move(event)

#endregion
