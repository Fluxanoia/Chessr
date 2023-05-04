from typing import Optional, cast

import pygame as pg
from backend import (ChangeConsequence, Consequence, ConsequenceType,
                     MoveConsequence, PieceType, RemoveConsequence)
from src.engine.spritesheets.board_spritesheet import (BoardColour,
                                                       BoardSpritesheet,
                                                       CellColour)
from src.logic.board_event import BoardDataType, BoardEvent, BoardEventType
from src.sprites.board.board_cell import BoardCell
from src.sprites.board.piece import Piece
from src.utils.enums import MouseButton
from src.utils.helpers import FloatVector, IntVector, inbounds


class Board():

    def __init__(
        self,
        colour : BoardColour = BoardColour.BLACK_WHITE,
    ):
        self.__width = 0
        self.__height = 0
        self.__cells : tuple[tuple[BoardCell, ...], ...] = tuple([tuple([])])
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
                if not cell is None:
                    cell.delete()

        self.__width = width
        self.__height = height

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

        self.__cells = tuple(cells)

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
                cell = self.at(i, j)
                if not cell is None:
                    cell.set_position(calculate_cell_position(i, j))

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
                if not cell is None and cell.point_intersects(point):
                    return cell.gxy
        return None
    
    def apply_consequences(self, consequences : list[Consequence]):
        for consequence in consequences:
            self.apply_consequence(consequence)

    def apply_consequence(self, consequence : Consequence):
        type = consequence.get_type()
        if type == ConsequenceType.MOVE:
            consequence = cast(MoveConsequence, consequence)
            self.__move(consequence.from_gxy, consequence.to_gxy)
        elif type == ConsequenceType.REMOVE:
            consequence = cast(RemoveConsequence, consequence)
            self.__remove(consequence.gxy)
        elif type == ConsequenceType.CHANGE:
            consequence = cast(ChangeConsequence, consequence)
            self.__change(consequence.gxy, consequence.piece_type)
        else:
            raise SystemExit('Unexpected consequence type.')

    def __move(
        self,
        from_gxy : IntVector,
        to_gxy : IntVector
    ) -> None:
        if from_gxy == to_gxy:
            return
        
        piece_to_move = self.piece_at(*from_gxy)
        if piece_to_move is None:
            return

        from_cell = self.at(*from_gxy)
        to_cell = self.at(*to_gxy)

        if from_cell is None or to_cell is None:
            return

        to_cell.take_piece_from(from_cell)

    def __remove(
        self,
        gxy : IntVector,
    ) -> None:
        piece_to_remove = self.piece_at(*gxy)
        if piece_to_remove is None:
            return

        cell = self.at(*gxy)
        if cell is None:
            return

        cell.remove_piece()

    def __change(
        self,
        gxy : IntVector,
        piece_type : PieceType
    ):
        piece_to_change = self.piece_at(*gxy)
        if piece_to_change is None:
            return

        piece_to_change.change_type(piece_type)
        
    def remove(self, i : int, j : int) -> None:
        cell = self.at(i, j)
        if cell is None:
            return
        cell.remove_piece()

#region Properties, Getters, and Setters

    def at(self, i : int, j : int) -> Optional[BoardCell]:
        if not inbounds(self.width, self.height, (i, j)):
            return None
        return self.__cells[i][j]

    def row_at(self, i : int) -> Optional[tuple[BoardCell]]:
        if not inbounds(self.width, self.height, (i, 0)):
            return None
        return self.__cells[i]

    def piece_at(self, i : int, j : int) -> Optional[Piece]:
        cell = self.at(i, j)
        if cell is None:
            return None
        return cell.piece
    
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
    def bounds(self) -> pg.Rect:
        return self.__bounds

#endregion
