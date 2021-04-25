import pygame as pg
from src.globals import Singleton

class Groups(Singleton):

    def __init__(self):
        super().__init__()
        self.__piece_group = pg.sprite.LayeredDirty()
        self.__shadow_group = pg.sprite.LayeredDirty()
        self.__board_group = pg.sprite.LayeredDirty()

    def update(self):
        self.__board_group.update()
        self.__shadow_group.update()
        self.__piece_group.update()

    def draw(self, screen):
        self.__board_group.draw(screen)
        self.__shadow_group.draw(screen)
        self.__piece_group.draw(screen)

    def get_pieces(self): return self.__piece_group.sprites()
    def get_shadows(self): return self.__shadow_group.sprites()
    def get_board_cells(self): return self.__board_group.sprites()

    def get_piece_group(self): return self.__piece_group
    def get_shadow_group(self): return self.__shadow_group
    def get_board_group(self): return self.__board_group
