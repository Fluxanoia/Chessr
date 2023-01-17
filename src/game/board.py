from typing import Optional

import pygame as pg

from src.engine.config import Config
from src.engine.factory import Factory
from src.engine.spritesheets.board_spritesheet import BoardSpritesheet
from src.game.board_event import BoardDataType, BoardEvent, BoardEventType
from src.game.sprite import ChessrSprite, GroupType
from src.game.sprites.board_cell import BoardCell
from src.game.sprites.coordinate_text import CoordinateText
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
        self.__cells : list[list[BoardCell]] = []
        self.__texts : list[CoordinateText] = []

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
        x_offset = (sw - cell_size * self.__width) / 2
        y_offset = (sh - cell_size * self.__height) / 2

        cell_colours = (CellColour.LIGHT, CellColour.DARK)
        def calculate_cell_colour(i : int, j : int) -> CellColour:
            return cell_colours[(i + j) % len(cell_colours)]

        def calculate_cell_position(i : int, j : int) -> FloatVector:
            return (x_offset + j * cell_size, y_offset + i * cell_size)

        sprites_to_removes : list[ChessrSprite] = [cell for row in self.__cells for cell in row]
        sprites_to_removes.extend(self.__texts)
        group_manager = Factory.get().group_manager
        for sprite in sprites_to_removes:
            group = sprite.group
            if group is None:
                continue
            group_manager.get_group(group).remove(sprite)

        self.__cells = []
        self.__texts = []

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

        buffer = int(3 * cell_size / 4)
        bottom = y_offset + self.__height * cell_size

        for i in range(self.__height):
            pos = (x_offset - buffer, bottom - (i + 0.5) * cell_size)
            self.__texts.append(CoordinateText(str(i + 1), pos, self.__cell_scale))
        
        for j in range(self.__width):
            pos = (x_offset + (j + 0.5) * cell_size, bottom + buffer)
            self.__texts.append(CoordinateText(chr(ord('A') + j), pos, self.__cell_scale))

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
            self.__pressed_grid_position = self.__get_intersected_grid_position(pg.mouse.get_pos())
    
    def mouse_up(self, event : pg.event.Event) -> None:
        if event.button == MouseButton.LEFT:
            released = self.__get_intersected_grid_position(pg.mouse.get_pos())

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
        from_cell = self.at(*from_gxy)
        to_cell = self.at(*to_gxy)
        piece = self.piece_at(*from_gxy)

        if from_cell is None \
            or to_cell is None \
            or piece is None \
            or from_gxy == to_gxy:
            return

        to_cell.transfer_from(from_cell)

    def remove(self, i : int, j : int) -> None:
        cell = self.at(i, j)
        if cell is None:
            return
        cell.remove_piece(True)
    
    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    def __get_intersected_grid_position(self, point : IntVector) -> Optional[IntVector]:
        sprites = reversed(Factory.get().group_manager.get_sprites(GroupType.BOARD))
        for sprite in sprites:
            if not isinstance(sprite, BoardCell):
                continue
            if sprite.point_intersects(point):
                return sprite.grid_position
        return None
