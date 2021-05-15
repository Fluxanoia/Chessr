from enum import auto
import pygame as pg
from src.enum import ArrayEnum, enum_as_list
from src.files import FileManager
from src.globals import Singleton, instance, scale_rect

class Side(ArrayEnum):
    FRONT = auto()
    BACK = auto()

class PieceType(ArrayEnum):
    QUEEN = auto()
    KING = auto()
    BISHOP = auto()
    ROOK = auto()
    KNIGHT = auto()
    PAWN = auto()

class PieceColour(ArrayEnum):
    WHITE = auto()
    BLACK = auto()
    RED = auto()

class ShadowType(ArrayEnum):
    LIGHT = auto()
    DARK = auto()

class BoardType(ArrayEnum):
    LIGHT = auto()
    DARK = auto()
    MOVE = auto()
    DANGER = auto()
    DEBUG = auto()

class BoardColour(ArrayEnum):
    BEIGE = auto()
    BLACK_WHITE = auto()

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

    def get_sheet(self, scale = 1):
        key = str(scale)
        if key in self.__sheets:
            return self.__sheets[key]
        src = self.__sheets["1"]
        scaled_size = tuple(map(lambda x: int(x * scale), src.get_size()))
        self.__sheets[key] = pg.transform.scale(src, scaled_size)
        return self.__sheets[key]

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
