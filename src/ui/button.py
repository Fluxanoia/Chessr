from enum import auto
from typing import Callable

import pygame as pg

from src.engine.group_manager import DrawingPriority
from src.ui.text import Text
from src.utils.enums import Anchor, ArrayEnum
from src.utils.helpers import Colour, FloatVector, IntVector
from src.utils.sprite import ChessrSprite, GroupType

TEXT_COLOUR : Colour = (240, 240, 240)
ALT_TEXT_COLOUR : Colour = (200, 200, 200)
BG_COLOUR : Colour = (30, 30, 30)
BORDER_COLOUR : Colour = (50, 50, 50)

class ButtonDisplayType(ArrayEnum):
    DEFAULT = auto()
    ALTERNATE = auto()

class Button(ChessrSprite):

    def __init__(
        self,
        xy : FloatVector,
        text : str,
        action : Callable[[], None],
        text_size : float,
        scale : float,
        anchor : Anchor,
        group_type : GroupType,
    ):
        self.__action = action

        self.__text = Text(xy,
                           text_size,
                           scale,Anchor.CENTER,
                           group_type,
                           DrawingPriority.PLUS_ONE)
        self.__text.add_text(ButtonDisplayType.DEFAULT, text, TEXT_COLOUR)
        size = self.__text.add_text(ButtonDisplayType.ALTERNATE, text, ALT_TEXT_COLOUR)
        self.__text.set_text_by_key(ButtonDisplayType.DEFAULT)

        self.__images = {
            ButtonDisplayType.DEFAULT: self.__create_image(size, BG_COLOUR, BORDER_COLOUR, scale),
            ButtonDisplayType.ALTERNATE: self.__create_image(size, BORDER_COLOUR, BG_COLOUR, scale)
        }

        super().__init__(
            xy,
            group_type,
            None,
            self.__images[ButtonDisplayType.DEFAULT],
            scale=scale,
            anchor=anchor
        )

        self.__mouse_down = False

    def __create_image(
        self,
        size : IntVector,
        bg_colour : Colour,
        border_colour : Colour,
        scale : float
    ) -> pg.Surface:
        image = pg.Surface(tuple(map(lambda x : x + 10 * scale, size)), pg.SRCALPHA)
        rect = pg.Rect(0, 0, *image.get_size())
        pg.draw.rect(image, bg_colour, rect, border_radius=20)
        pg.draw.rect(image, border_colour, rect, 5, border_radius=20)
        return image

#region Super Class Overrides

    def set_position(self, xy : FloatVector, preserve_tween : bool = False) -> None:
        super().set_position(xy, preserve_tween)
        
        if self.rect is None:
            raise SystemExit('Unexpected missing rect.')
            
        x, y = self.rect.topleft
        w, h = self.rect.size
        self.__text.set_position((x + w / 2, y + h / 2), preserve_tween)

    def delete(self) -> None:
        self.__text.delete()
        super().delete()

#endregion

#region User Input

    def mouse_down(self, _event : pg.event.Event) -> bool:
        if self.__mouse_intersects():
            self.__mouse_down = True
            self.image = self.__images[ButtonDisplayType.ALTERNATE]
            self.__text.set_text_by_key(ButtonDisplayType.ALTERNATE)
            return True
        return False
    
    def mouse_up(self, _event : pg.event.Event) -> bool:
        if self.__mouse_intersects() and self.__mouse_down:
            self.__action()
            self.__mouse_down = False
            self.image = self.__images[ButtonDisplayType.DEFAULT]
            self.__text.set_text_by_key(ButtonDisplayType.DEFAULT)
            return True
        return False

    def mouse_move(self, _event : pg.event.Event) -> None:
        if not self.__mouse_intersects() and self.__mouse_down:
            self.__mouse_down = False
            self.image = self.__images[ButtonDisplayType.DEFAULT]
            self.__text.set_text_by_key(ButtonDisplayType.DEFAULT)

    def __mouse_intersects(self) -> bool:
        return self.point_intersects(pg.mouse.get_pos())

#endregion
