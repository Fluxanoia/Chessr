from typing import Any, Optional

import pygame as pg
from src.engine.factory import Factory
from src.engine.group_manager import DrawingPriority, GroupType
from src.sprites.sprite import ChessrSprite
from src.utils.enums import Anchor
from src.utils.helpers import FloatVector
from src.utils.timer import Timer


class Spinner(ChessrSprite):

    def __init__(self, xy : FloatVector, group : GroupType, scale : float = 1) -> None:
        self.__scale = scale
        self.__frame = 0
        self.__frame_timer = Timer(75)
        image = Factory.get().spinner_spritesheet.get_sheet(scale)
        super().__init__(xy, group, DrawingPriority.PLUS_ONE, image, self.__get_src_rect(scale), Anchor.CENTER)
    
    def update(self, *args : list[Any], **kwargs : dict[str, Any]) -> None:
        if self.__frame_timer.finished():
            self.__frame += 1
            self.__frame_timer.restart()
        self.src_rect = self.__get_src_rect()
        super().update(*args)

    def __get_src_rect(self, scale : Optional[float] = None) -> pg.Rect:
        scale = scale if not scale is None else self.__scale
        spritesheet = Factory.get().spinner_spritesheet
        return spritesheet.get_src_rect(self.__frame, scale)
