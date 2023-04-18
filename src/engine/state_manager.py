from typing import Any, Optional

import pygame as pg

from src.engine.factory import Factory
from src.engine.state import State
from src.engine.state_type import StateType
from src.states.board_selection_state import BoardSelectionState
from src.states.game_state import GameState
from src.states.main_menu_state import MainMenuState
from src.utils.enums import enum_as_list


class StateManager():

    def __init__(self) -> None:
        self.__states : tuple[State, ...] = (
            MainMenuState(),
            BoardSelectionState(),
            GameState()
        )
        self.__current_state : Optional[State] = None

        possible_states = len(enum_as_list(StateType))
        distinct_states = len(set(map(lambda x : x.state_type, self.__states)))
        configured_states = len(self.__states)
        if not possible_states == distinct_states or not distinct_states == configured_states:
            raise SystemExit('Invalid state configuration.')

        for state in self.__states:
            state.provide_state_changer(self.set_state)

        self.set_state(StateType.MAIN_MENU, None)

    def set_state(self, state_type : StateType, data : Any):
        if not self.__current_state is None:
            self.__current_state.stop()
        self.__current_state = next(x for x in self.__states if x.state_type == state_type)
        self.__current_state.start(data)

    def update(self) -> None:
        if not self.__current_state is None:
            self.__current_state.update()

    def pass_event(self, event : pg.event.Event) -> None:
        if self.__current_state is None:
            return
        if event.type == pg.MOUSEBUTTONDOWN:
            self.__current_state.mouse_down(event)
        if event.type == pg.MOUSEBUTTONUP:
            self.__current_state.mouse_up(event)
        if event.type == pg.MOUSEMOTION:
            self.__current_state.mouse_move(event)
        if event.type == pg.WINDOWSIZECHANGED:
            bounds = Factory.get().camera.bounds
            for state in self.__states:
                state.on_view_change(bounds)

    @property
    def state_type(self):
        if self.__current_state is None:
            raise SystemExit('Unexpected missing state.')
        return self.__current_state.state_type
