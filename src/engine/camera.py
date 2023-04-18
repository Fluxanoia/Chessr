import pygame as pg


class Camera:

    def on_view_change(self, screen_width : int, screen_height : int) -> None:
        self.__bounds = pg.rect.Rect(0, 0, screen_width, screen_height)

    @property
    def bounds(self):
        return self.__bounds
