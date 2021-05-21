import pygame as pg
from src.game.enums import PieceType, Side
from src.utils.enum import enum_as_list
from src.utils.files import FileManager
from src.utils.globals import Singleton, instance, scale_rect

class Spritesheet(Singleton):

    PIECE_WIDTH = 16
    PIECE_HEIGHT = 48

    SHADOW_WIDTH = 16
    SHADOW_HEIGHT = 7

    BOARD_WIDTH = 16
    BOARD_HEIGHT = 20

    def __init__(self):
        super().__init__()
        self.__sheets = { "1" : instance(FileManager).load_image("sprites.png", True) }
#
    def get_sheet(self, scale = 1):
        key = str(scale)
        if key in self.__sheets:
            return self.__sheets[key]
        src = self.__sheets["1"]
        scaled_size = tuple(map(lambda x: int(x * scale), src.get_size()))
        self.__sheets[key] = pg.transform.scale(src, scaled_size)
        return self.__sheets[key]

    def get_image(self, srcrect, scale):
        image = pg.Surface(srcrect.size, pg.SRCALPHA, 32).convert_alpha()
        image.blit(self.get_sheet(scale), (0, 0), srcrect)
        return image
    @staticmethod
    def get_piece_src_rect(colour, _type, side, scale = 1):
        sides = len(enum_as_list(Side))
        r = pg.Rect((_type * sides + side) * Spritesheet.PIECE_WIDTH,
                    colour * Spritesheet.PIECE_HEIGHT,
                    Spritesheet.PIECE_WIDTH, Spritesheet.PIECE_HEIGHT)
        scale_rect(r, scale)
        return r
    @staticmethod
    def __piece_width():
        return len(enum_as_list(PieceType)) * len(enum_as_list(Side)) * Spritesheet.PIECE_WIDTH

    @staticmethod
    def get_shadow_src_rect(_type, scale = 1):
        r = pg.Rect(Spritesheet.__piece_width(),
                    _type * Spritesheet.SHADOW_HEIGHT,
                    Spritesheet.SHADOW_WIDTH,
                    Spritesheet.SHADOW_HEIGHT)
        scale_rect(r, scale)
        return r
    @staticmethod
    def __shadow_width():
        return Spritesheet.__piece_width() + Spritesheet.SHADOW_WIDTH

    @staticmethod
    def get_board_src_rect(colour, _type, scale = 1):
        r = pg.Rect(Spritesheet.__shadow_width() + _type * Spritesheet.BOARD_WIDTH,
                    colour * Spritesheet.BOARD_HEIGHT,
                    Spritesheet.BOARD_WIDTH,
                    Spritesheet.BOARD_HEIGHT)
        scale_rect(r, scale)
        return r
