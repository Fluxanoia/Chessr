import pygame as pg
from src.enum import enum_as_list
from src.tweens import Tween, TweenType
from src.groups import Groups
from src.globals import Globals, MouseButton, instance
from src.spritesheet import Spritesheet, BoardColour, BoardType, PieceColour, PieceType, ShadowType

class BoardSprite(pg.sprite.DirtySprite):

    def __init__(self, sheet, xy, scale):
        super().__init__()
        self.dirty = 2 # TODO
        self.image = sheet
        self._scale = scale
        self.source_rect = self.get_src_rect()
        self.rect = pg.Rect((0, 0), self.source_rect.size)
        self.layer = self.get_layer(xy)
        self.get_group().add(self)
        self.set_position(xy)

    def get_layer(self, xy): return xy[1]
    def get_src_rect(self): return pg.Rect(0, 0, 0, 0)
    def get_group(self): return None

    def set_position(self, xy):
        self.get_group().change_layer(self, xy[1])
        self.rect.x, self.rect.y = xy[0], xy[1]

    def set_src_rect(self, srcrect):
        if self.source_rect is None:
            self.source_rect = srcrect
        else:
            self.source_rect.update(srcrect)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

class Piece(BoardSprite):

    def __init__(self, sheet, xy, colour, _type, scale):
        self.__colour = colour
        self.__type = _type
        super().__init__(sheet, xy, scale)

    def get_position_from(self, xy):
        return (xy[0], xy[1] - self.rect.h)
    def get_layer(self, xy):
        return self.get_position_from(xy)[1]
    def get_src_rect(self):
        return Spritesheet.get_piece_src_rect(self.__colour, self.__type, self._scale)
    def get_group(self):
        return instance(Groups).get_piece_group()

    def set_colour_and_type(self, colour, _type):
        self.__colour = colour
        self.__type = _type
        self.set_src_rect(self.get_src_rect())

    def set_position(self, xy):
        super().set_position(self.get_position_from(xy))
        self.__tween = None

    def move(self, start, end, duration):
        self.__tween = Tween(TweenType.EASE_OUT_QUAD, start, end, duration)

    def update(self):
        if self.__tween is not None:
            super().set_position(self.get_position_from(self.__tween.value()))
            if self.__tween.finished():
                self.__tween = None

    def get_colour(self): return self.__colour
    def get_type(self): return self.__type
    def get_origin(self): return self.rect.bottomleft

class Shadow(BoardSprite):

    def __init__(self, sheet, xy, _type, scale):
        self.__type = _type
        super().__init__(sheet, xy, scale)

    def get_position_from(self, xy):
        return (xy[0], xy[1] - self.rect.h - 2 * self._scale)
    def get_layer(self, xy):
        return self.get_position_from(xy)[1]
    def get_src_rect(self):
        return Spritesheet.get_shadow_src_rect(self.__type, self._scale)
    def get_group(self):
        return instance(Groups).get_shadow_group()

    def set_type(self, _type):
        self.__type = _type
        self.set_src_rect(self.get_src_rect())

    def set_position(self, xy):
        super().set_position(self.get_position_from(xy))

class BoardCell(BoardSprite):

    def __init__(self, sheet, gxy, xy, colour, _type, scale):
        self.__colour = colour
        self.__type = _type
        super().__init__(sheet, xy, scale)

        self.__grid_position = gxy
        self.__selected = False

        self.__piece = Piece(self.image, self.get_origin(), 0, 0, scale)
        self.__piece.visible = 0
        self.__shadow = Shadow(sheet, self.get_origin(), ShadowType.LIGHT, scale)
        self.__shadow.visible = 0

    def get_layer(self, xy):
        return xy[1]
    def get_src_rect(self):
        return Spritesheet.get_board_src_rect(self.__colour, self.__type, self._scale)
    def get_group(self):
        return instance(Groups).get_board_group()

    def set_colour_and_type(self, colour, _type):
        self.__colour = colour
        self.__type = _type
        self.set_src_rect(self.get_src_rect())

    def get_piece(self): return self.__piece
    def has_piece(self): return bool(self.__piece.visible)
    def set_piece_colour_and_type(self, colour, _type):
        self.__piece.set_colour_and_type(colour, _type)
        self.__piece.visible = 1
    def remove_piece(self):
        self.__selected = False
        self.__piece.visible = 0
        self.__piece.set_position(self.get_origin())
    def move_piece(self, start, end, duration = 250):
        if self.has_piece(): self.__piece.move(start, end, duration)

    def is_selected(self): return self.__selected
    def select(self):
        if self.__selected:
            self.unselect()
        elif self.has_piece():
            self.move_piece(self.get_origin(), (self.rect.x, self.rect.y + self.rect.w / 2))
            self.__selected = True
    def unselect(self):
        if self.__selected and self.has_piece():
            self.move_piece(self.__piece.get_origin(), self.get_origin())
            self.__selected = False
    def transfer_to(self, cell):
        if self.has_piece():
            if cell.has_piece():
                self.unselect()
            else:
                cell.set_piece_colour_and_type(self.__piece.get_colour(), self.__piece.get_type())
                cell.move_piece(self.__piece.get_origin(), cell.get_origin())
                self.remove_piece()

    def get_grid_position(self): return self.__grid_position
    def get_origin(self): return (self.rect.x, self.rect.y + self.rect.w)

class Board():

    def __init__(self, colour = BoardColour.BLACK_WHITE, scale = 3):
        self.__spritesheet = instance(Spritesheet).get_sheet(scale)

        self.__board = list()
        self.__cell_width = 8
        cell_size = Spritesheet.BOARD_WIDTH * scale
        x_offset, y_offset = map(lambda x : (x - cell_size * self.__cell_width) / 2,
            instance(Globals).get_window_size())
        cell_types = enum_as_list(BoardType)
        for y in range(self.__cell_width):
            row = list()
            for x in range(self.__cell_width):
                row.append(BoardCell(self.__spritesheet,
                    (y, x), (x_offset + x * cell_size, y_offset + y * cell_size),
                    colour, cell_types[(x + y) % len(cell_types)], scale))
            self.__board.append(row)
        self.traditional_layout()

        self.__pressed = None
        self.__selected = None

    def traditional_layout(self):
        colour = lambda i : PieceColour.BLACK if i < self.__cell_width / 2 else PieceColour.WHITE
        base_rows = (0, self.__cell_width - 1)
        base_info = (
            (PieceType.ROOK, (0, self.__cell_width - 1)),
            (PieceType.KNIGHT, (1, self.__cell_width - 2)),
            (PieceType.BISHOP, (2, self.__cell_width - 3)),
            (PieceType.QUEEN, (3,)),
            (PieceType.KING, (self.__cell_width - 4,)),
        )
        for _type, cols in base_info:
            for i in base_rows:
                for j in cols:
                    self.__board[i][j].set_piece_colour_and_type(colour(i), _type)

        pawn_rows = (1, self.__cell_width - 2)
        for i in pawn_rows:
            for j in range(self.__cell_width):
                self.__board[i][j].set_piece_colour_and_type(colour(i), PieceType.PAWN)

    def update(self):
        pass

    def cell_at(self, i, j): return self.__board[i][j]

    def get_collision(self, pos):
        for s in reversed(instance(Groups).get_board_cells()):
            if s.collidepoint(pos): return s.get_grid_position()
        return None

    def pressed(self, event):
        if event.button == MouseButton.LEFT:
            self.__pressed = self.get_collision(pg.mouse.get_pos())
    def released(self, event):
        if event.button == MouseButton.LEFT:
            _released = self.get_collision(pg.mouse.get_pos())
            if self.__pressed == _released: self.__clicked(self.__pressed)
    def __clicked(self, gxy):
        if gxy is not None:
            if self.cell_at(*gxy).has_piece():
                if self.__selected is not None:
                    self.cell_at(*self.__selected).unselect()
                self.__selected = gxy
                self.cell_at(*gxy).select()
            elif self.__selected is not None:
                self.cell_at(*self.__selected).transfer_to(self.cell_at(*gxy))
                self.__selected = None
        elif self.__selected is not None:
            self.cell_at(*self.__selected).unselect()
            self.__selected = None
