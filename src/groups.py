import pygame as pg
from src.globals import Singleton

class Groups(Singleton):

    def __init__(self):
        super().__init__()
        self.__piece_group = pg.sprite.LayeredUpdates()
        self.__shadow_group = pg.sprite.LayeredUpdates()
        self.__board_group = pg.sprite.LayeredUpdates()

    def add_piece(self, piece):
        self.__piece_group.add(piece)

    def add_shadow(self, shadow):
        self.__shadow_group.add(shadow)

    def add_board_cell(self, cell):
        self.__board_group.add(cell)

    def update(self):
        self.__board_group.update()
        self.__shadow_group.update()
        self.__piece_group.update()

    def draw(self, screen):
        self.__board_group.draw(screen)
        self.__shadow_group.draw(screen)
        self.__piece_group.draw(screen)
