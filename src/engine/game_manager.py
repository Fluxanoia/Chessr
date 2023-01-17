import pygame as pg

from src.game.board import Board
from src.game.controllers import ClassicController


class GameManager():

    def __init__(self) -> None:
        self.__board = Board()
        self.__controller = ClassicController(self.__board)

    def start(self) -> None:
        self.__controller.start()

    def update(self) -> None:
        self.__controller.update()

    def pass_event(self, event : pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            self.__controller.mouse_down(event)
        if event.type == pg.MOUSEBUTTONUP:
            self.__controller.mouse_up(event)
