import pygame as pg

from src.engine.file_manager import FileManager
from src.engine.spritesheets.spritesheet import Spritesheet
from src.utils.helpers import scale_rect


class SpinnerSpritesheet(Spritesheet):

    SPINNER_WIDTH = SPINNER_HEIGHT = 172

    def __init__(self, file_manager : FileManager) -> None:
        super().__init__(file_manager, 'spinner.png')

    @staticmethod
    def get_src_rect(
        frame : int,
        scale : float = 1
    ) -> pg.Rect:
        index = frame % 19
        row = 1 if index >= 10 else 0 
        column = index % 10
        r = pg.Rect(
            column * SpinnerSpritesheet.SPINNER_WIDTH,
            row * SpinnerSpritesheet.SPINNER_HEIGHT,
            SpinnerSpritesheet.SPINNER_WIDTH,
            SpinnerSpritesheet.SPINNER_HEIGHT
        )
        scale_rect(r, scale)
        return r
