from src.game.logic import Logic, SimpleBoard
from src.game.enums import BoardType, PieceColour, PieceType, Side
from src.game.sprites import BoardCell
from src.utils.globals import Globals, instance
from src.utils.spritesheet import Spritesheet

class Controller:

    MOVE_KEY = "move"
    CHALLENGE_KEY = "challenge"
    SPECIAL_KEY = "special"

    def __init__(self, board, width = 8, height = 8):
        self.__board = board
        self.__width, self.__height = width, height

        sw, sh = instance(Globals).get_window_size()
        cell_size = Spritesheet.BOARD_WIDTH * self.__board.get_cell_scale()
        self.__x_offset = (sw - cell_size * self.__width) / 2
        self.__y_offset = (sh - cell_size * self.__height) / 2

        self.__selected = None
        self.__moves = tuple()

    def __get_cell_type(self, i, j):
        cell_colours = (BoardType.LIGHT, BoardType.DARK)
        return cell_colours[(i + j) % len(cell_colours)]
    def __get_cell_position(self, i, j):
        cell_size = Spritesheet.BOARD_WIDTH * self.__board.get_cell_scale()
        return (self.__x_offset + j * cell_size, self.__y_offset + i * cell_size)
    def reset_board(self):
        self.__cells = []
        for i in range(self.__height):
            row = []
            for j in range(self.__width):
                row.append(BoardCell((i, j),
                                     self.__get_cell_position(i, j),
                                     self.__board.get_board_colour(),
                                     self.__get_cell_type(i, j),
                                     self.__board.get_cell_scale(),
                                     self.__board.get_scale()))
            self.__cells.append(row)

    def start(self):
        self.reset_board()

        def side(i):
            return Side.BACK if i < self.__height / 2 else Side.FRONT
        def colour(side):
            return (PieceColour.BLACK, PieceColour.WHITE)[int(side == Side.FRONT)]

        base_rows = (0, self.__height - 1)
        base_info = (
            (PieceType.ROOK, (0, self.__width - 1)),
            (PieceType.KNIGHT, (1, self.__width - 2)),
            (PieceType.BISHOP, (2, self.__width - 3)),
            (PieceType.QUEEN, (3,)),
            (PieceType.KING, (self.__width - 4,)),
        )
        for _type, cols in base_info:
            for i in base_rows:
                for j in cols:
                    self.__cells[i][j].place_piece(colour(side(i)), _type, side(i))

        pawn_rows = (1, self.__height - 2)
        for i in pawn_rows:
            for j in range(self.__width):
                self.__cells[i][j].place_piece(colour(side(i)), PieceType.PAWN, side(i))

    def update(self):
        pass

    def click(self, gxy):
        if gxy is not None:
            if gxy == self.__selected:
                pass
            elif self.at(*gxy).has_piece():
                if self.__selected is not None:
                    self.at(*self.__selected).unselect()
                self.__selected = gxy
                self.at(*gxy).select()
            elif self.__selected is not None:
                self.move(self.__selected, gxy)
                self.__selected = None
        elif self.__selected is not None:
            self.at(*self.__selected).unselect()
            self.__selected = None
        self.__update_highlighting()

    def __get_all_moves(self, gxy):
        logic = instance(Logic)
        board = SimpleBoard(self)
        moves, challenges = logic.get_move_and_challenge_cells(board, gxy)
        special = logic.get_special_manoeuvres(board, gxy)
        return {
            Controller.MOVE_KEY : moves,
            Controller.CHALLENGE_KEY : challenges,
            Controller.SPECIAL_KEY : special,
        }
    def __update_highlighting(self):
        if self.__selected is None:
            for i in range(self.__height):
                for j in range(self.__width):
                    self.at(i, j).fallback_type()
        else:
            self.__moves = self.__get_all_moves(self.__selected)
            for i in range(self.__height):
                for j in range(self.__width):
                    cell = self.at(i, j)
                    if (i, j) in self.__moves[Controller.MOVE_KEY]:
                        cell.set_temporary_type(BoardType.MOVE)
                    elif (i, j) in self.__moves[Controller.CHALLENGE_KEY]:
                        cell.set_temporary_type(BoardType.DANGER)
                    elif (i, j) in map(lambda x : x[0], self.__moves[Controller.SPECIAL_KEY]):
                        cell.set_temporary_type(BoardType.DEBUG)
                    else:
                        cell.fallback_type()

    def move(self, a, b):
        if not self.at(*a).has_piece() or a == b:
            return
        self.at(*b).transfer_from(self.at(*a))
        for (xy, callback) in self.__moves[Controller.SPECIAL_KEY]:
            if xy == b:
                callback(a, b, self)
    def remove(self, gxy):
        self.at(*gxy).remove_piece()

    def at(self, i, j):
        return self.__cells[i][j]
    def get_width(self):
        return self.__width
    def get_height(self):
        return self.__height