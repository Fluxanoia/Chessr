import pygame as pg
from src.game.enums import BoardColour
from src.utils.groups import Groups
from src.utils.globals import MouseButton, instance
from src.game.controllers import Controller

class Board():

    def __init__(self, colour = BoardColour.BLACK_WHITE, scale = 3, cell_scale = 1.25):
        self.__colour = colour
        self.__scale = scale
        self.__cell_scale = scale * cell_scale

        self.__pressed = None
        self.__inactive_timer = None

        self.__controller = Controller(self)
        self.__controller.start()

    def __is_inactive(self):
        if self.__inactive_timer is not None:
            if self.__inactive_timer.has_not_started():
                return False
            if self.__inactive_timer.finished():
                self.__inactive_timer = None
                return False
            return True
        return False
    def update(self):
        if self.__is_inactive():
            return
        self.__controller.update()

    def __get_collision(self, pos):
        for s in reversed(instance(Groups).get_board_cells()):
            if s.collidepoint(pos):
                return s.get_grid_position()
        return None
    def pressed(self, event):
        if self.__is_inactive():
            return
        if event.button == MouseButton.LEFT:
            self.__pressed = self.__get_collision(pg.mouse.get_pos())
    def released(self, event):
        if self.__is_inactive():
            return
        if event.button == MouseButton.LEFT:
            _released = self.__get_collision(pg.mouse.get_pos())
            if self.__pressed == _released:
                self.__clicked(self.__pressed)
    def __clicked(self, gxy):
        if self.__is_inactive():
            return
        self.__controller.click(gxy)

    def get_board_colour(self):
        return self.__colour
    def get_scale(self):
        return self.__scale
    def get_cell_scale(self):
        return self.__cell_scale
    def get_width(self):
        return self.__controller.get_width()
    def get_height(self):
        return self.__controller.get_height()
