import pygame as pg
from src.tweens import Tween, TweenType
from src.groups import Groups
from src.globals import instance
from src.game.enums import PieceTag, ShadowType
from src.spritesheet import Spritesheet

class BoardSprite(pg.sprite.DirtySprite):

    def __init__(self, xy, scale):
        super().__init__()
        self.dirty = 2
        self.image = instance(Spritesheet).get_sheet(scale)
        self._scale = scale
        self.source_rect = self.get_src_rect()
        self.rect = pg.Rect((0, 0), self.source_rect.size)
        self.layer = self.position_transform(xy)[1]
        self.get_group().add(self)
        self.set_position(xy)
        self._position_tween = None

    def get_src_rect(self): return pg.Rect(0, 0, 0, 0)
    def get_group(self): return None

    def set_position(self, xy, preserve_tween = False):
        self._position = xy
        xy = self.position_transform(xy)
        self.get_group().change_layer(self, xy[1])
        self.rect.x, self.rect.y = xy[0], xy[1]
        if not preserve_tween:
            self._position_tween = None
    def position_transform(self, xy):
        return xy

    def tween_position(self, tween):
        self._position_tween = tween
        self._position_tween.restart()
    def move(self, start, end, duration, _type = TweenType.EASE_OUT_SINE, pause = 0):
        if start is None:
            start = self._position
        self.tween_position(Tween(_type, start, end, duration, pause))

    def update(self, force_position = False):
        if self._position_tween is not None:
            self.set_position(self._position_tween.value(), True)
            if self._position_tween.finished():
                self._position_tween = self._position_tween.get_chained()
        elif force_position:
            self.set_position(self._position, True)

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

    def __init__(self, cell):
        self.__cell = cell
        self.__colour = 0
        self.__type = 0
        self.__side = 0
        self.__tags = set()

        args = (cell.get_piece_position(), cell.get_child_scale())
        self.__shadow = Shadow(*args)
        self.__lift = 0
        self.__lift_tween = None
        super().__init__(*args)

        self.set_active(False)

    def position_transform(self, xy):
        return (xy[0], xy[1] - self.rect.h - self.__lift)
    def get_src_rect(self):
        return Spritesheet.get_piece_src_rect(self.__colour, self.__type, self.__side, self._scale)
    def get_group(self):
        return instance(Groups).get_piece_group()
    def set_data(self, colour, _type, side):
        self.__colour = colour
        self.__type = _type
        self.__side = side
        self.update_src_rect()

    def tween_lift(self, tween):
        self.__lift_tween = tween
        self.__lift_tween.restart()
    def lift(self, start, end, duration, _type = TweenType.EASE_OUT_SINE, pause = 0):
        if start is None:
            start = self.__lift
        self.tween_lift(Tween(_type, start, end, duration, pause))

    def set_position(self, xy, preserve_tween = False):
        super().set_position(xy, preserve_tween)
        self.__shadow.set_position(xy, preserve_tween)
        if not preserve_tween:
            self.__lift_tween = None
    def update(self, force_position = False):
        if self.__lift_tween is not None:
            force_position = True
            self.__lift = self.__lift_tween.value()
            if self.__lift_tween.finished():
                self.__lift_tween = None
        super().update(force_position)

    def get_colour(self): return self.__colour
    def get_type(self): return self.__type
    def get_side(self): return self.__side
    def get_position(self): return self.rect.bottomleft

    def add_tag(self, tag): self.__tags.add(tag)
    def remove_tag(self, tag): self.__tags.remove(tag)
    def has_tag(self, tag): return tag in self.__tags
    def get_tags(self): return self.__tags

    def set_cell(self, cell): self.__cell = cell
    def get_info(self):
        if not self.is_active(): return None
        return CellInfo(self.__cell.get_grid_position(),
                        self.__type,
                        self.__side,
                        self.__tags)

    def is_active(self): return self.visible == 1
    def set_active(self, a):
        self.visible = int(a)
        self.__shadow.visible = self.visible
        if not self.is_active():
            self.set_position(self.__cell.get_piece_position())

class Shadow(BoardSprite):

    def __init__(self, xy, scale):
        self.__type = ShadowType.LIGHT
        super().__init__(xy, scale)

    def position_transform(self, xy):
        return (xy[0], xy[1] - self.rect.h - 2 * self._scale)
    def get_src_rect(self):
        return Spritesheet.get_shadow_src_rect(self.__type, self._scale)
    def get_group(self):
        return instance(Groups).get_shadow_group()

    def set_type(self, _type):
        self.__type = _type
        self.update_src_rect()

    def is_active(self): return self.visible == 1
    def set_active(self, a): self.visible = int(a)

class CellInfo():

    def __init__(self, position, piece, side, tags):
        self.__position = position
        self.__piece = piece
        self.__side = side
        self.__tags = tags

    def get_position(self): return self.__position
    def get_piece(self): return self.__piece
    def get_side(self): return self.__side
    def has_tag(self, tag): return tag in self.__tags

class BoardCell(BoardSprite):

    def __init__(self, gxy, xy, colour, _type, scale, child_scale):
        self.__colour = colour
        self.__type = _type
        super().__init__(xy, scale)

        self.__grid_position = gxy
        self.__selected = False
        self.__fallback_type = None

        self.__child_scale = child_scale
        self.__piece = Piece(self)

    def get_src_rect(self):
        return Spritesheet.get_board_src_rect(self.__colour, self.__type, self._scale)
    def get_group(self):
        return instance(Groups).get_board_group()
    def set_data(self, colour, _type):
        self.__colour = colour
        self.__type = _type
        self.update_src_rect()

    def get_info(self):
        return self.__piece.get_info()

    def get_piece(self):
        return self.__piece
    def set_piece(self, piece):
        self.__piece = piece
        self.__piece.set_cell(self)
    def has_piece(self):
        return self.__piece.is_active()
    def remove_piece(self):
        self.__selected = False
        self.__piece.set_active(False)
    def place_piece(self, colour, _type, side):
        self.__piece.set_data(colour, _type, side)
        self.__piece.set_active(True)

    def is_selected(self):
        return self.__selected
    def select(self):
        if self.__selected:
            self.unselect()
        elif self.has_piece():
            self.__selected = True
            self.__piece.lift(None, self.rect.w / 2, 200)
    def unselect(self):
        if self.__selected and self.has_piece():
            self.__selected = False
            duration = 100
            self.__piece.move(None, self.get_piece_position(), duration)
            self.__piece.lift(None, 0, duration)
    def transfer_from(self, cell):
        if cell.has_piece():
            if self.has_piece():
                cell.unselect()
            else:
                new_piece = cell.get_piece()
                cell.set_piece(self.__piece)
                cell.remove_piece()
                self.set_piece(new_piece)
                duration = 300
                self.__piece.move(None, self.get_piece_position(), duration)
                self.__piece.lift(None, 0, duration)
                self.__piece.add_tag(PieceTag.HAS_MOVED)

    def set_temporary_type(self, _type):
        if self.__fallback_type is None:
            self.__fallback_type = self.__type
        self.set_data(self.__colour, _type)
    def fallback_type(self):
        if self.__fallback_type is not None:
            self.set_data(self.__colour, self.__fallback_type)
            self.__fallback_type = None

    def get_grid_position(self):
        return self.__grid_position
    def get_piece_position(self):
        offset = (self.rect.w - Spritesheet.PIECE_WIDTH * self.__child_scale) / 2
        return (self.rect.x + offset, self.rect.y + self.rect.w - offset)
    def get_child_scale(self):
        return self.__child_scale
