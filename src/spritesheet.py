from enum import auto
import pygame as pg
from src.enum import ArrayEnum
from src.files import FileManager
from src.globals import Singleton, instance

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

class PieceShadow(ArrayEnum):
    LIGHT = auto()
    DARK = auto()

class BoardType(ArrayEnum):
    LIGHT = auto()
    DARK = auto()

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
        self.__sheet = instance(FileManager).load_image("sprites.png", True)

        left = 0
        rect = pg.Rect(0, 0, 0, 0)

        self.__pieces = list()
        rect.update(left, 0, Spritesheet.PIECE_WIDTH, Spritesheet.PIECE_HEIGHT)
        for colour in PieceColour:
            rect.top = colour * Spritesheet.PIECE_HEIGHT
            row = list()
            for _type in PieceType:
                rect.left = _type * Spritesheet.PIECE_WIDTH
                row.append(self.__sheet.subsurface(rect))
            self.__pieces.append(row)

        left = rect.left + Spritesheet.PIECE_WIDTH

        self.__shadows = list()
        rect.update(left, 0, Spritesheet.SHADOW_WIDTH, Spritesheet.SHADOW_HEIGHT)
        for shadow in PieceShadow:
            rect.top = shadow * Spritesheet.SHADOW_HEIGHT
            self.__shadows.append(self.__sheet.subsurface(rect))

        left += Spritesheet.SHADOW_WIDTH

        self.__boards = list()
        rect.update(left, 0, Spritesheet.BOARD_WIDTH, Spritesheet.BOARD_HEIGHT)
        for colour in BoardColour:
            rect.top = colour * Spritesheet.BOARD_HEIGHT
            row = list()
            for _type in BoardType:
                rect.left = left + _type * Spritesheet.BOARD_WIDTH
                row.append(self.__sheet.subsurface(rect))
            self.__boards.append(row)

    def get_piece(self, colour, _type):
        return self.__pieces[colour][_type]

    def get_shadow(self, _type):
        return self.__shadows[_type]

    def get_board(self, colour, _type):
        return self.__boards[colour][_type]
