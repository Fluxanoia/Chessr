from typing import Any, Callable, Optional

import pygame as pg

from src.engine.factory import Factory
from src.game.sprite import ChessrSprite, GroupType
from src.utils.enums import Anchor, Direction, ViewState
from src.utils.helpers import Colour, FloatVector, add_vectors
from src.utils.tween import Tween, TweenType


class HudText(ChessrSprite):

    def __init__(
        self,
        xy : FloatVector,
        size : float,
        scale : float,
        anchor : Anchor,
        state : ViewState = ViewState.VISIBLE,
        slide_direction : Optional[Direction] = None
    ):
        self.__slide : float = 1 if state == ViewState.VISIBLE else 0
        self.__slide_direction : Optional[Direction] = slide_direction
        self.__slide_tween : Optional[Tween] = None

        self.__font = Factory.get().file_manager.load_default_font(int(size * scale))
        self.__cache : dict[Any, pg.surface.Surface] = {}

        super().__init__(xy, GroupType.UI, pg.Surface((0, 0)), scale=scale, anchor=anchor)

#region Super Class Methods

    def update(self, *args : list[Any]) -> None:
        if not self.__slide_tween is None:
            self.__slide = self.__slide_tween.value
            if self.__slide_tween.finished():
                callback = self.__slide_tween.get_callback()
                if not callback is None:
                    callback()
                self.__slide_tween = self.__slide_tween.get_chained()
        super().update()

    def _calculate_size(self) -> FloatVector:
        if self.image is None:
            return (0, 0)
        
        size = self.image.get_size()
        w, h = size
        if self.__slide_direction in (Direction.LEFT, Direction.RIGHT):
            size = (self.__slide * w, h)
            x = 0 if self.__slide_direction == Direction.RIGHT else w - size[0]
            self.src_rect = pg.Rect(x, 0, *size)
        elif self.__slide_direction in (Direction.TOP, Direction.BOTTOM):
            size = (w, self.__slide * h)
            y = 0 if self.__slide_direction == Direction.BOTTOM else h - size[1]
            self.src_rect = pg.Rect(0, y, *size)

        return size
    
    def _calculate_position(self, xy : FloatVector) -> FloatVector:
        x, y = xy
        if self._anchor in (Anchor.BOTTOM_LEFT, Anchor.BOTTOM_RIGHT):
            y = y - self.__font.get_descent()
        return super()._calculate_position((x, y))
    
#endregion

#region Image Logic

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
        self.image = surface

    def set_text(
        self,
        text : str,
        colour : Colour,
        outline_size : Optional[int] = None,
        outline_colour : Optional[Colour] = None
    ) -> None:
        self.image = self.__get_text(text, colour, outline_size, outline_colour)

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

#endregion

#region Sliding Logic

    def is_visible(self) -> bool:
        return self.__slide > 0
    
    def is_tweening_to(self, state : ViewState) -> bool:
        if self.__slide_tween is None:
            return False
        return self.__slide_tween.end_value == (1 if state == ViewState.VISIBLE else 0)

    def set_state(self, state : ViewState):
        self.__slide_tween = None
        self.__slide = 1 if state == ViewState.VISIBLE else 0

    def set_text_with_slide_by_key(self, key : Any, direction : Optional[Direction] = None) -> None:
        self.__slide_with_callback(direction, lambda : self.set_text_by_key(key))

    def set_text_with_slide(
        self,
        text : str,
        colour : Colour,
        direction : Optional[Direction] = None,
        outline_size : Optional[int] = None,
        outline_colour : Optional[Colour] = None
    ) -> None:
        self.__slide_with_callback(direction, lambda : self.set_text(text, colour, outline_size, outline_colour))

    def do_slide(
        self,
        state : ViewState,
        direction : Optional[Direction] = None,
        pause : int = 0
    ) -> None:
        self.__do_slide(state, direction, pause=pause)

    def __do_slide(
        self,
        state : ViewState,
        direction : Optional[Direction] = None,
        chain : Optional[Tween] = None,
        callback : Optional[Callable[[], None]] = None,
        pause : int = 0
    ) -> None:
        tween = self.__get_slide_tween(state, chain, callback, pause)

        if tween is None:
            if not callback is None:
                callback()
            tween = chain

        self.__slide_tween = tween
        if not direction is None:
            self.__slide_direction = direction

    def __slide_with_callback(self, direction : Optional[Direction], callback : Callable[[], None]):
        chain = self.__get_slide_tween(ViewState.VISIBLE, start=0, callback=callback)
        self.__do_slide(ViewState.INVISIBLE, direction, chain, callback)

    def __at_destination(self, dest : float):
        return not self.__slide_tween is None and self.__slide_tween.value == dest

    def __get_slide_tween(
        self,
        state : ViewState,
        chain : Optional[Tween] = None,
        callback : Optional[Callable[[], None]] = None,
        pause : int = 0,
        start : Optional[float] = None
    ) -> Optional[Tween]:
        tween_type = TweenType.EASE_IN_QUAD if state == ViewState.VISIBLE else TweenType.EASE_OUT_QUAD
        start = self.__slide if start is None else start
        end = 1 if state == ViewState.VISIBLE else 0

        if self.__at_destination(end):
            self.__slide = end
            return None

        return Tween(tween_type, start, end, 300, pause, chain, callback)

#endregion
