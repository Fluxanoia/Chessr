from enum import auto

import pygame as pg
from backend import PieceType, Player
from src.engine.file_manager import FileManager
from src.engine.spritesheets.spritesheet import Spritesheet
from src.utils.enums import ArrayEnum
from src.utils.helpers import scale_rect


class PieceColour(ArrayEnum):
    WHITE = auto()
    BLACK = auto()
    RED = auto()

class PieceSpritesheet(Spritesheet):

    PIECE_WIDTH = 16
    PIECE_HEIGHT = 48

    def __init__(self, file_manager : FileManager) -> None:
        super().__init__(file_manager, 'pieces.png')

    @staticmethod
    def get_src_rect(
        colour : PieceColour,
        piece_type : PieceType,
        player : Player,
        scale : float = 1
    ) -> pg.Rect:
        player_offset = 0 if player == Player.WHITE else 1
        r = pg.Rect(
            (piece_type.value * 2 + player_offset) * PieceSpritesheet.PIECE_WIDTH,
            colour * PieceSpritesheet.PIECE_HEIGHT,
            PieceSpritesheet.PIECE_WIDTH,
            PieceSpritesheet.PIECE_HEIGHT
        )
        scale_rect(r, scale)
        return r
