from src.logic.board_data import BoardData
from src.sprites.board.board import Board
from src.sprites.board.board_cell import BoardCell
from src.utils.enums import PieceColour, Side


class BoardApplier:

    def apply_board(self, board : Board, board_data : BoardData) -> None:
        board.reset(board_data.width, board_data.height)

        for piece_data in board_data.pieces:
            cell = board.at(*piece_data.gxy)
            if cell is None:
                continue
            if not isinstance(cell, BoardCell):
                raise SystemExit('Expected display element.')    
            cell.add_piece(
                self.__get_piece_colour(piece_data.side), piece_data.type, piece_data.side)

    def __get_piece_colour(self, side : Side) -> PieceColour:
        if side == Side.FRONT:
            return PieceColour.WHITE
        if side == Side.BACK:
            return PieceColour.BLACK
        raise SystemExit(f'Unexpected side value \'{side}\'.')
