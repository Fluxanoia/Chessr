import pygame as pg
from src.enum import enum_as_list
from src.groups import Groups
from src.globals import Globals, instance
from src.spritesheet import Spritesheet, BoardColour, BoardType

def config_sprite(sprite, x, y, image, scale):
    sprite.image = pg.transform.scale(image,
        tuple(map(lambda x : x * scale, image.get_size())))
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x, sprite.rect.y = (x, y)

class Piece(pg.sprite.Sprite):

    def __init__(self, x, y, colour, _type, scale):
        super().__init__()
        instance(Groups).add_piece(self)
        config_sprite(self, x, y, instance(Spritesheet).get_piece(colour, _type), scale)

class BoardCell(pg.sprite.Sprite):

    def __init__(self, x, y, colour, _type, scale):
        super().__init__()
        self.layer = y
        instance(Groups).add_board_cell(self)
        config_sprite(self, x, y, instance(Spritesheet).get_board(colour, _type), scale)
        self.__piece = None
        self.__shadow = None

class Board():

    def __init__(self, colour = BoardColour.BLACK_WHITE, scale = 3):
        self.__board = list()

        cell_width = 8
        cell_size = Spritesheet.BOARD_WIDTH * scale
        x_offset, y_offset = map(lambda x : (x - cell_size * cell_width) / 2,
            instance(Globals).get_window_size())
        cell_types = enum_as_list(BoardType)
        for y in range(cell_width):
            for x in range(cell_width):
                self.__board.append(BoardCell(x_offset + x * cell_size,
                    y_offset + y * cell_size, colour,
                    cell_types[(x + y) % len(cell_types)], scale))

    def update(self):
        pass
