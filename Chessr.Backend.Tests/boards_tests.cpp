#include "pch.h"

#include "../Chessr.Backend/boards.hpp"

TEST(BoardsTests, TestApplyMove)
{
	Piece wp = { PieceType::PAWN, Player::WHITE };
	Piece bp = { PieceType::PAWN, Player::BLACK };
	Piece wq = { PieceType::QUEEN, Player::WHITE };
	Grid<Piece> grid = { {
		{ wp, wq, {}, {}, bp },
		{ {}, bp, {}, wp, bp },
		{ {}, {}, {}, {}, {} },
		{ wp, wq, bp, {}, bp },
		{ {}, wp, wp, {}, {} }
	} };

	std::vector<std::shared_ptr<Consequence>> consequences_1 = {
		std::make_shared<RemoveConsequence>(Coordinate{ 1, 1 }),
		std::make_shared<MoveConsequence>(
			MoveType::ATTACK,
			MoveStyle::JUMP,
			Coordinate{ -2, 1 },
			Coordinate{ 3, 0 },
			Coordinate{ 1, 1 }),
	};
	std::vector<std::shared_ptr<Consequence>> consequences_2 = {
		std::make_shared<MoveConsequence>(
			MoveType::PUSH,
			MoveStyle::JUMP,
			Coordinate{ 2, 0 },
			Coordinate{ 0, 4 },
			Coordinate{ 2, 4 }),
		std::make_shared<MoveConsequence>(
			MoveType::PUSH,
			MoveStyle::JUMP,
			Coordinate{ 3, 0 },
			Coordinate{ 1, 4 },
			Coordinate{ 4, 4 }),
		std::make_shared<RemoveConsequence>(Coordinate{ 3, 4 }),
	};

	auto move_1 = std::make_shared<Move>(consequences_1, MoveProperty::PROMOTION);
	auto move_2 = std::make_shared<Move>(consequences_2);

	move_1->set_promotion_type(PieceType::QUEEN);

	Boards boards = { grid, Player::WHITE };

	auto& first_board = boards.get_current_board();

	EXPECT_EQ(boards.get_current_player(), Player::WHITE);

	EXPECT_FALSE(boards.get_last_move().has_value());

	EXPECT_TRUE(first_board.has_piece(Coordinate{ 3, 0 }));
	EXPECT_EQ(first_board.get_piece(Coordinate{ 3, 0 }).get_type(), PieceType::PAWN);
	EXPECT_EQ(first_board.get_piece(Coordinate{ 3, 0 }).get_player(), Player::WHITE);

	EXPECT_TRUE(first_board.has_piece(Coordinate{ 1, 1 }));
	EXPECT_EQ(first_board.get_piece(Coordinate{ 1, 1 }).get_type(), PieceType::PAWN);
	EXPECT_EQ(first_board.get_piece(Coordinate{ 1, 1 }).get_player(), Player::BLACK);

	EXPECT_FALSE(boards.has_moved(Coordinate{ 3, 0 }));
	EXPECT_FALSE(boards.has_moved(Coordinate{ 1, 1 }));

	boards.apply_move(move_1);

	auto& second_board = boards.get_current_board();

	EXPECT_EQ(boards.get_current_player(), Player::BLACK);

	EXPECT_TRUE(boards.get_last_move().has_value());
	EXPECT_EQ(boards.get_last_move().value(), move_1);

	EXPECT_FALSE(second_board.has_piece(Coordinate{ 3, 0 }));

	EXPECT_TRUE(second_board.has_piece(Coordinate{ 1, 1 }));
	EXPECT_EQ(second_board.get_piece(Coordinate{ 1, 1 }).get_type(), PieceType::QUEEN);
	EXPECT_EQ(second_board.get_piece(Coordinate{ 1, 1 }).get_player(), Player::WHITE);

	EXPECT_FALSE(boards.has_moved(Coordinate{ 3, 0 }));
	EXPECT_TRUE(boards.has_moved(Coordinate{ 1, 1 }));

	auto& first_board_again = boards.get_previous_board();

	EXPECT_TRUE(first_board_again.has_piece(Coordinate{ 3, 0 }));
	EXPECT_EQ(first_board_again.get_piece(Coordinate{ 3, 0 }).get_type(), PieceType::PAWN);
	EXPECT_EQ(first_board_again.get_piece(Coordinate{ 3, 0 }).get_player(), Player::WHITE);

	EXPECT_TRUE(first_board_again.has_piece(Coordinate{ 1, 1 }));
	EXPECT_EQ(first_board_again.get_piece(Coordinate{ 1, 1 }).get_type(), PieceType::PAWN);
	EXPECT_EQ(first_board_again.get_piece(Coordinate{ 1, 1 }).get_player(), Player::BLACK);

	EXPECT_TRUE(second_board.has_piece(Coordinate{ 0, 4 }));
	EXPECT_TRUE(second_board.has_piece(Coordinate{ 1, 4 }));
	EXPECT_FALSE(second_board.has_piece(Coordinate{ 2, 4 }));
	EXPECT_TRUE(second_board.has_piece(Coordinate{ 3, 4 }));
	EXPECT_FALSE(second_board.has_piece(Coordinate{ 4, 4 }));

	EXPECT_FALSE(boards.has_moved(Coordinate{ 0, 4 }));
	EXPECT_FALSE(boards.has_moved(Coordinate{ 1, 4 }));
	EXPECT_FALSE(boards.has_moved(Coordinate{ 2, 4 }));
	EXPECT_FALSE(boards.has_moved(Coordinate{ 3, 4 }));
	EXPECT_FALSE(boards.has_moved(Coordinate{ 4, 4 }));

	boards.apply_move(move_2);

	auto& third_board = boards.get_current_board();

	EXPECT_EQ(boards.get_current_player(), Player::WHITE);

	EXPECT_TRUE(boards.get_last_move().has_value());
	EXPECT_EQ(boards.get_last_move().value(), move_2);

	EXPECT_FALSE(third_board.has_piece(Coordinate{ 0, 4 }));
	EXPECT_FALSE(third_board.has_piece(Coordinate{ 1, 4 }));
	EXPECT_TRUE(third_board.has_piece(Coordinate{ 2, 4 }));
	EXPECT_FALSE(third_board.has_piece(Coordinate{ 3, 4 }));
	EXPECT_TRUE(third_board.has_piece(Coordinate{ 4, 4 }));

	EXPECT_EQ(third_board.get_piece(Coordinate{ 2, 4 }).get_type(), PieceType::PAWN);
	EXPECT_EQ(third_board.get_piece(Coordinate{ 2, 4 }).get_player(), Player::BLACK);

	EXPECT_EQ(third_board.get_piece(Coordinate{ 4, 4 }).get_type(), PieceType::PAWN);
	EXPECT_EQ(third_board.get_piece(Coordinate{ 4, 4 }).get_player(), Player::BLACK);

	EXPECT_FALSE(boards.has_moved(Coordinate{ 0, 4 }));
	EXPECT_FALSE(boards.has_moved(Coordinate{ 1, 4 }));
	EXPECT_TRUE(boards.has_moved(Coordinate{ 2, 4 }));
	EXPECT_FALSE(boards.has_moved(Coordinate{ 3, 4 }));
	EXPECT_TRUE(boards.has_moved(Coordinate{ 4, 4 }));
}

TEST(BoardsTests, TestApplyMoveFails_Move_Existence)
{
	Piece wp = { PieceType::PAWN, Player::WHITE };
	Piece bp = { PieceType::PAWN, Player::BLACK };
	Piece wq = { PieceType::QUEEN, Player::WHITE };
	Grid<Piece> grid = { {
		{ wp, wq, {}, {}, bp },
		{ {}, bp, {}, wp, bp },
		{ {}, {}, {}, {}, {} },
		{ wp, wq, bp, {}, bp },
		{ {}, wp, wp, {}, {} }
	} };

	auto move = std::make_shared<Move>(std::vector<std::shared_ptr<Consequence>>{
		std::make_shared<MoveConsequence>(
			MoveType::ATTACK,
			MoveStyle::JUMP,
			Coordinate{ 1, 0 },
			Coordinate{ 0, 2 },
			Coordinate{ 1, 2 }),
	});

	Boards boards = { grid, Player::WHITE };

	EXPECT_THROW(boards.apply_move(move), InvalidOperationException);
}

TEST(BoardsTests, TestApplyMoveFails_Move_Inhabitation)
{
	Piece wp = { PieceType::PAWN, Player::WHITE };
	Piece bp = { PieceType::PAWN, Player::BLACK };
	Piece wq = { PieceType::QUEEN, Player::WHITE };
	Grid<Piece> grid = { {
		{ wp, wq, {}, {}, bp },
		{ {}, bp, {}, wp, bp },
		{ {}, {}, {}, {}, {} },
		{ wp, wq, bp, {}, bp },
		{ {}, wp, wp, {}, {} }
	} };

	auto move = std::make_shared<Move>(std::vector<std::shared_ptr<Consequence>>{
		std::make_shared<MoveConsequence>(
			MoveType::ATTACK,
			MoveStyle::JUMP,
			Coordinate{ 0, 1 },
			Coordinate{ 1, 3 },
			Coordinate{ 1, 4 }),
	});

	Boards boards = { grid, Player::WHITE };

	EXPECT_THROW(boards.apply_move(move), InvalidOperationException);
}

TEST(BoardsTests, TestApplyMoveFails_Remove_Existence)
{
	Piece wp = { PieceType::PAWN, Player::WHITE };
	Piece bp = { PieceType::PAWN, Player::BLACK };
	Piece wq = { PieceType::QUEEN, Player::WHITE };
	Grid<Piece> grid = { {
		{ wp, wq, {}, {}, bp },
		{ {}, bp, {}, wp, bp },
		{ {}, {}, {}, {}, {} },
		{ wp, wq, bp, {}, bp },
		{ {}, wp, wp, {}, {} }
	} };

	auto move = std::make_shared<Move>(std::vector<std::shared_ptr<Consequence>>{
		std::make_shared<RemoveConsequence>(Coordinate{ 0, 2 }),
	});

	Boards boards = { grid, Player::WHITE };

	EXPECT_THROW(boards.apply_move(move), InvalidOperationException);
}

TEST(BoardsTests, TestApplyMoveFails_Change_Existence)
{
	Piece wp = { PieceType::PAWN, Player::WHITE };
	Piece bp = { PieceType::PAWN, Player::BLACK };
	Piece wq = { PieceType::QUEEN, Player::WHITE };
	Grid<Piece> grid = { {
		{ wp, wq, {}, {}, bp },
		{ {}, bp, {}, wp, bp },
		{ {}, {}, {}, {}, {} },
		{ wp, wq, bp, {}, bp },
		{ {}, wp, wp, {}, {} }
	} };

	auto move = std::make_shared<Move>(std::vector<std::shared_ptr<Consequence>>{
		std::make_shared<ChangeConsequence>(Coordinate{ 2, 0 }, PieceType::QUEEN),
	});

	Boards boards = { grid, Player::WHITE };

	EXPECT_THROW(boards.apply_move(move), InvalidOperationException);
}
