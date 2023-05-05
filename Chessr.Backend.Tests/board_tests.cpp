#include "pch.h"

#include "../Chessr.Backend/board.hpp"

TEST(BoardTests, TestConstructor)
{
	Board board_1 = { {
		{ {}, {}, {} },
		{ {}, {}, {} }
	} };
	Board board_2 = { {} };
	Board board_3 = { { 
		{ {}, {} }
	} };
	Board board_4 = { {
		{ {}, {}, {} },
		{ {}, {}, {} },
		{ {}, {}, {} },
		{ {}, {}, {} }
	} };

	EXPECT_EQ(board_1.get_dimensions(), Coordinate(3, 2));
	EXPECT_EQ(board_2.get_dimensions(), Coordinate(0, 0));
	EXPECT_EQ(board_3.get_dimensions(), Coordinate(2, 1));
	EXPECT_EQ(board_4.get_dimensions(), Coordinate(3, 4));
}

TEST(BoardTests, TestConstructor_Throws)
{
	Grid<Piece> grid = { {
		{ {}, {}, {} },
		{ {}, {} }
	} };

	EXPECT_THROW(Board{ grid }, InvalidBoardException);
}

TEST(BoardTests, TestIsInCheck)
{
	Board board = { {} };

	EXPECT_FALSE(board.is_in_check());

	board.set_in_check();

	EXPECT_TRUE(board.is_in_check());
}

TEST(BoardTests, TestHasAndGetPiece)
{
	Piece p1 = { PieceType::PAWN, Player::WHITE };
	Piece p2 = { PieceType::PAWN, Player::BLACK };
	Piece p3 = { PieceType::QUEEN, Player::WHITE };
	Board board = { {
		{ p1, {}, {} },
		{ {}, {}, p2 },
		{ {}, {}, {} },
		{ {}, p3, {} }
	} };

	EXPECT_TRUE(board.has_piece({ 0, 0 }));
	EXPECT_TRUE(board.has_piece({ 1, 2 }));
	EXPECT_TRUE(board.has_piece({ 3, 1 }));

	EXPECT_FALSE(board.has_piece({ 0, 1 }));
	EXPECT_FALSE(board.has_piece({ 1, 1 }));
	EXPECT_FALSE(board.has_piece({ 2, 2 }));

	EXPECT_EQ(board.get_piece({ 0, 0 }).get_type(), PieceType::PAWN);
	EXPECT_EQ(board.get_piece({ 1, 2 }).get_type(), PieceType::PAWN);
	EXPECT_EQ(board.get_piece({ 3, 1 }).get_type(), PieceType::QUEEN);

	EXPECT_EQ(board.get_piece({ 0, 0 }).get_player(), Player::WHITE);
	EXPECT_EQ(board.get_piece({ 1, 2 }).get_player(), Player::BLACK);
	EXPECT_EQ(board.get_piece({ 3, 1 }).get_player(), Player::WHITE);
}

TEST(BoardTests, TestRankContainsMultipleOf)
{
	Piece wp = { PieceType::PAWN, Player::WHITE };
	Piece bp = { PieceType::PAWN, Player::BLACK };
	Piece wq = { PieceType::QUEEN, Player::WHITE };
	Board board = { {
		{ wp, wq, {}, {}, bp },
		{ {}, wp, {}, wp, bp },
		{ {}, {}, {}, {}, {} },
		{ wp, wq, bp, {}, bp },
		{ {}, wp, wp, {}, {} }
	} };

	EXPECT_FALSE(board.rank_contains_multiple_of(0, PieceType::PAWN, Player::WHITE));
	EXPECT_TRUE (board.rank_contains_multiple_of(1, PieceType::PAWN, Player::WHITE));
	EXPECT_FALSE(board.rank_contains_multiple_of(2, PieceType::PAWN, Player::WHITE));
	EXPECT_FALSE(board.rank_contains_multiple_of(3, PieceType::PAWN, Player::WHITE));
	EXPECT_TRUE (board.rank_contains_multiple_of(4, PieceType::PAWN, Player::WHITE));

	EXPECT_FALSE(board.rank_contains_multiple_of(0, PieceType::PAWN, Player::BLACK));
	EXPECT_FALSE(board.rank_contains_multiple_of(1, PieceType::PAWN, Player::BLACK));
	EXPECT_FALSE(board.rank_contains_multiple_of(2, PieceType::PAWN, Player::BLACK));
	EXPECT_TRUE (board.rank_contains_multiple_of(3, PieceType::PAWN, Player::BLACK));
	EXPECT_FALSE(board.rank_contains_multiple_of(4, PieceType::PAWN, Player::BLACK));

	EXPECT_FALSE(board.rank_contains_multiple_of(0, PieceType::QUEEN, Player::WHITE));
	EXPECT_FALSE(board.rank_contains_multiple_of(1, PieceType::QUEEN, Player::WHITE));
	EXPECT_FALSE(board.rank_contains_multiple_of(2, PieceType::QUEEN, Player::WHITE));
	EXPECT_FALSE(board.rank_contains_multiple_of(3, PieceType::QUEEN, Player::WHITE));
	EXPECT_FALSE(board.rank_contains_multiple_of(4, PieceType::QUEEN, Player::WHITE));

	EXPECT_FALSE(board.rank_contains_multiple_of(0, PieceType::QUEEN, Player::BLACK));
	EXPECT_FALSE(board.rank_contains_multiple_of(1, PieceType::QUEEN, Player::BLACK));
	EXPECT_FALSE(board.rank_contains_multiple_of(2, PieceType::QUEEN, Player::BLACK));
	EXPECT_FALSE(board.rank_contains_multiple_of(3, PieceType::QUEEN, Player::BLACK));
	EXPECT_FALSE(board.rank_contains_multiple_of(4, PieceType::QUEEN, Player::BLACK));
}

TEST(BoardTests, TestFileContainsMultipleOf)
{
	Piece wp = { PieceType::PAWN, Player::WHITE };
	Piece bp = { PieceType::PAWN, Player::BLACK };
	Piece wq = { PieceType::QUEEN, Player::WHITE };
	Board board = { {
		{ wp, wq, {}, {}, bp },
		{ {}, wp, {}, wp, bp },
		{ {}, {}, {}, {}, {} },
		{ wp, wq, bp, {}, bp },
		{ {}, wp, wp, {}, {} }
	} };

	EXPECT_TRUE (board.file_contains_multiple_of(0, PieceType::PAWN, Player::WHITE));
	EXPECT_TRUE (board.file_contains_multiple_of(1, PieceType::PAWN, Player::WHITE));
	EXPECT_FALSE(board.file_contains_multiple_of(2, PieceType::PAWN, Player::WHITE));
	EXPECT_FALSE(board.file_contains_multiple_of(3, PieceType::PAWN, Player::WHITE));
	EXPECT_FALSE(board.file_contains_multiple_of(4, PieceType::PAWN, Player::WHITE));

	EXPECT_FALSE(board.file_contains_multiple_of(0, PieceType::PAWN, Player::BLACK));
	EXPECT_FALSE(board.file_contains_multiple_of(1, PieceType::PAWN, Player::BLACK));
	EXPECT_FALSE(board.file_contains_multiple_of(2, PieceType::PAWN, Player::BLACK));
	EXPECT_FALSE(board.file_contains_multiple_of(3, PieceType::PAWN, Player::BLACK));
	EXPECT_TRUE (board.file_contains_multiple_of(4, PieceType::PAWN, Player::BLACK));

	EXPECT_FALSE(board.file_contains_multiple_of(0, PieceType::QUEEN, Player::WHITE));
	EXPECT_TRUE (board.file_contains_multiple_of(1, PieceType::QUEEN, Player::WHITE));
	EXPECT_FALSE(board.file_contains_multiple_of(2, PieceType::QUEEN, Player::WHITE));
	EXPECT_FALSE(board.file_contains_multiple_of(3, PieceType::QUEEN, Player::WHITE));
	EXPECT_FALSE(board.file_contains_multiple_of(4, PieceType::QUEEN, Player::WHITE));

	EXPECT_FALSE(board.file_contains_multiple_of(0, PieceType::QUEEN, Player::BLACK));
	EXPECT_FALSE(board.file_contains_multiple_of(1, PieceType::QUEEN, Player::BLACK));
	EXPECT_FALSE(board.file_contains_multiple_of(2, PieceType::QUEEN, Player::BLACK));
	EXPECT_FALSE(board.file_contains_multiple_of(3, PieceType::QUEEN, Player::BLACK));
	EXPECT_FALSE(board.file_contains_multiple_of(4, PieceType::QUEEN, Player::BLACK));
}

TEST(BoardTests, TestPositionsOf)
{
	Piece wp = { PieceType::PAWN, Player::WHITE };
	Piece bp = { PieceType::PAWN, Player::BLACK };
	Piece wq = { PieceType::QUEEN, Player::WHITE };
	Board board = { {
		{ wp, wq, {}, {}, bp },
		{ {}, wp, {}, wp, bp },
		{ {}, {}, {}, {}, {} },
		{ wp, wq, bp, {}, bp },
		{ {}, wp, wp, {}, {} }
	} };

	auto wp_positions = board.positions_of(PieceType::PAWN, Player::WHITE);
	auto bp_positions = board.positions_of(PieceType::PAWN, Player::BLACK);
	auto wq_positions = board.positions_of(PieceType::QUEEN, Player::WHITE);
	auto bq_positions = board.positions_of(PieceType::QUEEN, Player::BLACK);

	EXPECT_EQ(wp_positions.size(), 6);
	EXPECT_EQ(bp_positions.size(), 4);
	EXPECT_EQ(wq_positions.size(), 2);
	EXPECT_EQ(bq_positions.size(), 0);

	EXPECT_TRUE(std::find(wp_positions.begin(), wp_positions.end(), Coordinate(0, 0)) != wp_positions.end());
	EXPECT_TRUE(std::find(wp_positions.begin(), wp_positions.end(), Coordinate(1, 1)) != wp_positions.end());
	EXPECT_TRUE(std::find(wp_positions.begin(), wp_positions.end(), Coordinate(1, 3)) != wp_positions.end());
	EXPECT_TRUE(std::find(wp_positions.begin(), wp_positions.end(), Coordinate(3, 0)) != wp_positions.end());
	EXPECT_TRUE(std::find(wp_positions.begin(), wp_positions.end(), Coordinate(4, 1)) != wp_positions.end());
	EXPECT_TRUE(std::find(wp_positions.begin(), wp_positions.end(), Coordinate(4, 2)) != wp_positions.end());

	EXPECT_TRUE(std::find(bp_positions.begin(), bp_positions.end(), Coordinate(0, 4)) != bp_positions.end());
	EXPECT_TRUE(std::find(bp_positions.begin(), bp_positions.end(), Coordinate(1, 4)) != bp_positions.end());
	EXPECT_TRUE(std::find(bp_positions.begin(), bp_positions.end(), Coordinate(3, 4)) != bp_positions.end());
	EXPECT_TRUE(std::find(bp_positions.begin(), bp_positions.end(), Coordinate(3, 2)) != bp_positions.end());

	EXPECT_TRUE(std::find(wq_positions.begin(), wq_positions.end(), Coordinate(0, 1)) != wq_positions.end());
	EXPECT_TRUE(std::find(wq_positions.begin(), wq_positions.end(), Coordinate(3, 1)) != wq_positions.end());
}
