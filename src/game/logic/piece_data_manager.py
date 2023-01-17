from typing import Callable

from src.engine.factory import Factory
from src.game.board import Board
from src.game.logic.piece_data import PieceData
from src.game.logic.piece_tag import PieceTag, PieceTagType
from src.utils.enums import PieceColour, PieceType, Side, enum_as_list
from src.utils.helpers import IntVector, add_vectors, inbounds

ManoeuvreCallback = Callable[[IntVector, IntVector], None]

class PieceDataManager():

    def __init__(self) -> None:
        self.__data : dict[PieceType, PieceData] = {
            PieceType.QUEEN  : PieceData('Q', ((1, 0), (1, 1)), True, True),
            PieceType.KING   : PieceData('K', ((1, 0), (1, 1)), True, False),
            PieceType.BISHOP : PieceData('B', ((1, 1),), True, True),
            PieceType.ROOK   : PieceData('R', ((1, 0),), True, True),
            PieceType.KNIGHT : PieceData('N', ((2, 1), (2, -1)), True, False),
            PieceType.PAWN   : PieceData(' ', ((-1, 0),), False, False, ((-1, -1), (-1, 1)))
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

    def get_moves(
        self,
        board : Board,
        gxy : IntVector
    ) -> tuple[tuple[IntVector], tuple[tuple[IntVector, ManoeuvreCallback]]]:
        moves = list(self.__get_normal_moves(board, gxy))
        manoeuvres = self.__get_manoeuvres(board, gxy)

        moves.extend(map(lambda x : x[0], manoeuvres))

        return (tuple(moves), manoeuvres)

    def __get_normal_moves(
        self,
        board : Board,
        gxy : IntVector
    ) -> tuple[IntVector,...]:
        piece = board.piece_at(*gxy)
        if piece is None:
            return tuple([tuple(), tuple()])
        return self.__data[piece.type].get_normal_moves(board, piece.side, gxy)

    def __get_manoeuvres(
        self,
        board : Board,
        gxy : IntVector
    ) -> tuple[tuple[IntVector, ManoeuvreCallback]]:
        piece = board.piece_at(*gxy)
        if piece is None:
            return tuple()

        manoeuvres : list[tuple[IntVector, ManoeuvreCallback]] = []

        if piece.type == PieceType.PAWN:
            manoeuvres.extend(self.__double_move_manoeuvre(board, gxy))
            manoeuvres.extend(self.__en_passant_manoeuvre(board, gxy))

        if piece.type == PieceType.KING:
            manoeuvres.extend(self.__castle_manoeuvre(board, gxy))

        return tuple(manoeuvres)

    def __double_move_manoeuvre(
        self,
        board : Board,
        gxy : IntVector
    ) -> tuple[tuple[IntVector, ManoeuvreCallback]]:
        piece = board.piece_at(*gxy)
        if piece is None or piece.has_tag(PieceTagType.HAS_MOVED):
            return tuple()

        piece_data = self.__data[piece.type]
        forward_vector = piece_data.side_transform_vector((-1, 0), piece.side)
        inbetween_gxy = add_vectors(gxy, forward_vector)
        if not inbounds(board.width, board.height, inbetween_gxy) \
            or not board.piece_at(*inbetween_gxy) is None:
            return tuple()

        def double_move_callback(_src : IntVector, dst : IntVector) -> None:
            piece = board.piece_at(*dst)
            if piece is None:
                return
            piece.add_tag(PieceTag.get_tag(PieceTagType.EN_PASSANT))

        return tuple([(add_vectors(inbetween_gxy, forward_vector), double_move_callback,)])

    def __en_passant_manoeuvre(
        self,
        board : Board,
        gxy : IntVector
    ) -> tuple[tuple[IntVector, ManoeuvreCallback]]:
        piece = board.piece_at(*gxy)
        if piece is None:
            return tuple()

        manoeuvres : list[IntVector] = []
        piece_data = self.__data[piece.type]

        forward_vector = piece_data.side_transform_vector((-1, 0), piece.side)
        en_passant_vectors = ((0, -1), (0, 1))
        for en_passant_vector in en_passant_vectors:
            en_passant_gxy = add_vectors(gxy, en_passant_vector)
            if not inbounds(board.width, board.height, en_passant_gxy):
                continue

            piece_to_take = board.piece_at(*en_passant_gxy)
            if piece_to_take is None:
                continue

            if piece_to_take.type == PieceType.PAWN \
                and piece_to_take.has_tag(PieceTagType.EN_PASSANT):
                move = add_vectors(en_passant_vector, forward_vector)
                manoeuvres.append(add_vectors(gxy, move))

        def en_passant_callback(src : IntVector, dst : IntVector) -> None:
            board.remove(src[0], dst[1])

        return tuple(map(lambda x : (x, en_passant_callback), manoeuvres))

    def __castle_manoeuvre(
        self,
        board : Board,
        gxy : IntVector
    ) -> tuple[tuple[IntVector, ManoeuvreCallback]]:
        king_piece = board.piece_at(*gxy)
        king_row = board.row_at(gxy[0])
        if king_piece is None or king_row is None or king_piece.has_tag(PieceTagType.HAS_MOVED):
            return tuple()

        def castle_callback(src : IntVector, dst : IntVector) -> None:
            castle_direction = -1 if dst[1] < src[1] else 1
            rook_destination = (dst[0], dst[1] - castle_direction)
            j = dst[1] + castle_direction
            while 0 <= j < board.width:
                position = (dst[0], j)
                piece = board.piece_at(*position)
                if not piece is None and piece.type == PieceType.ROOK:
                    board.move(position, rook_destination)
                    return
                j += castle_direction

        rook_columns : list[int] = []
        for cell in king_row:
            if cell is None:
                continue

            piece = cell.get_piece()
            if piece is None \
                or piece.has_tag(PieceTagType.HAS_MOVED) \
                or not piece.type == PieceType.ROOK \
                or not piece.side == king_piece.side:
                continue

            rook_columns.append(cell.grid_position[1])

        row, column = gxy
        manoeuvres : list[IntVector] = []
        for rook_column in rook_columns:
            if abs(column - rook_column) < 2:
                continue
            castle_direction = 1 if rook_column > column else -1
            columns_between = range(column + castle_direction, rook_column, castle_direction)
            pieces_between = [board.piece_at(row, j) for j in columns_between]
            if all(map(lambda x : x is None, pieces_between)):
                manoeuvres.append((row, rook_column - castle_direction))

        return tuple(map(lambda x : (x, castle_callback), manoeuvres))
