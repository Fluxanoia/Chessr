#include "pch.h"
#include "test_helpers.hpp"

#include "../Chessr.Backend/flag_board.hpp"

TEST(FlagBoardTests, TestConstructor)
{
	FlagBoard empty_board = { { 2, 4 }, false };
	FlagBoard full_board = { { 7, 4 }, true };

	EXPECT_EQ(empty_board.get_flagged().size(), 0);
	EXPECT_EQ(full_board.get_flagged().size(), 28);
}

TEST(FlagBoardTests, TestFlagging)
{
	FlagBoard board = { { 5, 5 } };

	std::vector<Coordinate> flagged;
	std::vector<Coordinate> to_flag = {
		{ 0, 0 },
		{ 1, 1 },
		{ 2, 2 },
		{ 3, 3 },
		{ 4, 4 }
	};

	board.flag(to_flag);
	board.flag(Coordinate{ 0, 4 });
	board.flag(std::optional<Coordinate>{});
	flagged = board.get_flagged();

	EXPECT_EQ(flagged.size(), 6);
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(0, 0)) != flagged.end());
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(1, 1)) != flagged.end());
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(2, 2)) != flagged.end());
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(3, 3)) != flagged.end());
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(4, 4)) != flagged.end());
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(0, 4)) != flagged.end());

	board.unflag(Coordinate{ 0, 4 });
	board.unflag(Coordinate{ 2, 2 });
	flagged = board.get_flagged();
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(0, 0)) != flagged.end());
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(1, 1)) != flagged.end());
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(3, 3)) != flagged.end());
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(4, 4)) != flagged.end());

	EXPECT_EQ(flagged.size(), 4);

	board.unflag(to_flag);
	flagged = board.get_flagged();

	EXPECT_EQ(flagged.size(), 0);
}

TEST(FlagBoardTests, TestSetAll)
{
	FlagBoard board = { { 2, 4 }, false };

	EXPECT_EQ(board.get_flagged().size(), 0);

	board.set_all(false);

	EXPECT_EQ(board.get_flagged().size(), 0);

	board.set_all(true);

	EXPECT_EQ(board.get_flagged().size(), 8);

	board.set_all(false);

	EXPECT_EQ(board.get_flagged().size(), 0);
}

TEST(FlagBoardTests, TestRestricting)
{
	FlagBoard board = { { 5, 5 }, true };

	std::vector<Coordinate> flagged;
	std::vector<Coordinate> to_restrict;

	flagged = board.get_flagged();

	EXPECT_EQ(flagged.size(), 25);

	to_restrict = {
		{ 0, 0 },
		{ 1, 1 },
		{ 2, 2 },
		{ 3, 3 },
		{ 4, 4 }
	};

	board.restrict(to_restrict);
	flagged = board.get_flagged();

	EXPECT_EQ(flagged.size(), 5);
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(0, 0)) != flagged.end());
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(1, 1)) != flagged.end());
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(2, 2)) != flagged.end());
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(3, 3)) != flagged.end());
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(4, 4)) != flagged.end());

	to_restrict = {
		{ 2, 0 },
		{ 2, 1 },
		{ 2, 2 },
		{ 2, 3 },
		{ 2, 4 }
	};

	board.restrict(to_restrict);
	flagged = board.get_flagged();

	EXPECT_EQ(flagged.size(), 1);
	EXPECT_TRUE(std::find(flagged.begin(), flagged.end(), Coordinate(2, 2)) != flagged.end());

	to_restrict = {
		{ 1, 0 },
		{ 1, 1 },
		{ 1, 2 },
		{ 1, 3 },
		{ 1, 4 }
	};

	board.restrict(to_restrict);
	flagged = board.get_flagged();

	EXPECT_EQ(flagged.size(), 0);
}

TEST(FlagBoardTests, TestMasking)
{
	FlagBoard board = { { 5, 5 }, true };

	auto consequence_1 = std::make_shared<MoveConsequence>(
		MoveType::PUSH, MoveStyle::JUMP, Coordinate{ 0, 0 }, Coordinate{ 0, 0 }, Coordinate{ 0, 0 });
	auto consequence_2 = std::make_shared<MoveConsequence>(
		MoveType::PUSH, MoveStyle::JUMP, Coordinate{ 0, 0 }, Coordinate{ 0, 0 }, Coordinate{ 1, 1 });
	auto consequence_3 = std::make_shared<MoveConsequence>(
		MoveType::PUSH, MoveStyle::JUMP, Coordinate{ 0, 0 }, Coordinate{ 0, 0 }, Coordinate{ 2, 2 });
	auto consequence_4 = std::make_shared<MoveConsequence>(
		MoveType::PUSH, MoveStyle::JUMP, Coordinate{ 0, 0 }, Coordinate{ 0, 0 }, Coordinate{ 3, 3 });
	auto consequence_5 = std::make_shared<MoveConsequence>(
		MoveType::PUSH, MoveStyle::JUMP, Coordinate{ 0, 0 }, Coordinate{ 0, 0 }, Coordinate{ 4, 4 });

	std::vector<std::shared_ptr<Move>> moves = {
		std::make_shared<Move>(std::vector<std::shared_ptr<Consequence>>{ consequence_1 }),
		std::make_shared<Move>(std::vector<std::shared_ptr<Consequence>>{ consequence_2 }),
		std::make_shared<Move>(std::vector<std::shared_ptr<Consequence>>{ consequence_3 }),
		std::make_shared<Move>(std::vector<std::shared_ptr<Consequence>>{ consequence_4 }),
		std::make_shared<Move>(std::vector<std::shared_ptr<Consequence>>{ consequence_5 }),
	};

	board.mask(moves);

	EXPECT_EQ(moves.size(), 5);
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(0, 0), Coordinate(0, 0)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(0, 0), Coordinate(1, 1)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(0, 0), Coordinate(2, 2)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(0, 0), Coordinate(3, 3)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(0, 0), Coordinate(4, 4)));

	board.set_all(false);
	board.flag(Coordinate{ 0, 0 });
	board.flag(Coordinate{ 1, 1 });
	board.flag(Coordinate{ 2, 2 });

	board.mask(moves);

	EXPECT_EQ(moves.size(), 3);
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(0, 0), Coordinate(0, 0)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(0, 0), Coordinate(1, 1)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(0, 0), Coordinate(2, 2)));

	board.set_all(false);
	board.flag(Coordinate{ 0, 0 });
	board.flag(Coordinate{ 0, 1 });
	board.flag(Coordinate{ 0, 2 });

	board.mask(moves);

	EXPECT_EQ(moves.size(), 1);
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(0, 0), Coordinate(0, 0)));

	board.set_all(false);
	board.mask(moves);

	EXPECT_EQ(moves.size(), 0);
}
