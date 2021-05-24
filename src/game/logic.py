from src.utils.enum import enum_as_list
from src.game.enums import PieceTag, PieceType, Side
from src.utils.globals import Singleton, instance


def v_add(x, y):
    return (x[0] + y[0], x[1] + y[1])
def is_singular_vector(v):
    return isinstance(v, (list, tuple)) and any(not isinstance(w, (list, tuple)) for w in v)

def inbounds(bw, bh, cell):
    i, j = cell
    return 0 <= i < bh and 0 <= j < bw

class PieceData:

    def __init__(self, _char, move_vectors, revolve, expand, challenge_vectors = None):
        self.__char = _char
        self.__move_vectors = move_vectors
        self.__challenge_vectors = challenge_vectors
        self.__expand = expand
        self.__revolve = revolve
        if revolve:
            self.__move_vectors = self.__revolve_vectors(self.__move_vectors)
            if self.__challenge_vectors is not None:
                self.__challenge_vectors = self.__revolve_vectors(self.__challenge_vectors)

    def __revolve_vectors(self, vectors):
        if is_singular_vector(vectors):
            return self.__revolve_vectors((vectors,))[0]
        revolved = []
        for v in vectors:
            revolved.append(v)
            for _ in range(3):
                i, j = revolved[-1]
                revolved.append((j, -i))
        return tuple(revolved)
    def __flip_vectors(self, vectors):
        if is_singular_vector(vectors):
            return self.__flip_vectors((vectors,))[0]
        flipped = []
        for (i, j) in vectors:
            flipped.append((-i, j))
        return flipped
    def vector_transform(self, info, v):
        do_flip = not self.__revolve and info.get_side() == Side.BACK
        if do_flip:
            v = self.__flip_vectors(v)
        return v

    def get_move_and_challenge_cells(self, board, cell):
        moves = []
        challenges = []
        info = board.at(*cell)
        board_size = board.get_size()

        def check_and_add_cell(c, challenge = False):
            if not inbounds(*board_size, c):
                return False
            if board.at(*c) is not None:
                if challenge or self.__challenge_vectors is None:
                    challenges.append(c)
                return False
            if not challenge:
                moves.append(c)
            return self.__expand

        for v in self.vector_transform(info, self.__move_vectors):
            c = v_add(cell, v)
            while check_and_add_cell(c):
                c = v_add(c, v)

        if self.__challenge_vectors is None:
            return (tuple(moves), tuple(challenges))

        for v in self.vector_transform(info, self.__challenge_vectors):
            c = v_add(cell, v)
            while check_and_add_cell(c, True):
                c = v_add(c, v)
        return (tuple(moves), tuple(challenges))

    def get_char(self): return self.__char

class Logic(Singleton):

    def __init__(self):
        super().__init__()
        self.__data = {}
        self.__data[PieceType.QUEEN] = PieceData('Q', ((1, 0), (1, 1)), True, True)
        self.__data[PieceType.KING] = PieceData('K', ((1, 0), (1, 1)), True, False)
        self.__data[PieceType.BISHOP] = PieceData('B', ((1, 1),), True, True)
        self.__data[PieceType.ROOK] = PieceData('R', ((1, 0),), True, True)
        self.__data[PieceType.KNIGHT] = PieceData('N', ((2, 1), (2, -1)), True, False)
        self.__data[PieceType.PAWN] = PieceData(' ', ((-1, 0),), False, False, ((-1, -1), (-1, 1)))
        if not all(map(lambda p: p in self.__data.keys(), enum_as_list(PieceType))):
            raise SystemExit("Not all piece types are categorised.")

    def get_piece(self, c):
        for key in self.__data:
            if self.__data[key].get_char() == c:
                return key
        raise Exception("Invalid piece character.")

    def get_coordinate(self, coord, board_height):
        if len(coord) != 2:
            raise Exception("Incorrect coordinate format.")
        i = board_height - int(coord[1])
        j = ord(coord[0].lower()) - ord('a')
        return (i, j)

    def get_base_row(self, board, side):
        return 0 if side == Side.BACK else board.get_height() - 1
    def get_move_and_challenge_cells(self, board, cell):
        info = board.at(*cell)
        if info is None:
            return None
        return self.get_data(info.get_piece()).get_move_and_challenge_cells(board, cell)
    def get_special_manoeuvres(self, board, cell):
        manoeuvres = []
        info = board.at(*cell)
        piece = info.get_piece()
        if info is not None:
            if piece is PieceType.PAWN:
                manoeuvres.extend(self.__double_move_manoeuvre(board, cell))
                manoeuvres.extend(self.__en_passant_manoeuvre(board, cell))
            if piece is PieceType.KING:
                manoeuvres.extend(self.__castle_manoeuvre(board, cell))
        return tuple(manoeuvres)

    def __double_move_manoeuvre(self, board, cell):
        def double_move_callback(_src, dst, controller):
            controller.at(*dst).get_piece().add_tag(PieceTag.DOUBLE_MOVE)
        info = board.at(*cell)
        size = board.get_size()
        data = self.get_data(info.get_piece())
        if not info.has_tag(PieceTag.HAS_MOVED):
            v = data.vector_transform(info, (-1, 0))
            c = v_add(cell, v)
            if inbounds(*size, c) and board.at(*c) is None:
                return ((v_add(c, v), double_move_callback),)
        return tuple()
    def __en_passant_manoeuvre(self, board, cell):
        def en_passant_callback(src, dst, controller):
            controller.remove((src[0], dst[1]))
        manoeuvres = []
        info = board.at(*cell)
        size = board.get_size()
        data = self.get_data(info.get_piece())
        ep_row = self.get_base_row(board, info.get_side()) \
            + data.vector_transform(info, (4 - board.get_height(), 0))[0]
        forward_vector = data.vector_transform(info, (-1, 0))
        if cell[0] == ep_row:
            for v in ((0, -1), (0, 1)):
                c = v_add(cell, v)
                if not inbounds(*size, c):
                    continue
                adj = board.at(*c)
                if adj is None:
                    continue
                if adj.get_piece() is PieceType.PAWN and adj.has_tag(PieceTag.DOUBLE_MOVE):
                    move = v_add(v, forward_vector)
                    manoeuvres.append((v_add(cell, move), en_passant_callback))
        return tuple(manoeuvres)
    def __castle_manoeuvre(self, board, cell):
        king_info = board.at(*cell)
        if king_info.has_tag(PieceTag.HAS_MOVED):
            return tuple()
        def castle_callback(src, dst, controller):
            direction = -1 if dst[1] < src[1] else 1
            b = (dst[0], dst[1] - direction)
            j = dst[1] + direction
            while 0 <= j < controller.get_width():
                a = (dst[0], j)
                cell = controller.at(*a)
                if cell.get_piece().get_type() is PieceType.ROOK:
                    controller.move(a, b)
                    return
                j += direction
        manoeuvres = []
        row, column = cell
        side = king_info.get_side()
        def rook_check(c):
            return c is not None \
                and not c.has_tag(PieceTag.HAS_MOVED) \
                and c.get_piece() is PieceType.ROOK \
                and c.get_side() is side
        rooks = map(lambda c : c.get_position()[1], filter(rook_check, board.row_at(row)))
        for rook in rooks:
            if abs(column - rook) < 2:
                continue
            direction = 1 if rook > column else -1
            cells_between = [board.at(row, j) for j in range(column + direction, rook, direction)]
            if all(map(lambda x : x is None, cells_between)):
                manoeuvres.append((row, column + 2 * direction))
        return tuple(map(lambda x : (x, castle_callback), manoeuvres))

    def get_data(self, piece):
        return self.__data[piece]
    def get_char(self, piece):
        return self.get_data(piece).get_char()

class SimpleBoard():

    def __init__(self, board):
        self.__width = board.get_width()
        self.__height = board.get_height()
        self.__board = []
        for i in range(self.__height):
            row = []
            for j in range(self.__width):
                cell = board.at(i, j)
                row.append(cell.get_info())
            self.__board.append(row)

    def at(self, i, j):
        return self.__board[i][j]
    def row_at(self, i):
        return self.__board[i]

    def get_width(self):
        return self.__width
    def get_height(self):
        return self.__height
    def get_size(self):
        return (self.__width, self.__height)

    def __str__(self):
        s = ""
        for i in range(self.__height):
            for j in range(self.__width):
                piece = self.__board[i][j]
                if piece is not None:
                    piece = piece.get_piece()
                c = '-' if piece is None else instance(Logic).get_char(piece)
                s += c + ' '
            s += '\n'
        return s
