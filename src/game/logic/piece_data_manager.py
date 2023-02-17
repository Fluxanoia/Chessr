from typing import Optional

from src.engine.factory import Factory
from src.game.board import Board, LogicBoard
from src.game.logic.move_data import (ManoeuvreCallback, Move, MoveData, Moves,
                                      MoveType)
from src.game.logic.piece_data import PieceData
from src.game.logic.piece_tag import PieceTag, PieceTagType
from src.game.sprites.board_cell import BoardCell
from src.utils.enums import (LogicState, PieceColour, PieceType, Side,
                             enum_as_list)
from src.utils.helpers import IntVector, add_vectors, inbounds, is_empty


class PieceDataManager():

    def __init__(self) -> None:
        self.__data : dict[PieceType, PieceData] = {
            PieceType.QUEEN : PieceData('Q', (
                MoveData((1, 0), True, True),
                MoveData((1, 1), True, True)
            )),
            PieceType.KING : PieceData('K', (
                MoveData((1, 0), True, False),
                MoveData((1, 1), True, False)
            )),
            PieceType.BISHOP : PieceData('B', (
                MoveData((1, 1), True, True),
            )),
            PieceType.ROOK : PieceData('R', (
                MoveData((1, 0), True, True),
            )),
            PieceType.KNIGHT : PieceData('N', (
                MoveData((2, 1), True, False),
                MoveData((2, -1), True, False),
            )),
            PieceType.PAWN : PieceData(' ', (
                MoveData((-1, 0), False, False, (MoveType.MOVE,)),
                MoveData((-1, -1), False, False, (MoveType.ATTACK,)),
                MoveData((-1, 1), False, False, (MoveType.ATTACK,))
            ))
        }

        if not all(map(lambda p : p in self.__data.keys(), enum_as_list(PieceType))):
            raise SystemExit('Some piece types are undefined.')

    def load_board(self, board : Board, board_name : str = 'default') -> None:
        file_data = Factory.get().file_manager.load_board(f'{board_name}.board')
        if file_data is None:
            raise SystemExit('The board file data could not be found.')

        width, height = None, None
        for key, value in file_data.items():
            if key == 'w':
                width = int(value)
            elif key == 'h':
                height = int(value)

        if width is None or height is None or width < 0 or height < 0:
            raise SystemError('Invalid width and height for board, ' \
                + f'width: \'{width}\', height: \'{height}\'.')

        board.reset(width, height)

        def get_piece_colour(side : Side) -> PieceColour:
            if side == Side.FRONT:
                return PieceColour.WHITE
            if side == Side.BACK:
                return PieceColour.BLACK
            raise SystemExit(f'Unexpected side value \'{side}\'.')

        for key, value in file_data.items():
            if not len(key) == 2:
                continue
            side = self.__get_side_from_text(key[0])
            piece = self.__get_piece_from_text(key[1])
            coords = map(lambda c : self.__get_coordinate_from_text(c, height), value.split(' '))
            for (i, j) in coords:
                cell = board.at(i, j)
                if cell is None:
                    continue
                if not isinstance(cell, BoardCell):
                    raise SystemExit('Expected display element.')    
                cell.add_piece(get_piece_colour(side), piece, side)

    def __get_piece_from_text(self, c : str) -> PieceType:
        for piece_type, piece_data in self.__data.items():
            if piece_data.char == c:
                return piece_type
        raise SystemExit(f'Invalid piece character \'{c}\'.')

    def __get_side_from_text(self, c : str) -> Side:
        if c == 'w':
            return Side.FRONT
        if c == 'b':
            return Side.BACK
        raise SystemExit(f'Invalid side character \'{c}\'.')

    def __get_coordinate_from_text(self, coord : str, board_height : int) -> IntVector:
        if len(coord) != 2:
            raise SystemExit(f'Incorrect coordinate format \'{coord}\'.')
        i = board_height - int(coord[1])
        j = ord(coord[0].lower()) - ord('a')
        return (i, j)

    ##################################
    ###### MOVES AND GAME STATE ######
    ##################################

    def __in_check(
        self,
        logic_board : LogicBoard,
        side : Side
    ) -> bool:
        endangered_cells = self.get_endangered_cells(logic_board, side)
        for i in range(logic_board.height):
            for j in range(logic_board.width):
                piece = logic_board.piece_at(i, j)
                if piece is None or piece.type != PieceType.KING or piece.side != side:
                    continue
                if (i, j) in endangered_cells:
                    return True
        return False

    def get_state(
        self,
        logic_board : LogicBoard,
        side : Side
    ) -> LogicState:
        check = self.__in_check(logic_board, side)

        if check:
            for i in range(logic_board.height):
                for j in range(logic_board.width):
                    from_gxy = (i, j)
                    piece = logic_board.piece_at(*from_gxy)
                    if piece is None or piece.side != side:
                        continue
                    moves = self.get_valid_moves(logic_board, from_gxy)
                    for to_gxy in moves:
                        copy = logic_board.copy()
                        copy.move(from_gxy, to_gxy)
                        if not self.__in_check(copy, side):
                            return LogicState.CHECK
            return LogicState.CHECKMATE
            
        for i in range(logic_board.height):
            for j in range(logic_board.width):
                gxy = (i, j)
                piece = logic_board.piece_at(*gxy)
                if piece is None or piece.side != side:
                    continue
                moves = self.get_valid_moves(logic_board, gxy)
                if not is_empty(moves):
                    return LogicState.NONE

        return LogicState.STALEMATE

    def get_endangered_cells(self, logic_board : LogicBoard, side : Side):
        def get_possible_attacks(i : int, j : int) -> tuple[IntVector, ...]:
            moves = logic_board.moves_at(i, j)
            return tuple() if moves is None else moves.get_moves(MoveType.ATTACK, None)
    
        attacks : list[IntVector] = []

        for i in range(logic_board.height):
            for j in range(logic_board.width):
                piece = logic_board.piece_at(i, j)
                if piece is None or piece.side == side:
                    continue
                attacks.extend(get_possible_attacks(i, j))

        return tuple(set(attacks))

    def get_valid_moves(self, logic_board : LogicBoard, gxy : IntVector) -> tuple[IntVector, ...]:
        moves_object = logic_board.moves_at(*gxy)
        piece = logic_board.piece_at(*gxy)
        if moves_object is None or piece is None:
            return tuple()

        moves = moves_object.get_moves(MoveType.MOVE, True)
        attacks = moves_object.get_moves(MoveType.ATTACK, True)

        for attack in attacks:
            piece_to_take = logic_board.piece_at(*attack)
            if piece_to_take is None or piece_to_take.side == piece.side:
                continue

            moves = (*moves, attack)

        if piece.type == PieceType.KING:
            def is_valid_move(move : IntVector):
                copy = logic_board.copy()
                copy.move(gxy, move)
                return not self.__in_check(copy, piece.side)
            moves = tuple(filter(is_valid_move, moves))

        return moves
    
    def get_moves(
        self,
        logic_board : LogicBoard,
    ) -> tuple[tuple[Optional[Moves]]]:
        moves : list[tuple[Optional[Moves]]] = []

        for i in range(logic_board.height):
            row : list[Optional[Moves]] = []
            for j in range(logic_board.width):
                gxy = (i, j)
                piece = logic_board.piece_at(*gxy)
                if piece is None:
                    row.append(None)
                else:
                    moves_object = self.__data[piece.type].get_moves(logic_board, piece.side, gxy)
                    for (move, callback) in self.__get_manoeuvres(logic_board, gxy):
                        moves_object.add_move(move, callback)
                    row.append(moves_object)
            moves.append(tuple(row))

        return tuple(moves)

    ##########################
    ####### MANOEUVRES #######
    ##########################

    def __get_manoeuvres(
        self,
        logic_board : LogicBoard,
        gxy : IntVector
    ) -> tuple[tuple[Move, ManoeuvreCallback]]:
        manoeuvres : list[tuple[Move, ManoeuvreCallback]] = []
        manoeuvres.extend(self.__double_move_manoeuvre(logic_board, gxy))
        manoeuvres.extend(self.__en_passant_manoeuvre(logic_board, gxy))
        manoeuvres.extend(self.__castle_manoeuvre(logic_board, gxy))
        return tuple(manoeuvres)

    def __double_move_manoeuvre(
        self,
        logic_board : LogicBoard,
        gxy : IntVector
    ) -> tuple[tuple[Move, ManoeuvreCallback]]:
        piece = logic_board.piece_at(*gxy)
        if piece is None \
            or not piece.type == PieceType.PAWN \
            or piece.has_tag(PieceTagType.HAS_MOVED):
            return tuple()

        forward_vector = PieceData.get_forward_vector(piece.side)
        inbetween_gxy = add_vectors(gxy, forward_vector)
        if not inbounds(logic_board.width, logic_board.height, inbetween_gxy) \
            or not logic_board.piece_at(*inbetween_gxy) is None:
            return tuple()

        def double_move_callback(_src : IntVector, dst : IntVector) -> None:
            piece = logic_board.piece_at(*dst)
            if piece is None:
                return
            piece.add_tag(PieceTag.get_tag(PieceTagType.EN_PASSANT))

        move = Move(
            add_vectors(inbetween_gxy, forward_vector),
            MoveType.MOVE,
            True
        )
        return tuple([(move, double_move_callback)])

    def __en_passant_manoeuvre(
        self,
        logic_board : LogicBoard,
        gxy : IntVector
    ) -> tuple[tuple[Move, ManoeuvreCallback]]:
        piece = logic_board.piece_at(*gxy)
        if piece is None or not piece.type == PieceType.PAWN:
            return tuple()

        manoeuvres : list[IntVector] = []

        forward_vector = PieceData.get_forward_vector(piece.side)
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

        def en_passant_callback(src : IntVector, dst : IntVector) -> None:
            logic_board.remove(src[0], dst[1])

        return tuple(map(
            lambda x : (Move(x, MoveType.MOVE, True), en_passant_callback),
            manoeuvres))

    def __castle_manoeuvre(
        self,
        logic_board : LogicBoard,
        gxy : IntVector
    ) -> tuple[tuple[Move, ManoeuvreCallback]]:
        king_piece = logic_board.piece_at(*gxy)
        king_row = logic_board.row_at(gxy[0])
        if king_piece is None \
            or not king_piece.type == PieceType.KING \
            or king_row is None \
            or king_piece.has_tag(PieceTagType.HAS_MOVED):
            return tuple()

        def castle_callback(src : IntVector, dst : IntVector) -> None:
            castle_direction = -1 if dst[1] < src[1] else 1
            rook_destination = (dst[0], dst[1] - castle_direction)
            j = dst[1] + castle_direction
            while 0 <= j < logic_board.width:
                position = (dst[0], j)
                piece = logic_board.piece_at(*position)
                if not piece is None and piece.type == PieceType.ROOK:
                    logic_board.move(position, rook_destination)
                    return
                j += castle_direction

        rook_columns : list[int] = []
        for cell in king_row:
            piece = cell.piece
            if piece is None \
                or piece.has_tag(PieceTagType.HAS_MOVED) \
                or not piece.type == PieceType.ROOK \
                or not piece.side == king_piece.side:
                continue

            rook_columns.append(cell.gxy[1])

        row, column = gxy
        manoeuvres : list[IntVector] = []
        for rook_column in rook_columns:
            if abs(column - rook_column) < 2:
                continue
            castle_direction = 1 if rook_column > column else -1
            columns_between = range(column + castle_direction, rook_column, castle_direction)
            pieces_between = [logic_board.piece_at(row, j) for j in columns_between]
            if all(map(lambda x : x is None, pieces_between)):
                manoeuvres.append((row, rook_column - castle_direction))

        return tuple(map(
            lambda x : (Move(x, MoveType.MOVE, True), castle_callback),
            manoeuvres))
