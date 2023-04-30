#include "pch.h"

#include "../Chessr.Backend/data.hpp"

TEST(DataTests, TestPiece)
{
	Piece piece_1 = { PieceType::QUEEN, Player::BLACK };
	Piece piece_2 = { PieceType::ROOK, Player::WHITE };

	EXPECT_EQ(piece_1.get_type(), PieceType::QUEEN);
	EXPECT_EQ(piece_2.get_type(), PieceType::ROOK);
	EXPECT_EQ(piece_1.get_player(), Player::BLACK);
	EXPECT_EQ(piece_2.get_player(), Player::WHITE);
}

TEST(DataTests, TestMove)
{
	Move move_1 = { { 1, 2 }, { 3, 4 } };
	Move move_2 = { { -281, 123 }, { 344, -442 } };

	EXPECT_EQ(move_1.get_from(), Coordinate(1, 2));
	EXPECT_EQ(move_1.get_to(), Coordinate(3, 4));
	EXPECT_EQ(move_2.get_from(), Coordinate(-281, 123));
	EXPECT_EQ(move_2.get_to(), Coordinate(344, -442));
}
