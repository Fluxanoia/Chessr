from typing import Callable, Optional

from src.game.logic.move_data import Moves
from src.game.logic.piece_tag import PieceTag, PieceTagType
from src.game.sprites.board_cell import LogicCell
from src.game.sprites.piece import LogicPiece
from src.utils.helpers import IntVector, inbounds

MovesGrid = tuple[tuple[Optional[Moves]]]
LogicCellGrid = tuple[tuple[LogicCell]]
LogicPieceGrid = tuple[tuple[Optional[LogicPiece]]]
MoveSupplier = Callable[["LogicBoard"], MovesGrid]

class LogicBoard():

    def __init__(self,
                 move_supplier : MoveSupplier,
                 width : int = 0,
                 height : int = 0,
                 cells : Optional[LogicCellGrid] = None):
        self.__width = width
        self.__height = height
        self.__cells : LogicCellGrid = tuple([tuple([])]) if cells is None else cells
        self.__moves : MovesGrid = tuple([tuple([])])
        self.__move_supplier = move_supplier
        self.__dirty_moves = True

    def move(self, from_gxy : IntVector, to_gxy : IntVector) -> None:
        moves_object = self.moves_at(*from_gxy)
        piece_to_move = self.piece_at(*from_gxy)
        if moves_object is None or piece_to_move is None:
            return

        self.__move(from_gxy, to_gxy)
        if not piece_to_move.has_tag(PieceTagType.HAS_MOVED):
            piece_to_move.add_tag(PieceTag.get_tag(PieceTagType.HAS_MOVED))

        moves_object.trigger_callbacks(from_gxy, to_gxy)
        
        self.__update_tags()

    def __move(self, from_gxy : IntVector, to_gxy : IntVector) -> None:
        if from_gxy == to_gxy:
            return

        from_cell = self.at(*from_gxy)
        to_cell = self.at(*to_gxy)

        if from_cell is None or to_cell is None:
            return

        to_cell.take_piece_from(from_cell)
        self.__dirty_moves = True

    def __update_tags(self) -> None:
        for row in self.__cells:
            for cell in row:
                if cell.piece is None:
                    continue
                cell.piece.update_tags()
        self.__dirty_moves = True

    def remove(self, i : int, j : int) -> None:
        cell = self.at(i, j)
        if cell is None:
            return
        cell.remove_piece()
        self.__dirty_moves = True

    def at(self, i : int, j : int) -> Optional[LogicCell]:
        if not inbounds(self.width, self.height, (i, j)):
            return None
        return self.__cells[i][j]

    def row_at(self, i : int) -> Optional[tuple[LogicCell]]:
        if not inbounds(self.width, self.height, (i, 0)):
            return None
        return self.__cells[i]

    def piece_at(self, i : int, j : int) -> Optional[LogicPiece]:
        cell = self.at(i, j)
        if cell is None:
            return None
        return cell.piece
    
    def moves_at(self, i : int, j : int) -> Optional[Moves]:
        all_cells = [cell for row in self.__cells for cell in row]
        dirty = self.__dirty_moves or any(map(lambda x : x.is_dirty(), all_cells))
        if dirty:
            self.__dirty_moves = False
            for cell in all_cells:
                cell.clean()
            self.__moves = self.__move_supplier(self)

        if not inbounds(self.width, self.height, (i, j)):
            return None
        return self.__moves[i][j]
    
    def copy(self) -> "LogicBoard":
        cells : list[tuple[LogicCell]] = []

        for i in range(self.height):
            row : list[LogicCell] = []
            for j in range(self.width):
                cell = self.at(i, j)
                if cell is None:
                    raise SystemExit('Unexpected missing cell.')
                row.append(cell.copy())
            cells.append(tuple(row))
        
        return LogicBoard(
            self.__move_supplier,
            self.width,
            self.height,
            tuple(cells))

    def _set_cells(self, cells : LogicCellGrid):
        self.__cells = cells
        self.__dirty_moves = True

    @property
    def width(self) -> int:
        return self.__width
    
    @width.setter
    def _width(self, width : int):
        self.__width = width

    @property
    def height(self) -> int:
        return self.__height
    
    @height.setter
    def _height(self, height : int):
        self.__height = height