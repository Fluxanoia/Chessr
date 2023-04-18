from src.logic.logic_board import LogicBoard, Move, Moves
from src.logic.move_data import MoveData, MoveType
from src.utils.enums import Side
from src.utils.helpers import IntVector, add_vectors


class PieceMoveCalculator:

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
            
            if piece.side == side:
                return False
            if is_attack:
                moves.append(Move(cell, MoveType.ATTACK, True))
            return False

        flip = self.do_flip(side)

        for move_data in self.__moves:
            for vector in move_data.get_vectors(flip):
                cell = add_vectors(gxy, vector)
                while check_cell(cell, move_data):
                    cell = add_vectors(cell, vector)

        return Moves(tuple(moves))

    @staticmethod
    def get_forward_vector(side : Side):
        return (1, 0) if PieceMoveCalculator.do_flip(side) else (-1, 0)
    
    @staticmethod
    def get_home_row(logic_board : LogicBoard, side : Side):
        return 0 if PieceMoveCalculator.do_flip(side) else logic_board.height - 1
    
    @staticmethod
    def get_away_row(logic_board : LogicBoard, side : Side):
        return 0 if not PieceMoveCalculator.do_flip(side) else logic_board.height - 1

    @staticmethod
    def do_flip(side : Side):
        return side == Side.BACK

    @property
    def char(self) -> str:
        return self.__char
