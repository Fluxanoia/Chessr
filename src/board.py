import pygame as pg
from src.enum import enum_as_list
from src.timer import Timer
from src.groups import Groups
from src.tweens import Tween, TweenType
from src.globals import Globals, Singleton, MouseButton, instance
from src.spritesheet import Spritesheet, BoardColour, BoardType, PieceColour, PieceType
from src.board_sprites import BoardCell

class PieceData:

    def __init__(self, move_vectors, revolve, expand, challenge_vectors = None):
        self.__move_vectors = move_vectors
        if revolve:
            self.__move_vectors = self.__revolve_vectors(self.__move_vectors)
        self.__challenge_vectors = challenge_vectors
        self.__expand = expand

    def __revolve_vectors(self, vectors):
        revolved = []
        for v in vectors:
            revolved.append(v)
            for _ in range(3):
                i, j = revolved[-1]
                revolved.append((j, -i))
        return tuple(revolved)

    def __inbounds(self, board_size, cell):
        if isinstance(cell, tuple):
            return all(map(lambda x: self.__inbounds(board_size, x), cell))
        return 0 <= cell < board_size

    def get_move_and_challenge_cells(self, board, cell):
        moves = []
        challenges = []
        board_size = board.get_size()

        def v_add(x, y):
            return (x[0] + y[0], x[1] + y[1])
        def check_and_add_cell(c, challenge = False):
            if not self.__inbounds(board_size, c):
                return False
            if challenge or self.__challenge_vectors is None:
                challenges.append(c)
            if board.cell_at(*c).has_piece():
                return False
            if not challenge:
                moves.append(c)
            return self.__expand

        for v in self.__move_vectors:
            c = v_add(cell, v)
            while check_and_add_cell(c):
                c = v_add(c, v)

        if self.__challenge_vectors is None:
            return (moves, challenges)

        for v in self.__challenge_vectors:
            c = v_add(cell, v)
            while check_and_add_cell(c, True):
                c = v_add(c, v)
        return (moves, challenges)

class Logic(Singleton):

    def __init__(self):
        super().__init__()
        self.__data = {}
        self.__data[PieceType.QUEEN] = PieceData(((1, 0), (1, 1)), True, True)
        self.__data[PieceType.KING] = PieceData(((1, 0), (1, 1)), True, False)
        self.__data[PieceType.BISHOP] = PieceData(((1, 1),), True, True)
        self.__data[PieceType.ROOK] = PieceData(((1, 0),), True, True)
        self.__data[PieceType.KNIGHT] = PieceData(((2, 1), (2, -1)), True, False)
        self.__data[PieceType.PAWN] = PieceData(
            ((-1, 0),), False, False, ((-1, -1), (-1, 1)))
        if not all(map(lambda p: p in self.__data.keys(), enum_as_list(PieceType))):
            raise SystemExit("Not all piece types are categorised.")

    def get_move_and_challenge_cells(self, board, cell, piece):
        return self.__data[piece].get_move_and_challenge_cells(board, cell)

class Board():

    def __init__(self, colour = BoardColour.BLACK_WHITE, scale = 3):
        self.__spritesheet = instance(Spritesheet).get_sheet(scale)
        self.__colour = colour
        self.__scale = scale

        self.__pressed = None
        self.__selected = None

        self.__load_default_layout()
        self.__drop_board()

    def __calculate_offsets(self):
        def get_offset(x): return (x - Spritesheet.BOARD_WIDTH * self.__scale * self.__size) / 2
        self.__x_offset, self.__y_offset = map(get_offset, instance(Globals).get_window_size())
    def __get_cell_type(self, i, j):
        return self.__cell_types[(i + j) % len(self.__cell_types)]
    def __fill_board(self):
        self.__board = []
        self.__calculate_offsets()
        for i in range(self.__size):
            row = []
            for j in range(self.__size):
                row.append(BoardCell(self.__spritesheet, (i, j),
                                     self.__get_cell_position(i, j), self.__colour,
                                     self.__get_cell_type(i, j), self.__scale))
            self.__board.append(row)
    def __load_default_layout(self):
        self.__size = 8
        self.__cell_types = (BoardType.LIGHT, BoardType.DARK)
        self.__fill_board()

        colours = (PieceColour.BLACK, PieceColour.WHITE)
        def colour(i): return colours[0 if i < self.__size / 2 else 1]

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
                    self.__board[i][j].set_piece_colour_and_type(
                        colour(i), _type)

        pawn_rows = (1, self.__size - 2)
        for i in pawn_rows:
            for j in range(self.__size):
                self.__board[i][j].set_piece_colour_and_type(
                    colour(i), PieceType.PAWN)
    def __drop_board(self):
        drop_duration = 750
        delta_duration = 100
        piece_pause = 500
        self.__inactive_timer = Timer(drop_duration
                                      + piece_pause
                                      + 2 * (self.__size - 1) * delta_duration)
        for i in range(self.__size):
            for j in range(self.__size):
                cell = self.cell_at(i, j)
                sx, sy = self.__get_cell_position(i, j)
                delay_factor = self.__size - 1 - i + j
                cell.set_position((sx, sy))
                cell.move_piece(
                    (sx, -Spritesheet.PIECE_HEIGHT * self.__scale),
                    cell.get_bottom_left(),
                    drop_duration,
                    delay_factor * delta_duration + piece_pause)
                cell.tween_position(Tween(TweenType.EASE_OUT_EXPO,
                                          (sx, -Spritesheet.BOARD_HEIGHT * self.__scale),
                                          (sx, sy),
                                          drop_duration,
                                          delay_factor * delta_duration))

    def cell_at(self, i, j):
        return self.__board[i][j]
    def __get_cell_position(self, i, j):
        return (self.__x_offset + j * Spritesheet.BOARD_WIDTH * self.__scale,
                self.__y_offset + i * Spritesheet.BOARD_WIDTH * self.__scale)

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
            elif self.cell_at(*gxy).has_piece():
                if self.__selected is not None:
                    self.cell_at(*self.__selected).unselect()
                self.__selected = gxy
                self.cell_at(*gxy).select()
            elif self.__selected is not None:
                self.cell_at(*self.__selected).transfer_to(self.cell_at(*gxy))
                self.__selected = None
        elif self.__selected is not None:
            self.cell_at(*self.__selected).unselect()
            self.__selected = None
        if self.__selected is not None:
            moves, challenges = self.__get_moves_and_challenges(self.__selected)
            for i in range(self.__size):
                for j in range(self.__size):
                    cell = self.cell_at(i, j)
                    if (i, j) in moves:
                        cell.set_temporary_type(BoardType.MOVE)
                    elif (i, j) in challenges:
                        cell.set_temporary_type(BoardType.DANGER)
                    else:
                        cell.fallback_type()

    def __get_moves_and_challenges(self, gxy):
        cell = self.cell_at(*gxy)
        if cell.has_piece():
            _type = cell.get_piece().get_type()
            return instance(Logic).get_move_and_challenge_cells(self, gxy, _type)

    def get_size(self): return self.__size
