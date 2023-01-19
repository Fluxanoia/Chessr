from typing import Optional

import pygame as pg

from src.engine.config import Config
from src.engine.factory import Factory
from src.engine.spritesheets.board_spritesheet import BoardSpritesheet
from src.game.board_event import BoardDataType, BoardEvent, BoardEventType
from src.game.sprite import GroupType
from src.game.sprites.board_cell import BoardCell
from src.game.sprites.piece import Piece
from src.utils.enums import BoardColour, CellColour, MouseButton
from src.utils.helpers import FloatVector, IntVector, inbounds


class Board():

    def __init__(
        self,
        colour : BoardColour = BoardColour.BLACK_WHITE,
        scale : float = 3,
        cell_scale : float = 1.25
    ):
        self.__width : int = 0
        self.__height : int = 0
        self.__bounds : pg.Rect = pg.Rect(0, 0, 0, 0)
        self.__cells : list[list[BoardCell]] = []

        self.__colour = colour
        self.__scale = scale
        self.__cell_scale = scale * cell_scale

        self.__events : list[BoardEvent] = [] 
        self.__pressed_grid_position : Optional[IntVector] = None
    
    def reset(self, width : int, height : int) -> None:
        self.__width = width
        self.__height = height

        sw, sh = Config.get_window_dimensions()
        cell_size = BoardSpritesheet.BOARD_WIDTH * self.__cell_scale
        pixel_width = cell_size * self.__width
        pixel_height = cell_size * self.__height
        left = (sw - pixel_width) / 2
        top = (sh - pixel_height) / 2

        self.__bounds = pg.Rect(left, top, pixel_width, pixel_height)

        cell_colours = (CellColour.LIGHT, CellColour.DARK)
        def calculate_cell_colour(i : int, j : int) -> CellColour:
            return cell_colours[(i + j) % len(cell_colours)]

        def calculate_cell_position(i : int, j : int) -> FloatVector:
            return (left + j * cell_size, top + i * cell_size)

        group_manager = Factory.get().group_manager
        for group in [GroupType.BOARD, GroupType.BOARD_HIGHLIGHT, GroupType.PIECE, GroupType.SHADOW]:
            sprites = group_manager.get_sprites(group)
            for sprite in sprites:
                group_manager.get_group(group).remove(sprite)

        self.__cells = []

        for i in range(self.__height):
            row : list[BoardCell] = []
            for j in range(self.__width):
                cell = BoardCell(
                    (i, j),
                    calculate_cell_position(i, j),
                    self.__colour,
                    calculate_cell_colour(i, j),
                    self.__cell_scale,
                    self.__scale
                )
                row.append(cell)
            self.__cells.append(row)

    def at(self, i : int, j : int) -> Optional[BoardCell]:
        if not inbounds(self.__width, self.__height, (i, j)):
            return None
        return self.__cells[i][j]

    def row_at(self, i : int) -> Optional[list[BoardCell]]:
        if not inbounds(self.__width, self.__height, (i, 0)):
            return None
        return self.__cells[i]

    def piece_at(self, i : int, j : int) -> Optional[Piece]:
        cell = self.at(i, j)
        if cell is None:
            return None
        return cell.get_piece()

    def mouse_down(self, event : pg.event.Event) -> None:
        if event.button == MouseButton.LEFT:
            self.__pressed_grid_position = self.at_pixel_position(pg.mouse.get_pos())
    
    def mouse_up(self, event : pg.event.Event) -> None:
        if event.button == MouseButton.LEFT:
            released = self.at_pixel_position(pg.mouse.get_pos())

            if self.__pressed_grid_position == released:
                data = { BoardDataType.GRID_POSITION: self.__pressed_grid_position }
                self.__events.append(BoardEvent(BoardEventType.CLICK, data))
            
            self.__pressed_grid_position = None
    
    def pop_event(self) -> Optional[BoardEvent]:
        if len(self.__events) == 0:
            return None
        return self.__events.pop(0)

    def update_tags(self) -> None:
        for row in self.__cells:
            for cell in row:
                piece = cell.get_piece()
                if piece is None:
                    continue
                piece.update_tags()

    def move(self, from_gxy : IntVector, to_gxy : IntVector) -> None:
        if from_gxy == to_gxy:
            return

        from_cell = self.at(*from_gxy)
        to_cell = self.at(*to_gxy)

        if from_cell is None or to_cell is None:
            return

        piece_to_move = from_cell.get_piece()
        piece_to_take = to_cell.get_piece()

        if piece_to_move is None:
            return

        if not piece_to_take is None:
            to_cell.remove_piece(True)

        from_cell.remove_piece()
        to_cell.set_piece(piece_to_move)

    def remove(self, i : int, j : int) -> None:
        cell = self.at(i, j)
        if cell is None:
            return
        cell.remove_piece(True)
    
    def at_pixel_position(self, point : IntVector) -> Optional[IntVector]:
        sprites = reversed(Factory.get().group_manager.get_sprites(GroupType.BOARD))
        for sprite in sprites:
            if not isinstance(sprite, BoardCell):
                continue
            if sprite.point_intersects(point):
                return sprite.grid_position
        return None

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def scale(self) -> float:
        return self.__scale

    @property
    def pixel_bounds(self) -> pg.Rect:
        return self.__bounds
