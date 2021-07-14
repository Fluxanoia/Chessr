from src.utils.groups import FluxSprite, GroupType
from src.utils.files import FileManager
from src.game.logic import Logic, SimpleBoard
from src.game.enums import BoardType, PieceColour, Side
from src.game.elements import BoardCell
from src.utils.globals import Globals, instance
from src.utils.spritesheet import Spritesheet

class CoordinateText(FluxSprite):

    def __init__(self, text, xy, scale):
        self.group = GroupType.UI
        self.scale = scale
        font = instance(FileManager).load_default_font(8 * scale)
        self.image = font.render(text, True, (255, 255, 255))
        super().__init__(xy)

    def position_transform(self, xy):
        x, y = xy
        w, h = self.rect.size
        return (x - w / 2, y - h / 2)

class Controller:

    MOVE_KEY = "move"
    CHALLENGE_KEY = "challenge"
    SPECIAL_KEY = "special"

    def __init__(self, board):
        self.__board = board
        self.__selected = None

        self.__moves = tuple()

    def __get_cell_type(self, i, j):
        cell_colours = (BoardType.LIGHT, BoardType.DARK)
        return cell_colours[(i + j) % len(cell_colours)]
    def __get_cell_size(self):
        return Spritesheet.BOARD_WIDTH * self.__board.get_cell_scale()
    def __get_cell_position(self, i, j):
        cell_size = self.__get_cell_size()
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
        self.__texts = []
        scale = self.__board.get_cell_scale()
        cell_size = self.__get_cell_size()
        left = self.__x_offset
        bottom = self.__y_offset + self.__height * cell_size
        buffer = int(3 * cell_size / 4)
        for i in range(self.__height):
            pos = (left - buffer, self.__y_offset + (i + 0.5) * cell_size)
            self.__texts.append(CoordinateText(str(i + 1), pos, scale))
        for j in range(self.__width):
            pos = (left + (j + 0.5) * cell_size, bottom + buffer)
            self.__texts.append(CoordinateText(chr(ord('A') + j), pos, scale))

    def start(self):
        self.__width, self.__height = 0, 0

        def side(c):
            if c == 'w':
                return Side.FRONT
            if c == 'b':
                return Side.BACK
            raise Exception("Incorrect board format.")

        data = {}
        logic = instance(Logic)
        for key, value in instance(FileManager).load_board("default.board").items():
            if key == "w":
                self.__width = int(value)
            elif key == "h":
                self.__height = int(value)
            elif len(key) == 2:
                def get_coord(c):
                    return logic.get_coordinate(c, self.__height)
                coords = tuple(map(get_coord, value.split(' ')))
                data[(side(key[0]), logic.get_piece(key[1]))] = coords

        sw, sh = instance(Globals).get_window_size()
        cell_size = Spritesheet.BOARD_WIDTH * self.__board.get_cell_scale()
        self.__x_offset = (sw - cell_size * self.__width) / 2
        self.__y_offset = (sh - cell_size * self.__height) / 2

        self.reset_board()

        def colour(side):
            return (PieceColour.BLACK, PieceColour.WHITE)[int(side == Side.FRONT)]
        for key, values in data.items():
            s, p = key
            for (i, j) in values:
                self.__cells[i][j].place_piece(colour(s), p, s)

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
