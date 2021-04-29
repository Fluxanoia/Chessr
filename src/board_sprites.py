import pygame as pg
from src.tweens import Tween, TweenType
from src.groups import Groups
from src.globals import instance
from src.spritesheet import Spritesheet, ShadowType

class BoardSprite(pg.sprite.DirtySprite):

    def __init__(self, sheet, xy, scale):
        super().__init__()
        self.dirty = 2
        self.image = sheet
        self._scale = scale
        self.source_rect = self.get_src_rect()
        self.rect = pg.Rect((0, 0), self.source_rect.size)
        self.layer = self.position_transform(xy)[1]
        self.get_group().add(self)
        self.set_position(xy)
        self.__position_tween = None

    def get_src_rect(self): return pg.Rect(0, 0, 0, 0)
    def get_group(self): return None

    def set_position(self, xy, preserve_tween = False):
        xy = self.position_transform(xy)
        self.get_group().change_layer(self, xy[1])
        self.rect.x, self.rect.y = xy[0], xy[1]
        if not preserve_tween:
            self.__position_tween = None
    def position_transform(self, xy):
        return xy

    def tween_position(self, tween):
        self.__position_tween = tween
        self.__position_tween.restart()

    def update(self):
        if self.__position_tween is not None:
            self.set_position(self.__position_tween.value(), True)
            if self.__position_tween.finished():
                self.__position_tween = self.__position_tween.get_chained()

    def set_src_rect(self, srcrect):
        if self.source_rect is None:
            self.source_rect = srcrect
        else:
            self.source_rect.update(srcrect)
    def update_src_rect(self):
        self.set_src_rect(self.get_src_rect())

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)


class Piece(BoardSprite):

    def __init__(self, sheet, xy, colour, _type, scale):
        self.__colour = colour
        self.__type = _type
        super().__init__(sheet, xy, scale)

    def position_transform(self, xy):
        return (xy[0], xy[1] - self.rect.h)
    def get_src_rect(self):
        return Spritesheet.get_piece_src_rect(self.__colour, self.__type, self._scale)
    def get_group(self):
        return instance(Groups).get_piece_group()
    def set_colour_and_type(self, colour, _type):
        self.__colour = colour
        self.__type = _type
        self.update_src_rect()

    def move(self, start, end, duration, pause = 0):
        self.tween_position(Tween(TweenType.EASE_OUT_SINE,
                                  start, end, duration, pause))

    def get_colour(self): return self.__colour
    def get_type(self): return self.__type
    def get_bottom_left(self): return self.rect.bottomleft


class Shadow(BoardSprite):

    def __init__(self, sheet, xy, _type, scale):
        self.__type = _type
        super().__init__(sheet, xy, scale)

    def position_transform(self, xy):
        return (xy[0], xy[1] - self.rect.h - 2 * self._scale)
    def get_src_rect(self):
        return Spritesheet.get_shadow_src_rect(self.__type, self._scale)
    def get_group(self):
        return instance(Groups).get_shadow_group()

    def set_type(self, _type):
        self.__type = _type
        self.update_src_rect()


class BoardCell(BoardSprite):

    def __init__(self, sheet, gxy, xy, colour, _type, scale):
        self.__colour = colour
        self.__type = _type
        super().__init__(sheet, xy, scale)

        self.__grid_position = gxy
        self.__selected = False
        self.__fallback_type = None

        self.__piece = Piece(self.image, self.get_bottom_left(), 0, 0, scale)
        self.__piece.visible = 0
        self.__shadow = Shadow(
            sheet, self.get_bottom_left(), ShadowType.LIGHT, scale)
        self.__shadow.visible = 0

    def get_src_rect(self):
        return Spritesheet.get_board_src_rect(self.__colour, self.__type, self._scale)
    def get_group(self):
        return instance(Groups).get_board_group()
    def set_colour_and_type(self, colour, _type):
        self.__colour = colour
        self.__type = _type
        self.update_src_rect()

    def get_piece(self): return self.__piece
    def has_piece(self): return bool(self.__piece.visible)

    def set_piece_colour_and_type(self, colour, _type):
        self.__piece.set_colour_and_type(colour, _type)
        self.__piece.visible = 1
    def remove_piece(self):
        self.__selected = False
        self.__piece.visible = 0
        self.__piece.set_position(self.get_bottom_left())
    def move_piece(self, start, end, duration=250, pause=0):
        if self.has_piece():
            self.__piece.move(start, end, duration, pause)

    def is_selected(self): return self.__selected
    def select(self):
        if self.__selected:
            self.unselect()
        elif self.has_piece():
            self.move_piece(self.get_bottom_left(),
                            (self.rect.x, self.rect.y + self.rect.w / 2))
            self.__selected = True
    def unselect(self):
        if self.__selected and self.has_piece():
            self.move_piece(self.__piece.get_bottom_left(),
                            self.get_bottom_left())
            self.__selected = False
    def transfer_to(self, cell):
        if self.has_piece():
            if cell.has_piece():
                self.unselect()
            else:
                cell.set_piece_colour_and_type(
                    self.__piece.get_colour(), self.__piece.get_type())
                cell.move_piece(self.__piece.get_bottom_left(),
                                cell.get_bottom_left())
                self.remove_piece()

    def set_temporary_type(self, _type):
        if self.__fallback_type is None:
            self.__fallback_type = self.__type
        self.set_colour_and_type(self.__colour, _type)
    def fallback_type(self):
        if self.__fallback_type is not None:
            self.set_colour_and_type(self.__colour, self.__fallback_type)
            self.__fallback_type = None

    def get_grid_position(self): return self.__grid_position
    def get_bottom_left(self): return (self.rect.x, self.rect.y + self.rect.w)
