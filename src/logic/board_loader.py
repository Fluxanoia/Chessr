from typing import Optional, cast

from src.engine.factory import Factory
from src.engine.file_manager import PathLike
from src.logic.board_data import BoardData, PieceData
from src.logic.notation import Notation
from src.utils.enums import Side
from src.utils.helpers import IntVector


class BoardLoader:

    def load_board(self, path : PathLike) -> BoardData:
        file_data = Factory.get().file_manager.load_board(path)
        if file_data is None:
            return self.__get_invalid_board(path, 'The file could not be loaded.')
        
        width, height = None, None
        for key, value in file_data.items():
            if key == 'w':
                width = int(value)
            elif key == 'h':
                height = int(value)

        if width is None or height is None or width <= 0 or height <= 0:
            return self.__get_invalid_board(path, 'The board width and/or height was invalid, ' \
                + f'width: \'{width}\', height: \'{height}\'.')

        name = 'MISSING_NAME'
        description = 'MISSING_DESC'
        turn = Side.FRONT
        pieces : list[PieceData] = []

        notation = Notation.get()

        for key, value in file_data.items():
            if key in ('w', 'h'):
                continue
            if key == 'turn':
                parsed_turn = self.__get_side_from_text(value)
                if parsed_turn is None:
                    return self.__get_invalid_board(
                        path,
                        f'The \'turn\' value was invalid: {value}.')
                turn = parsed_turn
            elif key == 'name':
                name = value
            elif key == 'desc':
                description = value
            else:
                if not len(key) == 2:
                    return self.__get_invalid_board(
                        path,
                        f'The piece data was invalid: \'{key}:{value}\'.')

                side = self.__get_side_from_text(key[0])
                piece_type = notation.get_piece_type(key[1])
                coords = list(map(
                    lambda c : notation.get_coordinate_from_notation(c, height),
                    value.split(' ')))

                if side is None or piece_type is None or any(map(lambda x : x is None, coords)):
                    return self.__get_invalid_board(
                        path,
                        f'The piece data was invalid: \'{key}:{value}\'.')

                for gxy in coords:
                    pieces.append(PieceData(piece_type, side, cast(IntVector, gxy)))

        return BoardData(
            True,
            width,
            height,
            turn,
            name,
            description,
            pieces)

#region Private Methods

    def __get_side_from_text(self, c : str) -> Optional[Side]:
        if c == 'w':
            return Side.FRONT
        if c == 'b':
            return Side.BACK
        return None

    def __get_invalid_board(self, path : PathLike, description : str) -> BoardData:
        return BoardData(
            False,
            0,
            0,
            Side.FRONT,
            'INVALID_BOARD',
            f'{description} Path: {path}.',
            [])

#endregion
