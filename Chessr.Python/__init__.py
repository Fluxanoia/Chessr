import os

from src.master import Master

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

from backend import ChessEngine, Piece, PieceType, Player

engine = ChessEngine([
    [
        Piece(PieceType.QUEEN, Player.BLACK),
        None,
        Piece(PieceType.ROOK, Player.BLACK)
    ],
    [
        None,
        Piece(PieceType.KING, Player.BLACK),
        None
    ],
    [None, None, None],
    [
        Piece(PieceType.KNIGHT, Player.WHITE),
        Piece(PieceType.QUEEN, Player.WHITE),
        None
    ]
])

x = print(engine.process(Player.BLACK)[0][1])

if __name__ == '__main__':
    Master()
