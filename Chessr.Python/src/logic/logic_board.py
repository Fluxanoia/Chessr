from typing import Callable, Optional

from src.logic.move_data import MoveType
from src.logic.notation import Notation
from src.logic.piece_tag import PieceTag, PieceTagType
from src.sprites.board.board_cell import LogicCell
from src.sprites.board.piece import LogicPiece
from src.utils.enums import LogicState, PendingMoveType, PieceType
from src.utils.helpers import IntVector, inbounds

MovesGrid = tuple[tuple[Optional["Moves"]]]
LogicCellGrid = tuple[tuple[LogicCell]]
LogicPieceGrid = tuple[tuple[Optional[LogicPiece]]]
MoveSupplier = Callable[["LogicBoard"], None]
ManoeuvreCallback = Callable[["LogicBoard", IntVector, IntVector], None]

class LogicBoard():

    def __init__(
        self,
        move_supplier : MoveSupplier,
        width : int = 0,
        height : int = 0,
        cells : Optional[LogicCellGrid] = None,
        moves : Optional[MovesGrid] = None,
        dirty_moves : bool = True
    ):
        self.__width = width
        self.__height = height
        self.__cells : LogicCellGrid = tuple([tuple([])]) if cells is None else cells
        self.__moves : MovesGrid = tuple([tuple([])]) if moves is None else moves
        self.__move_supplier = move_supplier
        self.__dirty_moves = dirty_moves

#region Piece Logic

    def move(
        self,
        from_gxy : IntVector,
        to_gxy : IntVector,
        skip_validation : bool = False
    ) -> None:
        if from_gxy == to_gxy:
            return
        
        moves = self.moves_at(*from_gxy, skip_validation)
        piece_to_move = self.piece_at(*from_gxy)
        if (not skip_validation and moves is None) or piece_to_move is None:
            return

        from_cell = self.at(*from_gxy)
        to_cell = self.at(*to_gxy)

        if from_cell is None or to_cell is None:
            return

        to_cell.take_piece_from(from_cell)

        if not piece_to_move.has_tag(PieceTagType.HAS_MOVED):
            piece_to_move.add_tag(PieceTag.get_tag(PieceTagType.HAS_MOVED))

        if not moves is None:
            moves.trigger_callbacks(self, from_gxy, to_gxy)
        
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

#endregion

#region Moves

    def supply_moves(self, moves : MovesGrid):
        self.__moves = moves

        self.__dirty_moves = False
        all_cells = [cell for row in self.__cells for cell in row]
        for cell in all_cells:
            cell.clean()

    def clean(self):
        if self.is_dirty():
            self.__move_supplier(self)

    def is_dirty(self) -> bool:
        all_cells = [cell for row in self.__cells for cell in row]
        return self.__dirty_moves or any(map(lambda x : x.is_dirty(), all_cells))

#endregion

#region Copying

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
            tuple(cells),
            self.__moves,
            self.__dirty_moves)

#endregion

#region Properties, Getters, and Setters

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
    
    def moves_at(self, i : int, j : int, skip_validation : bool = False) -> Optional["Moves"]:
        if not inbounds(self.width, self.height, (i, j)) \
            or len(self.__moves) <= i or len(self.__moves[i]) <= j:
            return None
        if not skip_validation and self.is_dirty():
            raise SystemExit('Attempted to get moves from a dirty LogicBoard.')
        return self.__moves[i][j]

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

#endregion

class Move:

    def __init__(
        self,
        piece_type : PieceType,
        from_gxy : IntVector,
        gxy : IntVector,
        move_type : MoveType,
        valid : bool,
        callback : Optional[ManoeuvreCallback] = None,
        pending_action : Optional[PendingMoveType] = None
    ):
        self.__piece_type = piece_type
        self.__from_gxy = from_gxy
        self.__gxy = gxy
        self.__move_type = move_type
        self.__valid = valid
        self.__callback = callback
        self.__pending_action = pending_action
        self.__notation : Optional[str] = None

    def invalidate(self):
        self.__valid = False

    def set_pending_action(self, value : Optional[PendingMoveType]):
        self.__pending_action = value

    def override_notation(self, notation : str):
        self.__notation = notation

    def set_notation(
        self,
        board_height : int,
        rank_ambigious : bool,
        file_ambigious : bool,
        state : LogicState
    ) -> None:
        notation = Notation.get()

        if self.__piece_type is PieceType.PAWN:
            char = ''
            file_ambigious = file_ambigious or self.__move_type is MoveType.ATTACK
        else:
            char = notation.get_char(self.__piece_type)
        
        destination = notation.get_notation_from_coordinate(self.__gxy, board_height)
        if destination is None:
            return

        suffix = ''
        if state is LogicState.CHECK:
            suffix = '+'
        elif state is LogicState.CHECKMATE:
            suffix = '#'

        ambiguity = ''
        if file_ambigious:
            ambiguity += notation.get_file_from_coordinate(self.__from_gxy[1])
        if rank_ambigious:
            ambiguity += notation.get_rank_from_coordinate(self.__from_gxy[0], board_height)

        capture = 'x' if self.__move_type is MoveType.ATTACK else ''

        self.__notation = char + ambiguity + capture + destination + suffix

    @property
    def gxy(self):
        return self.__gxy

    @property
    def move_type(self):
        return self.__move_type

    @property
    def valid(self):
        return self.__valid
    
    @property
    def callback(self):
        return self.__callback

    @property
    def pending_action(self):
        return self.__pending_action
    
    @property
    def notation(self):
        return self.__notation

class Moves:

    def __init__(self, moves : tuple[Move, ...]):
        self.__moves : tuple[Move, ...] = moves

    def get_all_moves(self) -> tuple[Move]:
        return self.__moves

    def get_valid_moves(self) -> tuple[Move]:
        return tuple(filter(lambda x : x.valid, self.__moves))
    
    def get_possible_attacks(self) -> tuple[Move]:
        return tuple(filter(lambda x : x.move_type == MoveType.ATTACK, self.__moves))
    
    def add_move(self, move : Move) -> None:
        self.__moves = (*self.__moves, move)

    def trigger_callbacks(self, logic_board : LogicBoard, from_gxy : IntVector, to_gxy : IntVector):
        for move in self.__moves:
            if not move.gxy == to_gxy or move.callback is None:
                continue
            move.callback(logic_board, from_gxy, to_gxy)
