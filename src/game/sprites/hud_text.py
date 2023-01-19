from typing import Any, Optional

import pygame as pg

from src.engine.factory import Factory
from src.game.sprite import ChessrSprite, GroupType
from src.utils.helpers import Colour, FloatVector, add_vectors


class HudText(ChessrSprite):

    def __init__(
        self,
        xy : FloatVector,
        size : float,
        scale : float,
    ):
        self.__font = Factory.get().file_manager.load_default_font(int(size * scale))
        self.__cache : dict[Any, pg.surface.Surface] = {}

        super().__init__(xy, GroupType.UI, pg.Surface((0, 0)), scale = scale)

    def add_text(
        self,
        key : Any,
        text : str,
        colour : Colour,
        outline_size : Optional[int] = None,
        outline_colour : Optional[Colour] = None
    ) -> None:
        surface = self.__get_text(text, colour, outline_size, outline_colour)
        
        if not self.__cache.get(key, None) is None:
            raise SystemExit('This cache key is already populated.')

        self.__cache[key] = surface

    def set_text_by_key(self, key : Any) -> None:
        surface = self.__cache.get(key, None)
        if surface is None:
            raise SystemExit('There is no image at this cache key.')
        
        self.visible = 1
        self.image = surface

    def set_text(
        self,
        text : str,
        colour : Colour,
        outline_size : Optional[int] = None,
        outline_colour : Optional[Colour] = None
    ) -> None:
        self.visible = 1
        self.image = self.__get_text(text, colour, outline_size, outline_colour)

    def clear(self) -> None:
        self.visible = 0

    def __get_text(
        self,
        text : str,
        colour : Colour,
        outline_size : Optional[int] = None,
        outline_colour : Optional[Colour] = None
    ) -> pg.surface.Surface:
        rendered_text = self.__font.render(text, True, colour)
        if outline_colour is None or outline_size is None:
            return rendered_text
            
        rendered_outline_text = self.__font.render(text, True, outline_colour)
        rendered_outline_text_size = rendered_outline_text.get_size()
        surface = pg.surface.Surface(
                add_vectors(rendered_outline_text_size, (2 * outline_size, 2 * outline_size)),
                flags = pg.SRCALPHA)
        
        offsets = range(-outline_size, 2 * outline_size, 1)
        for x in offsets:
            for y in offsets:
                if x == y == 0:
                    continue
                surface.blit(rendered_outline_text, (x + outline_size, y + outline_size))

        surface.blit(rendered_text, (outline_size, outline_size))
        return surface

    def _calculate_position(self, xy : FloatVector) -> FloatVector:
        if self.rect is None:
            return xy
        x, y = xy
        w, h = self.rect.size
        return (x - w, y - h - self.__font.get_descent())
