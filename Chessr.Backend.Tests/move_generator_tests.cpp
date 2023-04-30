#include "pch.h"

#include "../Chessr.Backend/move_generator.hpp"

std::optional<Piece> get_piece(PieceType piece_type, Player player)
{
	return Piece{ piece_type, player };
}

TEST(MoveGeneratorTests, TestGetOpposingPlayer)
{
	EXPECT_EQ(MoveGenerator::get_opposing_player(Player::BLACK), Player::WHITE);
	EXPECT_EQ(MoveGenerator::get_opposing_player(Player::WHITE), Player::BLACK);
}

TEST(MoveGeneratorTests, TestGetRay)
{
	auto board = Board({
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, get_piece(PieceType::PAWN, Player::BLACK), {}},
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
	});

	auto ray = MoveGenerator::get_ray(board, Player::WHITE, { 0, 1 }, { 1, 1 }, {}, false);
}
