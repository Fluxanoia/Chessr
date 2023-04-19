from enum import auto
from typing import Callable, Optional

import pygame as pg

from src.engine.group_manager import DrawingPriority
from src.sprites.sprite import ChessrSprite, GroupType
from src.sprites.ui.text import Text
from src.utils.enums import Anchor, ArrayEnum
from src.utils.helpers import Colour, FloatVector, IntVector

TEXT_COLOUR : Colour = (240, 240, 240)
ALT_TEXT_COLOUR : Colour = (200, 200, 200)
BG_COLOUR : Colour = (30, 30, 30)
BORDER_COLOUR : Colour = (50, 50, 50)

class ButtonDisplayType(ArrayEnum):
    DEFAULT = auto()
    HOVERED = auto()
    PRESSED = auto()

class Button(ChessrSprite):

    def __init__(
        self,
        xy : FloatVector,
        text : str,
        action : Callable[[], None],
        text_size : float,
        anchor : Anchor,
        group_type : GroupType,
        min_width : Optional[int] = None
    ):
        self.__action = action

        self.__text = Text(xy,
                           text_size,
                           Anchor.CENTER,
                           group_type,
                           DrawingPriority.PLUS_ONE)
        size = self.__text.add_text(ButtonDisplayType.DEFAULT, text, TEXT_COLOUR)
        self.__text.add_text(ButtonDisplayType.HOVERED, text, TEXT_COLOUR)
        self.__text.add_text(ButtonDisplayType.PRESSED, text, ALT_TEXT_COLOUR)
        self.__text.set_text_by_key(ButtonDisplayType.DEFAULT)

        self.__images = {
            ButtonDisplayType.DEFAULT: self.__create_image(size, BG_COLOUR, BORDER_COLOUR, min_width),
            ButtonDisplayType.HOVERED: self.__create_image(size, BG_COLOUR, ALT_TEXT_COLOUR, min_width),
            ButtonDisplayType.PRESSED: self.__create_image(size, BORDER_COLOUR, BG_COLOUR, min_width)
        }

        super().__init__(
            xy,
            group_type,
            None,
            self.__images[ButtonDisplayType.DEFAULT],
            anchor=anchor
        )

        self.__mouse_down = False
        self.__hovering = False

    def __create_image(
        self,
        size : IntVector,
        bg_colour : Colour,
        border_colour : Colour,
        min_width : Optional[int]
    ) -> pg.Surface:
        buffer = 30
        width, height = size
        width = (width if min_width is None else max(min_width, width)) + buffer
        height += buffer
        image = pg.Surface((width, height), pg.SRCALPHA)
        rect = pg.Rect(0, 0, width, height)
        pg.draw.rect(image, bg_colour, rect, border_radius=20)
        pg.draw.rect(image, border_colour, rect, 5, border_radius=20)
        return image
    
    def __change_display_type(self, display_type : ButtonDisplayType):
        self.image = self.__images[display_type]
        self.__text.set_text_by_key(display_type)

#region Super Class Overrides

    def set_position(self, xy : FloatVector, preserve_tween : bool = False) -> None:
        super().set_position(xy, preserve_tween)
        
        if self.dst_rect is None:
            raise SystemExit('Unexpected missing dst_rect.')
            
        x, y = self.dst_rect.topleft
        w, h = self.dst_rect.size
        self.__text.set_position((x + w / 2, y + h / 2), preserve_tween)

    def delete(self) -> None:
        self.__text.delete()
        super().delete()

#endregion

#region User Input

    def mouse_down(self, _event : pg.event.Event) -> bool:
        if self.__mouse_intersects():
            self.__mouse_down = True
            self.__change_display_type(ButtonDisplayType.PRESSED)
            return True
        return False
    
    def mouse_up(self, _event : pg.event.Event) -> bool:
        if self.__mouse_intersects() and self.__mouse_down:
            self.__action()
            self.__mouse_down = False
            self.__change_display_type(ButtonDisplayType.DEFAULT)
            return True
        return False

    def mouse_move(self, _event : pg.event.Event) -> None:
        hovering = self.__mouse_intersects()
        if hovering:
            if not self.__hovering:
                self.__change_display_type(ButtonDisplayType.HOVERED)
        else:
            if self.__hovering:
                self.__change_display_type(ButtonDisplayType.DEFAULT)
            if self.__mouse_down:
                self.__mouse_down = False
        self.__hovering = hovering

    def __mouse_intersects(self) -> bool:
        return self.point_intersects(pg.mouse.get_pos())

#endregion
