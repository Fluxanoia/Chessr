from src.game.board import LogicBoard
from src.game.logic.move_data import Move, MoveData, Moves, MoveType
from src.utils.enums import Side
from src.utils.helpers import IntVector, add_vectors


class PieceData:

    def __init__(
        self,
        character : str,
        moves : tuple[MoveData, ...]
    ):
        self.__char = character
        self.__moves = moves

    def get_moves(
        self,
        logic_board : LogicBoard,
        side : Side,
        gxy : IntVector
    ) -> Moves:
        moves : list[Move] = []

        def check_cell(cell : IntVector, move_data : MoveData) -> bool:
            board_cell = logic_board.at(*cell)
            if board_cell is None:
                return False

            is_move = MoveType.MOVE in move_data.types
            is_attack = MoveType.ATTACK in move_data.types

            piece = board_cell.piece
            if piece is None:
                if is_move:
                    moves.append(Move(cell, MoveType.MOVE, True))
                if is_attack:
                    moves.append(Move(cell, MoveType.ATTACK, False))
                return move_data.expand
            else:
                if piece.side == side:
                    return False
                if is_attack:
                    moves.append(Move(cell, MoveType.ATTACK, True))
                return False

        flip = self.flip(side)

        for move_data in self.__moves:
            for vector in move_data.get_vectors(flip):
                cell = add_vectors(gxy, vector)
                while check_cell(cell, move_data):
                    cell = add_vectors(cell, vector)

        return Moves(tuple(moves))

    @staticmethod
    def get_forward_vector(side : Side):
        return (1, 0) if PieceData.flip(side) else (-1, 0)

    @staticmethod
    def flip(side : Side):
        return side == Side.BACK

    @property
    def char(self) -> str:
        return self.__char
