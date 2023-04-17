from typing import Callable, Optional

from src.logic.logic_board import LogicBoard, Move, Moves
from src.logic.logic_piece import LogicPiece
from src.logic.move_data import MoveType
from src.logic.piece_move_calculator import PieceMoveCalculator
from src.logic.piece_move_calculators import PieceMoveCalculators
from src.logic.piece_tag import PieceTag, PieceTagType
from src.utils.enums import LogicState, PendingMoveType, PieceType, Side
from src.utils.helpers import IntVector, add_vectors, inbounds, is_empty


class MoveLogic():

#region Game State

    def get_state(
        self,
        logic_board : LogicBoard,
        side : Side
    ) -> LogicState:
        '''
            Calculates the state of the game, whether the given side is in
            check, checkmated, stalemated, or none of the above.
        '''

        if logic_board.is_dirty():
            logic_board.clean()

        check = self.__in_check(logic_board, side)

        if check:
            for i in range(logic_board.height):
                for j in range(logic_board.width):
                    from_gxy = (i, j)
                    piece = logic_board.piece_at(*from_gxy)
                    if piece is None or piece.side != side:
                        continue
                    moves = logic_board.moves_at(*from_gxy)
                    if moves is None:
                        continue
                    for move in moves.get_valid_moves():
                        if not self.__move_results_in_check(logic_board, from_gxy, move.gxy, side):
                            return LogicState.CHECK
            return LogicState.CHECKMATE
            
        for i in range(logic_board.height):
            for j in range(logic_board.width):
                gxy = (i, j)
                piece = logic_board.piece_at(*gxy)
                if piece is None or piece.side != side:
                    continue
                moves = logic_board.moves_at(*gxy)
                if moves is None:
                    continue
                if not is_empty(moves.get_valid_moves()):
                    return LogicState.NONE

        return LogicState.STALEMATE
    
#endregion

#region Moves

    def supply_moves(
        self,
        logic_board : LogicBoard
    ) -> None:
        '''
            Using the PieceData logic, we can draft a list of possible moves
            per piece. These moves don't take into account the moves of other
            pieces. As such, we need to reiterate over the set of moves to
            ensure the moves comply with check/checkmating rules.
        '''

        self.__supply_partial_moves(logic_board)

        for i in range(logic_board.height):
            for j in range(logic_board.width):
                gxy = (i, j)
                piece = logic_board.piece_at(*gxy)
                moves = logic_board.moves_at(*gxy)
                if piece is None or moves is None:
                    continue
                for move in moves.get_valid_moves():
                    if self.__move_results_in_check(logic_board, gxy, move.gxy, piece.side):
                        move.invalidate()

        self.__supply_manoeuvres(logic_board, self.__get_complex_manoeuvres)

    def __supply_partial_moves(
        self,
        logic_board : LogicBoard
    ) -> None:
        '''
            When checking if a future move puts a side into check, we don't
            need to account for moves made invalid by putting the other side
            into check. You can check the opposition with a move that would
            put yourself in check.

            As such, here we supply the moves as-is from the PieceData, and
            that's all.
        '''

        moves_grid : list[tuple[Optional[Moves]]] = []

        piece_move_calculators = PieceMoveCalculators.get()

        for i in range(logic_board.height):
            row : list[Optional[Moves]] = []
            for j in range(logic_board.width):
                gxy = (i, j)
                piece = logic_board.piece_at(*gxy)
                if piece is None:
                    row.append(None)
                else:
                    moves = piece_move_calculators \
                        .get_calculator(piece.type) \
                        .get_moves(logic_board, piece.side, gxy)

                    for move in moves.get_all_moves():
                        self.__supply_pending_action(logic_board, piece, move)

                    row.append(moves)
            moves_grid.append(tuple(row))

        logic_board.supply_moves(tuple(moves_grid))

        self.__supply_manoeuvres(logic_board, self.__get_manoeuvres)

    def __supply_pending_action(
        self,
        logic_board : LogicBoard,
        piece : LogicPiece,
        move : Move
    ) -> None:
        if (piece.type == PieceType.PAWN
            and PieceMoveCalculator.get_away_row(logic_board, piece.side) == move.gxy[0]):
            move.set_pending_action(PendingMoveType.PIECE_PROMOTION)

    def __supply_manoeuvres(
        self,
        logic_board : LogicBoard,
        get_manoeuvres : Callable[[LogicBoard, IntVector], tuple[Move]]
    ):
        '''
            Adds manoeuvres to the available moves of a board.
        '''

        for i in range(logic_board.height):
            for j in range(logic_board.width):
                gxy = (i, j)
                moves = logic_board.moves_at(*gxy)
                if moves is None:
                    continue
                for move in get_manoeuvres(logic_board, gxy):
                    moves.add_move(move)

#endregion

#region Board State

    def __move_results_in_check(
        self,
        logic_board : LogicBoard,
        from_gxy : IntVector,
        to_gxy : IntVector,
        side : Side
    ):
        copy = logic_board.copy()
        copy.move(from_gxy, to_gxy)
        self.__supply_partial_moves(copy)
        return self.__in_check(copy, side)

    def __get_endangered_cells(
        self,
        logic_board : LogicBoard,
        side : Side
    ) -> tuple[IntVector, ...]:
        '''
            Returns all the grid positions that are under attack by the opposing side.
        '''

        attacks : list[IntVector] = []

        for i in range(logic_board.height):
            for j in range(logic_board.width):
                piece = logic_board.piece_at(i, j)
                if piece is None or piece.side == side:
                    continue
                moves = logic_board.moves_at(i, j)
                if moves is None:
                    continue
                possible_attacks = moves.get_possible_attacks()
                attacks.extend(map(lambda x : x.gxy, possible_attacks))

        return tuple(set(attacks))
    
    def __in_check(
        self,
        logic_board : LogicBoard,
        side : Side
    ) -> bool:
        '''
            Returns whether this side is in check or not.
        '''

        endangered_cells = self.__get_endangered_cells(logic_board, side)
        for i in range(logic_board.height):
            for j in range(logic_board.width):
                piece = logic_board.piece_at(i, j)
                if piece is None or piece.type != PieceType.KING or piece.side != side:
                    continue
                if (i, j) in endangered_cells:
                    return True
        return False

#endregion

#region Manoeuvres

    '''
        Manoeuvres are a way of implementing moves that depend on complex conditions
        such as the state of other pieces or cells on the board.
        They must self-validate as they are added to the board without any validation.
    '''

    def __get_manoeuvres(
        self,
        logic_board : LogicBoard,
        gxy : IntVector
    ) -> tuple[Move]:
        '''
            These manoeuvres only rely on PieceTags and the piece positions
            on the board.
        '''
        manoeuvres : list[Move] = []
        manoeuvres.extend(self.__double_move_manoeuvre(logic_board, gxy))
        manoeuvres.extend(self.__en_passant_manoeuvre(logic_board, gxy))
        return tuple(manoeuvres)
    
    def __get_complex_manoeuvres(
        self,
        logic_board : LogicBoard,
        gxy : IntVector
    ) -> tuple[Move]:
        '''
            These manoeuvres rely on the available moves of the opposition,
            so can't be run on partial move supplying.
        '''
        return tuple(self.__castle_manoeuvre(logic_board, gxy))

    def __double_move_manoeuvre(
        self,
        logic_board : LogicBoard,
        gxy : IntVector
    ) -> tuple[Move]:
        piece = logic_board.piece_at(*gxy)
        if piece is None \
            or not piece.type == PieceType.PAWN \
            or piece.has_tag(PieceTagType.HAS_MOVED):
            return tuple()

        forward_vector = PieceMoveCalculator.get_forward_vector(piece.side)
        inbetween_gxy = add_vectors(gxy, forward_vector)
        final_gxy = add_vectors(inbetween_gxy, forward_vector)
        if not inbounds(logic_board.width, logic_board.height, inbetween_gxy) \
            or not inbounds(logic_board.width, logic_board.height, final_gxy) \
            or not logic_board.piece_at(*inbetween_gxy) is None \
            or not logic_board.piece_at(*final_gxy) is None:
            return tuple()

        def double_move_callback(logic_board : LogicBoard, _src : IntVector, dst : IntVector) -> None:
            piece = logic_board.piece_at(*dst)
            if piece is None:
                return
            piece.add_tag(PieceTag.get_tag(PieceTagType.EN_PASSANT))

        move = Move(
            final_gxy,
            MoveType.MOVE,
            True,
            double_move_callback
        )
        return tuple([move])

    def __en_passant_manoeuvre(
        self,
        logic_board : LogicBoard,
        gxy : IntVector
    ) -> tuple[Move]:
        piece = logic_board.piece_at(*gxy)
        if piece is None or not piece.type == PieceType.PAWN:
            return tuple()

        manoeuvres : list[IntVector] = []

        forward_vector = PieceMoveCalculator.get_forward_vector(piece.side)
        en_passant_vectors = ((0, -1), (0, 1))
        for en_passant_vector in en_passant_vectors:
            en_passant_gxy = add_vectors(gxy, en_passant_vector)
            if not inbounds(logic_board.width, logic_board.height, en_passant_gxy):
                continue

            piece_to_take = logic_board.piece_at(*en_passant_gxy)
            if piece_to_take is None:
                continue

            if piece_to_take.type == PieceType.PAWN \
                and piece_to_take.has_tag(PieceTagType.EN_PASSANT):
                move = add_vectors(en_passant_vector, forward_vector)
                manoeuvres.append(add_vectors(gxy, move))

        def en_passant_callback(logic_board : LogicBoard, src : IntVector, dst : IntVector) -> None:
            logic_board.remove(src[0], dst[1])

        return tuple(map(
            lambda x : Move(x, MoveType.MOVE, True, en_passant_callback),
            manoeuvres))

    def __castle_manoeuvre(
        self,
        logic_board : LogicBoard,
        gxy : IntVector
    ) -> tuple[Move]:
        king_piece = logic_board.piece_at(*gxy)
        king_row = logic_board.row_at(gxy[0])
        if king_piece is None \
            or not king_piece.type == PieceType.KING \
            or king_row is None \
            or king_piece.has_tag(PieceTagType.HAS_MOVED):
            return tuple()
        
        endangered_cells = self.__get_endangered_cells(logic_board, king_piece.side)
        if gxy in endangered_cells:
            return tuple()
        
        rook_columns : list[int] = []
        for cell in king_row:
            piece = cell.piece
            if piece is None \
                or piece.has_tag(PieceTagType.HAS_MOVED) \
                or not piece.type == PieceType.ROOK \
                or not piece.side == king_piece.side:
                continue

            rook_columns.append(cell.gxy[1])

        if is_empty(rook_columns):
            return tuple()

        row, column = gxy
        manoeuvres : list[IntVector] = []
        for rook_column in rook_columns:
            if abs(column - rook_column) < 2:
                continue
            castle_direction = 1 if rook_column > column else -1
            cells_between = [(row, x) for x in range(column + castle_direction, rook_column, castle_direction)]
            if any(map(lambda x : x in endangered_cells, cells_between)):
                continue
            if all(map(lambda x : x is None, [logic_board.piece_at(*x) for x in cells_between])):
                manoeuvres.append((row, rook_column - castle_direction))

        def castle_callback(logic_board : LogicBoard, src : IntVector, dst : IntVector) -> None:
            castle_direction = -1 if dst[1] < src[1] else 1
            rook_destination = (dst[0], dst[1] - castle_direction)
            j = dst[1] + castle_direction
            while 0 <= j < logic_board.width:
                position = (dst[0], j)
                piece = logic_board.piece_at(*position)
                if not piece is None and piece.type == PieceType.ROOK:
                    logic_board.move(position, rook_destination, True)
                    return
                j += castle_direction

        return tuple(map(
            lambda x : Move(x, MoveType.MOVE, True, castle_callback),
            manoeuvres))

#endregion
