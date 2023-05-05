#include "pch.h"
#include "test_helpers.hpp"

#include "../Chessr.Backend/chess_engine.hpp"

TEST(ChessEngineTests, Test)
{
	const auto bl = TestHelpers::get_piece(PieceType::PAWN, Player::BLACK);
	const auto wh = TestHelpers::get_piece(PieceType::PAWN, Player::WHITE);

	PieceConfiguration piece_configuration = {};
	Grid<Piece> grid = {
		{ {}, {}, {}, {}, {} },
		{ {}, bl, {}, {}, bl },
		{ {}, {}, {}, {}, {} },
		{ {}, wh, {}, bl, {} },
		{ {}, {}, {}, {}, {} },
	};
	ChessEngine engine = { piece_configuration };
	engine.do_not_release_gil();
	engine.start(grid, Player::WHITE);

	const auto& moves = engine.get_current_moves();

	engine.make_move(moves.front());
}
