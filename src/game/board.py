from typing import Optional

import pygame as pg

from src.engine.config import Config
from src.engine.factory import Factory
from src.engine.spritesheets.board_spritesheet import BoardSpritesheet
from src.game.board_event import BoardDataType, BoardEvent, BoardEventType
from src.game.logic.logic_board import LogicBoard, MoveSupplier
from src.game.sprites.board_cell import BoardCell
from src.utils.enums import BoardColour, CellColour, MouseButton
from src.utils.helpers import FloatVector, IntVector
from src.utils.sprite import GroupType


class Board(LogicBoard):

    def __init__(
        self,
        move_supplier : MoveSupplier,
        colour : BoardColour = BoardColour.BLACK_WHITE,
        scale : float = 3,
        cell_scale : float = 1.25
    ):
        super().__init__(move_supplier)
        self.__bounds : pg.Rect = pg.Rect(0, 0, 0, 0)

        self.__colour = colour
        self.__scale = scale
        self.__cell_scale = scale * cell_scale

        self.__events : list[BoardEvent] = [] 
        self.__pressed_grid_position : Optional[IntVector] = None
    
    def reset(self, width : int, height : int) -> None:
        self._width = width
        self._height = height

        sw, sh = Config.get_window_dimensions()
        cell_size = BoardSpritesheet.BOARD_WIDTH * self.__cell_scale
        pixel_width = cell_size * self.width
        pixel_height = cell_size * self.height
        left = (sw - pixel_width) / 2
        top = (sh - pixel_height) / 2

        self.__bounds = pg.Rect(left, top, pixel_width, pixel_height)

        cell_colours = (CellColour.LIGHT, CellColour.DARK)
        def calculate_cell_colour(i : int, j : int) -> CellColour:
            return cell_colours[(i + j + 1) % len(cell_colours)]

        def calculate_cell_position(i : int, j : int) -> FloatVector:
            return (left + j * cell_size, top + i * cell_size)

        group_manager = Factory.get().group_manager
        for group in [GroupType.GAME_BOARD, GroupType.GAME_PIECE]:
            sprites = group_manager.get_sprites(group)
            for priority, sprites in sprites.items():
                for sprite in sprites:
                    group_manager.get_group(group, priority).remove(sprite)

        cells : list[tuple[BoardCell]] = []

        for i in range(self.height):
            row : list[BoardCell] = []
            for j in range(self.width):
                cell = BoardCell(
                    (i, j),
                    calculate_cell_position(i, j),
                    self.__colour,
                    calculate_cell_colour(i, j),
                    self.__cell_scale,
                    self.__scale
                )
                row.append(cell)
            cells.append(tuple(row))

        self._set_cells(tuple(cells))

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
    
    def at_pixel_position(self, point : IntVector) -> Optional[IntVector]:
        sprites = reversed(Factory.get().group_manager.get_flattened_sprites(GroupType.GAME_BOARD))
        for sprite in sprites:
            if not isinstance(sprite, BoardCell):
                continue
            if sprite.point_intersects(point):
                return sprite.gxy
        return None

    @property
    def scale(self) -> float:
        return self.__scale

    @property
    def pixel_bounds(self) -> pg.Rect:
        return self.__bounds
