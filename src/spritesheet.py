from enum import auto
import pygame as pg
from src.enum import ArrayEnum, enum_as_list
from src.files import FileManager
from src.globals import Singleton, instance, scale_rect

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

class BoardColour(ArrayEnum):
    BEIGE = auto()
    BLACK_WHITE = auto()

class Spritesheet(Singleton):

    PIECE_WIDTH = 16
    PIECE_HEIGHT = 40

    SHADOW_WIDTH = 16
    SHADOW_HEIGHT = 7

    BOARD_WIDTH = 16
    BOARD_HEIGHT = 20

    __instance = None

    def __init__(self):
        super().__init__()
        self.__sheets = { 1 : instance(FileManager).load_image("sprites.png", True) }

    def get_sheet(self, scale = 1):
        if scale in self.__sheets: return self.__sheets[scale]
        self.__sheets[scale] = pg.transform.scale(self.__sheets[1],
            tuple(map(lambda x : x * scale, self.__sheets[1].get_size())))
        return self.__sheets[scale]

    @staticmethod
    def get_piece_src_rect(colour, _type, scale = 1):
        r = pg.Rect(_type * Spritesheet.PIECE_WIDTH, colour * Spritesheet.PIECE_HEIGHT,
            Spritesheet.PIECE_WIDTH, Spritesheet.PIECE_HEIGHT)
        scale_rect(r, scale)
        return r

    @staticmethod
    def get_shadow_src_rect(_type, scale = 1):
        r = pg.Rect(len(enum_as_list(PieceType)) * Spritesheet.PIECE_WIDTH,
            _type * Spritesheet.SHADOW_HEIGHT, Spritesheet.SHADOW_WIDTH, Spritesheet.SHADOW_HEIGHT)
        scale_rect(r, scale)
        return r

    @staticmethod
    def get_board_src_rect(colour, _type, scale = 1):
        offset = len(enum_as_list(PieceType)) * Spritesheet.PIECE_WIDTH + Spritesheet.SHADOW_WIDTH
        r = pg.Rect(offset + _type * Spritesheet.BOARD_WIDTH,
            colour * Spritesheet.BOARD_HEIGHT, Spritesheet.BOARD_WIDTH, Spritesheet.BOARD_HEIGHT)
        scale_rect(r, scale)
        return r
