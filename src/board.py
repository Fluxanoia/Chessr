import pygame as pg
from src.enum import enum_as_list
from src.groups import Groups
from src.globals import Globals, Singleton, MouseButton, instance
from src.spritesheet import Spritesheet
from src.board_enums import PieceTag, BoardColour, BoardType, PieceColour, PieceType, Side
from src.board_sprites import BoardCell

def v_add(x, y):
    return (x[0] + y[0], x[1] + y[1])
def is_singular_vector(v):
    return isinstance(v, (list, tuple)) and any(not isinstance(w, (list, tuple)) for w in v)

def inbounds(board_size, cell):
    if isinstance(cell, tuple):
        return all(map(lambda x: inbounds(board_size, x), cell))
    return 0 <= cell < board_size

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
        board_size = board.get_size()
        info = board.at(*cell)

        def check_and_add_cell(c, challenge = False):
            if not inbounds(board_size, c):
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
        self.__data[PieceType.KNIGHT] = PieceData('K', ((2, 1), (2, -1)), True, False)
        self.__data[PieceType.PAWN] = PieceData('P', ((-1, 0),), False, False, ((-1, -1), (-1, 1)))
        if not all(map(lambda p: p in self.__data.keys(), enum_as_list(PieceType))):
            raise SystemExit("Not all piece types are categorised.")

    def get_base_row(self, board, side):
        return 0 if side == Side.BACK else board.get_size() - 1
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
        def double_move_callback(_src, dst, board):
            board.at(*dst).get_piece().add_tag(PieceTag.DOUBLE_MOVE)
        info = board.at(*cell)
        size = board.get_size()
        data = self.get_data(info.get_piece())
        if not info.has_tag(PieceTag.HAS_MOVED):
            v = data.vector_transform(info, (-1, 0))
            c = v_add(cell, v)
            if inbounds(size, c) and board.at(*c) is None:
                return ((v_add(c, v), double_move_callback),)
        return tuple()
    def __en_passant_manoeuvre(self, board, cell):
        def en_passant_callback(src, dst, board):
            board.game_remove((src[0], dst[1]))
        manoeuvres = []
        info = board.at(*cell)
        size = board.get_size()
        data = self.get_data(info.get_piece())
        ep_row = self.get_base_row(board, info.get_side()) \
            + data.vector_transform(info, (4 - size, 0))[0]
        forward_vector = data.vector_transform(info, (-1, 0))
        if cell[0] == ep_row:
            for v in ((0, -1), (0, 1)):
                c = v_add(cell, v)
                if not inbounds(size, c):
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
        def castle_callback(src, dst, board):
            direction = -1 if dst[1] < src[1] else 1
            b = (dst[0], dst[1] - direction)
            j = dst[1] + direction
            while 0 <= j < board.get_size():
                a = (dst[0], j)
                cell = board.at(*a)
                if cell.get_piece().get_type() is PieceType.ROOK:
                    board.game_move(a, b)
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
        self.__size = board.get_size()
        self.__board = []
        for i in range(self.__size):
            row = []
            for j in range(self.__size):
                cell = board.at(i, j)
                row.append(cell.get_info())
            self.__board.append(row)

    def at(self, i, j):
        return self.__board[i][j]
    def row_at(self, i):
        return self.__board[i]

    def get_size(self):
        return self.__size

    def __str__(self):
        s = ""
        for i in range(self.__size):
            for j in range(self.__size):
                piece = self.__board[i][j]
                if piece is not None:
                    piece = piece.get_piece()
                c = '-' if piece is None else instance(Logic).get_char(piece)
                s += c + ' '
            s += '\n'
        return s

class Board():

    def __init__(self, colour = BoardColour.BLACK_WHITE, scale = 3, cell_scale = 1.25):
        self.__colour = colour
        self.__scale = scale
        self.__cell_scale = scale * cell_scale

        self.__pressed = None
        self.__selected = None
        self.__inactive_timer = None

        self.__load_default_layout()

    def __calculate_offsets(self):
        def get_offset(x):
            return (x - Spritesheet.BOARD_WIDTH * self.__cell_scale * self.__size) / 2
        self.__x_offset, self.__y_offset = map(get_offset, instance(Globals).get_window_size())
    def __get_cell_type(self, i, j):
        return self.__cell_types[(i + j) % len(self.__cell_types)]
    def __fill_board(self):
        self.__board = []
        self.__calculate_offsets()
        for i in range(self.__size):
            row = []
            for j in range(self.__size):
                row.append(BoardCell((i, j),
                                     self.__get_cell_position(i, j),
                                     self.__colour,
                                     self.__get_cell_type(i, j),
                                     self.__cell_scale,
                                     self.__scale))
            self.__board.append(row)
    def __load_default_layout(self):
        self.__size = 8
        self.__cell_types = (BoardType.LIGHT, BoardType.DARK)
        self.__fill_board()

        colours = (PieceColour.BLACK, PieceColour.WHITE)
        def colour(i): return colours[0 if i < self.__size / 2 else 1]
        def side(i): return Side.BACK if i < self.__size / 2 else Side.FRONT

        base_rows = (0, self.__size - 1)
        base_info = (
            (PieceType.ROOK, (0, self.__size - 1)),
            (PieceType.KNIGHT, (1, self.__size - 2)),
            (PieceType.BISHOP, (2, self.__size - 3)),
            (PieceType.QUEEN, (3,)),
            (PieceType.KING, (self.__size - 4,)),
        )
        for _type, cols in base_info:
            for i in base_rows:
                for j in cols:
                    self.__board[i][j].place_piece(colour(i), _type, side(i))

        pawn_rows = (1, self.__size - 2)
        for i in pawn_rows:
            for j in range(self.__size):
                self.__board[i][j].place_piece(colour(i), PieceType.PAWN, side(i))

    def at(self, i, j):
        return self.__board[i][j]
    def __get_cell_position(self, i, j):
        return (self.__x_offset + j * Spritesheet.BOARD_WIDTH * self.__cell_scale,
                self.__y_offset + i * Spritesheet.BOARD_WIDTH * self.__cell_scale)

    def __is_inactive(self):
        if self.__inactive_timer is not None:
            if self.__inactive_timer.has_not_started():
                return False
            if self.__inactive_timer.finished():
                self.__inactive_timer = None
                return False
            return True
        return False
    def update(self):
        if self.__is_inactive():
            return

    def game_move(self, a, b):
        if not self.at(*a).has_piece() or a == b:
            return
        self.at(*b).transfer_from(self.at(*a))
        for (xy, callback) in self.__moves[2]:
            if xy == b:
                callback(a, b, self)
    def game_remove(self, a):
        self.at(*a).remove_piece()

    def __get_collision(self, pos):
        for s in reversed(instance(Groups).get_board_cells()):
            if s.collidepoint(pos):
                return s.get_grid_position()
        return None
    def pressed(self, event):
        if self.__is_inactive():
            return
        if event.button == MouseButton.LEFT:
            self.__pressed = self.__get_collision(pg.mouse.get_pos())
    def released(self, event):
        if self.__is_inactive():
            return
        if event.button == MouseButton.LEFT:
            _released = self.__get_collision(pg.mouse.get_pos())
            if self.__pressed == _released:
                self.__clicked(self.__pressed)
    def __clicked(self, gxy):
        if self.__is_inactive():
            return
        if gxy is not None:
            if gxy == self.__selected:
                pass
            elif self.at(*gxy).has_piece():
                if self.__selected is not None:
                    self.at(*self.__selected).unselect()
                self.__selected = gxy
                self.at(*gxy).select()
            elif self.__selected is not None:
                self.game_move(self.__selected, gxy)
                self.__selected = None
        elif self.__selected is not None:
            self.at(*self.__selected).unselect()
            self.__selected = None
        self.__update_highlighting()

    def __get_all_moves(self, gxy):
        logic = instance(Logic)
        board = SimpleBoard(self)
        return (*logic.get_move_and_challenge_cells(board, gxy),
                logic.get_special_manoeuvres(board, gxy))
    def __update_highlighting(self):
        if self.__selected is None:
            for i in range(self.__size):
                for j in range(self.__size):
                    self.at(i, j).fallback_type()
        else:
            self.__moves = self.__get_all_moves(self.__selected)
            if self.__moves is not None:
                moves, challenges, special = self.__moves
                for i in range(self.__size):
                    for j in range(self.__size):
                        cell = self.at(i, j)
                        if (i, j) in moves:
                            cell.set_temporary_type(BoardType.MOVE)
                        elif (i, j) in challenges:
                            cell.set_temporary_type(BoardType.DANGER)
                        elif (i, j) in map(lambda x: x[0], special):
                            cell.set_temporary_type(BoardType.DEBUG)
                        else:
                            cell.fallback_type()

    def get_size(self):
        return self.__size
