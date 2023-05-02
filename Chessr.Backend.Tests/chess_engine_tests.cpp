#include "pch.h"
#include "test_helpers.hpp"

#include "../Chessr.Backend/chess_engine.hpp"

TEST(ChessEngineTests, TestName)
{
	const auto bk = TestHelpers::get_piece(PieceType::KING, Player::BLACK);
	const auto bq = TestHelpers::get_piece(PieceType::QUEEN, Player::BLACK);
	const auto wk = TestHelpers::get_piece(PieceType::KING, Player::WHITE);
	const auto wr = TestHelpers::get_piece(PieceType::ROOK, Player::WHITE);
	auto chess_engine = ChessEngine({
		{ {}, {}, bk, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ bq, {}, wr, {}, {}},
		{ {}, {}, wk, {}, {} },
	});

	auto moves = chess_engine.get_moves(Player::BLACK);
}
