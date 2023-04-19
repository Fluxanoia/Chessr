from typing import NoReturn, Optional

import pygame as pg

from src.engine.spritesheets.board_spritesheet import BoardSpritesheet
from src.logic.board_event import BoardDataType, BoardEvent, BoardEventType
from src.logic.logic_board import LogicBoard, MoveSupplier
from src.sprites.board.board_cell import BoardCell
from src.utils.enums import BoardColour, CellColour, MouseButton
from src.utils.helpers import FloatVector, IntVector


class Board(LogicBoard):

    def __init__(
        self,
        move_supplier : MoveSupplier,
        colour : BoardColour = BoardColour.BLACK_WHITE,
    ):
        super().__init__(move_supplier)
        self.__bounds : pg.Rect = pg.Rect(0, 0, 0, 0)

        self.__colour = colour
        self.__scale = 3
        self.__cell_scale = 3.75

        self.__events : list[BoardEvent] = [] 
        self.__pressed_grid_position : Optional[IntVector] = None
    
    def reset(self, width : int, height : int) -> None:
        for i in range(self.height):
            for j in range(self.width):
                cell = self.at(i, j)
                if not isinstance(cell, BoardCell):
                    self.__raise_display_cast_error()
                cell.delete()

        self._width = width
        self._height = height

        cell_colours = (CellColour.LIGHT, CellColour.DARK)
        def calculate_cell_colour(i : int, j : int) -> CellColour:
            return cell_colours[(i + j + 1) % len(cell_colours)]

        cells : list[tuple[BoardCell]] = []

        for i in range(self.height):
            row : list[BoardCell] = []
            for j in range(self.width):
                cell = BoardCell(
                    (i, j),
                    (0, 0),
                    self.__colour,
                    calculate_cell_colour(i, j),
                    self.__cell_scale,
                    self.__scale
                )
                row.append(cell)
            cells.append(tuple(row))

        self._set_cells(tuple(cells))

    def set_position(self, x : int, y : int):
        cell_size = BoardSpritesheet.BOARD_WIDTH * self.__cell_scale
        pixel_width = cell_size * self.width
        pixel_height = cell_size * self.height
        left = x - pixel_width / 2
        top = y - pixel_height / 2

        self.__bounds = pg.Rect(left, top, pixel_width, pixel_height)

        def calculate_cell_position(i : int, j : int) -> FloatVector:
            return (left + j * cell_size, top + i * cell_size)

        for i in range(self.height):
            for j in range(self.width):
                sprite = self.at(i, j)
                if not isinstance(sprite, BoardCell):
                    self.__raise_display_cast_error()
                sprite.set_position(calculate_cell_position(i, j))

    def mouse_down(self, event : pg.event.Event) -> bool:
        if event.button == MouseButton.LEFT:
            self.__pressed_grid_position = self.at_pixel_position(pg.mouse.get_pos())
            if not self.__pressed_grid_position is None:
                return True
        return False
    
    def mouse_up(self, event : pg.event.Event) -> bool:
        if event.button == MouseButton.LEFT:
            event_parsed = False
            released = self.at_pixel_position(pg.mouse.get_pos())

            if self.__pressed_grid_position == released:
                data = { BoardDataType.GRID_POSITION: self.__pressed_grid_position }
                self.__events.append(BoardEvent(BoardEventType.CLICK, data))
                event_parsed = True
            
            self.__pressed_grid_position = None
            return event_parsed
        return False
    
    def pop_event(self) -> Optional[BoardEvent]:
        if len(self.__events) == 0:
            return None
        return self.__events.pop(0)
    
    def at_pixel_position(self, point : IntVector) -> Optional[IntVector]:
        for i in range(self.height):
            for j in range(self.width):
                cell = self.at(i, j)
                if not isinstance(cell, BoardCell):
                    self.__raise_display_cast_error()
                if cell.point_intersects(point):
                    return cell.gxy
        return None

    @property
    def scale(self) -> float:
        return self.__scale

    @property
    def bounds(self) -> pg.Rect:
        return self.__bounds
    
    @staticmethod
    def __raise_display_cast_error() -> NoReturn:
        raise SystemExit('There was a failed attempt to cast a logic object to a display object.')