from enum import auto

import pygame as pg
from src.engine.file_manager import FileManager
from src.engine.spritesheets.spritesheet import Spritesheet
from src.utils.enums import ArrayEnum
from src.utils.helpers import scale_rect


class ShadowType(ArrayEnum):
    LIGHT = auto()
    DARK = auto()

class ShadowSpritesheet(Spritesheet):

    SHADOW_WIDTH = 16
    SHADOW_HEIGHT = 7

    def __init__(self, file_manager : FileManager) -> None:
        super().__init__(file_manager, 'shadows.png')

    @staticmethod
    def get_src_rect(shadow_type : ShadowType, scale : float = 1) -> pg.Rect:
        r = pg.Rect(
            0,
            shadow_type * ShadowSpritesheet.SHADOW_HEIGHT,
            ShadowSpritesheet.SHADOW_WIDTH,
            ShadowSpritesheet.SHADOW_HEIGHT
        )
        scale_rect(r, scale)
        return r
