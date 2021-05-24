from src.game.enums import PieceTag, ShadowType
from src.utils.groups import FluxSprite, GroupType
from src.utils.tweens import Tween, TweenType
from src.utils.globals import clamp, instance
from src.utils.spritesheet import Spritesheet

class Piece(FluxSprite):

    def __init__(self, cell):
        self.__cell = cell
        self.__colour = 0
        self.__type = 0
        self.__side = 0
        self.__tags = set()

        self.group = GroupType.PIECE
        self.scale = cell.get_child_scale()
        self.image = instance(Spritesheet).get_sheet(self._scale)

        xy = cell.get_piece_position()
        self.__lift = 0
        self.__lift_tween = None
        self.__shadow = Shadow(xy, self._scale)
        self.update_shadow_alpha()
        super().__init__(xy, self.get_srcrect())

        self.set_active(False)

    def position_transform(self, xy):
        return (xy[0], xy[1] - self.rect.h - self.__lift)
    def get_srcrect(self):
        return Spritesheet.get_piece_srcrect(self.__colour, self.__type, self.__side, self._scale)
    def update_srcrect(self):
        self.srcrect = self.get_srcrect()
    def set_data(self, colour, _type, side):
        self.__colour = colour
        self.__type = _type
        self.__side = side
        self.update_srcrect()

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
            self.update_shadow_alpha()
            if self.__lift_tween.finished():
                self.__lift_tween = None
        super().update(force_position)

    def update_shadow_alpha(self):
        alpha = 255 * (1 - self.__lift / 60.0) if self.__lift != 0 else 0
        self.__shadow.set_alpha(clamp(alpha, 0, 255))

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
        if not self.is_active():
            return None
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

class Shadow(FluxSprite):

    def __init__(self, xy, scale):
        self.__type = ShadowType.DARK
        self.group = GroupType.SHADOW
        self.scale = scale
        self.image = instance(Spritesheet).get_image(Spritesheet.get_shadow_srcrect(
            self.__type, scale), scale)
        super().__init__(xy)

    def position_transform(self, xy):
        return (xy[0], xy[1] - self.rect.h - 2 * self._scale)

    def set_alpha(self, alpha):
        self.image.set_alpha(alpha)

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

class BoardCell(FluxSprite):

    def __init__(self, gxy, xy, colour, _type, scale, child_scale):
        self.__colour = colour
        self.__type = _type

        self.group = GroupType.BOARD
        self.scale = scale
        self.image = instance(Spritesheet).get_sheet(self._scale)
        super().__init__(xy, self.get_srcrect())

        self.__grid_position = gxy
        self.__selected = False
        self.__fallback_type = None

        self.__child_scale = child_scale
        self.__piece = Piece(self)

    def get_srcrect(self):
        return Spritesheet.get_board_srcrect(self.__colour, self.__type, self._scale)
    def update_srcrect(self):
        self.srcrect = self.get_srcrect()
    def set_data(self, colour, _type):
        self.__colour = colour
        self.__type = _type
        self.update_srcrect()

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
