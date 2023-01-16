import pygame as pg

from src.game.board import Board
from src.game.controllers import ClassicController


class GameManager():

    def __init__(self):
        self.__board = Board()
        self.__controller = ClassicController(self.__board)

    def start(self):
        self.__controller.start()

    def update(self):
        self.__controller.update()

    def pass_event(self, event : pg.event.Event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.__controller.mouse_down(event)
        if event.type == pg.MOUSEBUTTONUP:
            self.__controller.mouse_up(event)
