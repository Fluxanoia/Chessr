#include "pch.h"
#include "test_helpers.hpp"

#include "../Chessr.Backend/move_generator.hpp"

#pragma region get_king_move_mask

TEST(MoveGeneratorTests, TestGetKingMoveMask1)
{
	const auto bk = TestHelpers::get_piece(PieceType::KING, Player::BLACK);
	const auto wk = TestHelpers::get_piece(PieceType::KING, Player::WHITE);
	const auto wr = TestHelpers::get_piece(PieceType::ROOK, Player::WHITE);
	auto boards = Boards({
		{ {}, {}, bk, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, wr, {} },
		{ {}, {}, wk, {}, {} },
	}, Player::WHITE);

	auto mask = MoveGenerator::get_king_move_mask(boards, Player::BLACK, { 0, 2 });
	auto flagged = mask->get_flagged();

	EXPECT_EQ(flagged.size(), 16);
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(0, 3)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(1, 3)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(2, 3)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(4, 3)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(3, 0)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(3, 1)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(3, 2)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(3, 4)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(4, 1)) != flagged.end());
}

TEST(MoveGeneratorTests, TestGetKingMoveMask2)
{
	const auto bk = TestHelpers::get_piece(PieceType::KING, Player::BLACK);
	const auto wk = TestHelpers::get_piece(PieceType::KING, Player::WHITE);
	const auto wr = TestHelpers::get_piece(PieceType::ROOK, Player::WHITE);
	auto boards = Boards({
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, bk, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, wr, {} },
		{ {}, {}, wk, {}, {} },
	}, Player::WHITE);

	auto mask = MoveGenerator::get_king_move_mask(boards, Player::BLACK, { 1, 3 });
	auto flagged = mask->get_flagged();

	EXPECT_EQ(flagged.size(), 16);
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(0, 3)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(1, 3)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(2, 3)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(4, 3)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(3, 0)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(3, 1)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(3, 2)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(3, 4)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(4, 1)) != flagged.end());
}

TEST(MoveGeneratorTests, TestGetKingMoveMask3)
{
	const auto wk = TestHelpers::get_piece(PieceType::KING, Player::WHITE);
	const auto bk = TestHelpers::get_piece(PieceType::KING, Player::BLACK);
	const auto bb = TestHelpers::get_piece(PieceType::BISHOP, Player::BLACK);
	auto boards = Boards({
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, wk, {}, {} },
		{ {}, {}, {}, bb, {} },
		{ {}, {}, bk, {}, {} },
	}, Player::WHITE);

	auto mask = MoveGenerator::get_king_move_mask(boards, Player::WHITE, { 2, 2 });
	auto flagged = mask->get_flagged();

	EXPECT_EQ(flagged.size(), 16);
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(0, 0)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(1, 1)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(2, 2)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(2, 4)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(4, 4)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(4, 1)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(4, 3)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(3, 1)) != flagged.end());
	EXPECT_FALSE(std::find(flagged.begin(), flagged.end(), Coordinate(3, 2)) != flagged.end());
}

#pragma endregion

#pragma region get_possible_attacks

TEST(MoveGeneratorTests, TestGetPossibleAttacks)
{
	const auto bk = TestHelpers::get_piece(PieceType::KING, Player::BLACK);
	const auto br = TestHelpers::get_piece(PieceType::ROOK, Player::BLACK);
	const auto wk = TestHelpers::get_piece(PieceType::KING, Player::WHITE);
	const auto wr = TestHelpers::get_piece(PieceType::ROOK, Player::WHITE);
	auto boards = Boards({
		{ br, {}, bk, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, wr, {} },
		{ wr, {}, wk, {}, br },
	}, Player::WHITE);

	auto piece_data = TestHelpers::get_piece_data(
		{ { 1, 0 }, { 1, -1 }, { -1, 0 } },
		{ { -2, 2 }, { 0, -2 }, { -2, -2 } },
		{},
		{});
	auto attacks = MoveGenerator::get_possible_attacks(boards, Player::BLACK, piece_data, { 2, 2 }, {});

	EXPECT_EQ(attacks.size(), 6);
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(4, 0)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(3, 2)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(4, 2)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(1, 1)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(1, 2)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(2, 0)) != attacks.end());
}

TEST(MoveGeneratorTests, TestGetPossibleAttacks_Ignoring)
{
	const auto bk = TestHelpers::get_piece(PieceType::KING, Player::BLACK);
	const auto br = TestHelpers::get_piece(PieceType::ROOK, Player::BLACK);
	const auto wk = TestHelpers::get_piece(PieceType::KING, Player::WHITE);
	const auto wr = TestHelpers::get_piece(PieceType::ROOK, Player::WHITE);
	auto boards = Boards({
		{ br, {}, bk, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, wr, {} },
		{ wr, {}, wk, {}, wr },
	}, Player::WHITE);

	auto piece_data = TestHelpers::get_piece_data(
		{ { 1, 0 }, { 1, -1 }, { -1, 0 }, { -1, 1 } },
		{ { 0, -2 }, { -2, -2 } },
		{},
		{});
	auto attacks = MoveGenerator::get_possible_attacks(boards, Player::BLACK, piece_data, { 2, 2 }, Coordinate{ 3, 3 });

	EXPECT_EQ(attacks.size(), 8);
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(4, 0)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(3, 2)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(4, 2)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(1, 1)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(1, 2)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(2, 0)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(3, 3)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(4, 4)) != attacks.end());
}

#pragma endregion

#pragma region get_attacking_coordinates

TEST(MoveGeneratorTests, TestGetAttackingCoordinates)
{
	const auto ro = TestHelpers::get_piece(PieceType::ROOK, Player::WHITE);
	const auto bi = TestHelpers::get_piece(PieceType::BISHOP, Player::WHITE);
	const auto kn = TestHelpers::get_piece(PieceType::KNIGHT, Player::WHITE);
	const auto pa = TestHelpers::get_piece(PieceType::PAWN, Player::WHITE);
	const auto qu = TestHelpers::get_piece(PieceType::QUEEN, Player::WHITE);
	auto boards = Boards({
		{ {}, {}, {}, {}, bi },
		{ kn, {}, {}, {}, bi},
		{ ro, {}, {}, {}, {} },
		{ {}, {}, pa, pa, {} },
		{ qu, {}, ro, {}, {} },
	}, Player::WHITE);

	auto attacks = MoveGenerator::get_attacking_coordinates(boards, Player::BLACK, { 2, 2 });

	EXPECT_EQ(attacks.size(), 5);
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(3, 3)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(4, 0)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(2, 0)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(1, 0)) != attacks.end());
	EXPECT_TRUE(std::find(attacks.begin(), attacks.end(), Coordinate(0, 4)) != attacks.end());
}

#pragma endregion

#pragma region get_blocks_to_attack

TEST(MoveGeneratorTests, TestGetBlocksToAttack)
{
	auto boards = Boards({
		{ {}, {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {}, {} }
	}, Player::WHITE);

	auto piece_data = TestHelpers::get_piece_data(
		{ { 1, 1 }, { 0, 1 } },
		{},
		{},
		{});
	auto blocks_1 = MoveGenerator::get_blocks_to_attack(boards, Player::WHITE, piece_data, { 1, 1 }, { 4, 4 });
	auto blocks_2 = MoveGenerator::get_blocks_to_attack(boards, Player::WHITE, piece_data, { 1, 1 }, { 1, 5 });

	EXPECT_EQ(blocks_1.size(), 2);
	EXPECT_TRUE(std::find(blocks_1.begin(), blocks_1.end(), Coordinate(2, 2)) != blocks_1.end());
	EXPECT_TRUE(std::find(blocks_1.begin(), blocks_1.end(), Coordinate(3, 3)) != blocks_1.end());

	EXPECT_EQ(blocks_2.size(), 3);
	EXPECT_TRUE(std::find(blocks_2.begin(), blocks_2.end(), Coordinate(1, 2)) != blocks_2.end());
	EXPECT_TRUE(std::find(blocks_2.begin(), blocks_2.end(), Coordinate(1, 3)) != blocks_2.end());
	EXPECT_TRUE(std::find(blocks_2.begin(), blocks_2.end(), Coordinate(1, 4)) != blocks_2.end());
}

TEST(MoveGeneratorTests, TestGetBlocksToAttack_Jump)
{
	auto boards = Boards({
		{ {}, {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {}, {} }
	}, Player::WHITE);

	auto piece_data = TestHelpers::get_piece_data(
		{ { 1, 1 } },
		{ { 3, 3 } },
		{},
		{});
	auto blocks = MoveGenerator::get_blocks_to_attack(boards, Player::WHITE, piece_data, { 1, 1 }, { 4, 4 });

	EXPECT_EQ(blocks.size(), 0);
}

TEST(MoveGeneratorTests, TestGetBlocksToAttack_Invalid)
{
	auto boards = Boards({
		{ {}, {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {}, {} }
	}, Player::WHITE);

	auto piece_data = TestHelpers::get_piece_data(
		{ { 1, 1 }, { 0, 1 } },
		{},
		{},
		{});

	EXPECT_THROW(
		MoveGenerator::get_blocks_to_attack(boards, Player::BLACK, piece_data, { 1, 1 }, { 4, 4 }),
		InvalidOperationException);
}

#pragma endregion

#pragma region get_pins

TEST(MoveGeneratorTests, TestGetPins)
{
	const auto wk = TestHelpers::get_piece(PieceType::KING, Player::WHITE);
	const auto wp = TestHelpers::get_piece(PieceType::PAWN, Player::WHITE);

	const auto br = TestHelpers::get_piece(PieceType::ROOK, Player::BLACK);
	const auto bb = TestHelpers::get_piece(PieceType::BISHOP, Player::BLACK);
	const auto bq = TestHelpers::get_piece(PieceType::QUEEN, Player::BLACK);
	auto boards = Boards({
		{ {}, {}, {}, wp, {}, {} },
		{ {}, {}, {}, br, {}, {} },
		{ {}, {}, {}, wp, {}, bb },
		{ {}, {}, {}, {}, wp, {} },
		{ bq, wp, {}, wk, {}, br },
		{ {}, {}, {}, {}, {}, {} }
	}, Player::WHITE);
	
	auto pins = MoveGenerator::get_pins(boards, Player::WHITE);

	EXPECT_EQ(pins.size(), 3);

	auto pin_1 = std::find_if(pins.begin(), pins.end(), [](const PinnedPiece& pin) { return pin.get_coordinate() == Coordinate(4, 1); });
	auto pin_2 = std::find_if(pins.begin(), pins.end(), [](const PinnedPiece& pin) { return pin.get_coordinate() == Coordinate(2, 3); });
	auto pin_3 = std::find_if(pins.begin(), pins.end(), [](const PinnedPiece& pin) { return pin.get_coordinate() == Coordinate(3, 4); });

	EXPECT_FALSE(pin_1 == pins.end());
	EXPECT_FALSE(pin_2 == pins.end());
	EXPECT_FALSE(pin_3 == pins.end());

	auto flags_1 = pin_1->get_move_mask()->get_flagged();
	auto flags_2 = pin_2->get_move_mask()->get_flagged();
	auto flags_3 = pin_3->get_move_mask()->get_flagged();

	EXPECT_EQ(flags_1.size(), 3);
	EXPECT_EQ(flags_2.size(), 3);
	EXPECT_EQ(flags_3.size(), 2);

	EXPECT_TRUE(std::find(flags_1.begin(), flags_1.end(), Coordinate(4, 0)) != flags_1.end());
	EXPECT_TRUE(std::find(flags_1.begin(), flags_1.end(), Coordinate(4, 1)) != flags_1.end());
	EXPECT_TRUE(std::find(flags_1.begin(), flags_1.end(), Coordinate(4, 2)) != flags_1.end());

	EXPECT_TRUE(std::find(flags_2.begin(), flags_2.end(), Coordinate(1, 3)) != flags_2.end());
	EXPECT_TRUE(std::find(flags_2.begin(), flags_2.end(), Coordinate(2, 3)) != flags_2.end());
	EXPECT_TRUE(std::find(flags_2.begin(), flags_2.end(), Coordinate(3, 3)) != flags_2.end());

	EXPECT_TRUE(std::find(flags_3.begin(), flags_3.end(), Coordinate(3, 4)) != flags_3.end());
	EXPECT_TRUE(std::find(flags_3.begin(), flags_3.end(), Coordinate(2, 5)) != flags_3.end());
}

TEST(MoveGeneratorTests, TestGetPin_Multiple)
{
	const auto wk = TestHelpers::get_piece(PieceType::KING, Player::WHITE);
	const auto wp = TestHelpers::get_piece(PieceType::PAWN, Player::WHITE);
	const auto br = TestHelpers::get_piece(PieceType::ROOK, Player::BLACK);
	auto boards = Boards({
		{ {}, {}, br, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ br, {}, wp, {}, wk },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, wk, {}, {} },
	}, Player::WHITE);

	auto pins = MoveGenerator::get_pins(boards, Player::WHITE);

	EXPECT_EQ(pins.size(), 1);

	auto& pin = pins.front();

	auto flags = pin.get_move_mask()->get_flagged();

	EXPECT_EQ(flags.size(), 1);
	EXPECT_EQ(flags.front(), Coordinate(2, 2));
}

#pragma endregion
