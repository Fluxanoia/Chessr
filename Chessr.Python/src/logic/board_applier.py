from backend import Player
from src.engine.spritesheets.piece_spritesheet import PieceColour
from src.logic.board_data import BoardData
from src.sprites.board.board import Board


class BoardApplier:

    def apply_board(self, board : Board, board_data : BoardData) -> None:
        board.reset(board_data.width, board_data.height)

        for piece_data in board_data.pieces:
            cell = board.at(*piece_data.gxy)
            if cell is None:
                continue
            cell.add_piece(
                self.__get_piece_colour(piece_data.player), piece_data.type, piece_data.player)

    def __get_piece_colour(self, player : Player) -> PieceColour:
        if player == Player.WHITE:
            return PieceColour.WHITE
        if player == Player.BLACK:
            return PieceColour.BLACK
        raise SystemExit(f'Unexpected player value \'{player}\'.')
