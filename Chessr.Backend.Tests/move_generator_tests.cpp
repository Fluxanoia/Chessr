#include "pch.h"
#include "test_helpers.hpp"

#include "../Chessr.Backend/move_generator.hpp"

#pragma region get_king_move_mask

TEST(MoveGeneratorTests, TestGetKingMoveMask1)
{
	const auto bk = TestHelpers::get_piece(PieceType::KING, Player::BLACK);
	const auto wk = TestHelpers::get_piece(PieceType::KING, Player::WHITE);
	const auto wr = TestHelpers::get_piece(PieceType::ROOK, Player::WHITE);
	auto board = Board({
		{ {}, {}, bk, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, wr, {} },
		{ {}, {}, wk, {}, {} },
	});

	auto mask = MoveGenerator::get_king_move_mask(board, Player::BLACK, { 0, 2 });
	auto flagged = mask.get_flagged();

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
	auto board = Board({
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, bk, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, wr, {} },
		{ {}, {}, wk, {}, {} },
	});

	auto mask = MoveGenerator::get_king_move_mask(board, Player::BLACK, { 1, 3 });
	auto flagged = mask.get_flagged();

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
	auto board = Board({
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, wk, {}, {} },
		{ {}, {}, {}, bb, {} },
		{ {}, {}, bk, {}, {} },
		});

	auto mask = MoveGenerator::get_king_move_mask(board, Player::WHITE, { 2, 2 });
	auto flagged = mask.get_flagged();

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
	auto board = Board({
		{ br, {}, bk, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, wr, {} },
		{ wr, {}, wk, {}, br },
	});

	auto piece_data = TestHelpers::get_piece_data(
		{ { 1, 0 }, { 1, -1 }, { -1, 0 } },
		{ { -2, 2 }, { 0, -2 }, { -2, -2 } },
		{},
		{});
	auto attacks = MoveGenerator::get_possible_attacks(board, Player::BLACK, piece_data, { 2, 2 }, {});

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
	auto board = Board({
		{ br, {}, bk, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, wr, {} },
		{ wr, {}, wk, {}, wr },
	});

	auto piece_data = TestHelpers::get_piece_data(
		{ { 1, 0 }, { 1, -1 }, { -1, 0 }, { -1, 1 } },
		{ { 0, -2 }, { -2, -2 } },
		{},
		{});
	auto attacks = MoveGenerator::get_possible_attacks(board, Player::BLACK, piece_data, { 2, 2 }, Coordinate{ 3, 3 });

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

// TODO

#pragma endregion

#pragma region get_blocks_to_attack

// TODO

#pragma endregion

#pragma region get_pins

// TODO

#pragma endregion

#pragma region get_ray

TEST(MoveGeneratorTests, TestGetRay)
{
	auto board = Board({
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, TestHelpers::get_piece(PieceType::PAWN, Player::BLACK), {}},
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
		});

	auto ray_1 = MoveGenerator::get_ray(board, Player::WHITE, { 0, 1 }, { 1, 1 }, {}, false);
	auto ray_2 = MoveGenerator::get_ray(board, Player::WHITE, { -1, 1 }, { 3, 0 }, {}, false);
	auto ray_3 = MoveGenerator::get_ray(board, Player::WHITE, { 1, 2 }, { 0, 0 }, {}, false);

	EXPECT_EQ(ray_1.size(), 1);
	EXPECT_EQ(ray_1.at(0), Coordinate(1, 2));

	EXPECT_EQ(ray_2.size(), 3);
	EXPECT_EQ(ray_2.at(0), Coordinate(2, 1));
	EXPECT_EQ(ray_2.at(1), Coordinate(1, 2));
	EXPECT_EQ(ray_2.at(2), Coordinate(0, 3));

	EXPECT_EQ(ray_3.size(), 2);
	EXPECT_EQ(ray_3.at(0), Coordinate(1, 2));
	EXPECT_EQ(ray_3.at(1), Coordinate(2, 4));
}

TEST(MoveGeneratorTests, TestGetRay_Attacks)
{
	auto board = Board({
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, TestHelpers::get_piece(PieceType::PAWN, Player::BLACK), {}},
		{ {}, TestHelpers::get_piece(PieceType::PAWN, Player::WHITE), {}, {}, {}},
		{ {}, {}, {}, {}, {} },
		});

	auto ray_1 = MoveGenerator::get_ray(board, Player::WHITE, { 0, 1 }, { 1, 1 }, {}, true);
	auto ray_2 = MoveGenerator::get_ray(board, Player::WHITE, { -1, 1 }, { 3, 0 }, {}, true);
	auto ray_3 = MoveGenerator::get_ray(board, Player::WHITE, { 1, 2 }, { 0, 1 }, {}, true);

	EXPECT_EQ(ray_1.size(), 2);
	EXPECT_EQ(ray_1.at(0), Coordinate(1, 2));
	EXPECT_EQ(ray_1.at(1), Coordinate(1, 3));

	EXPECT_EQ(ray_2.size(), 0);

	EXPECT_EQ(ray_3.size(), 1);
	EXPECT_EQ(ray_3.at(0), Coordinate(1, 3));
}

TEST(MoveGeneratorTests, TestGetRay_Ignoring)
{
	auto board = Board({
		{ {}, {}, {}, {}, {} },
		{ {}, {}, TestHelpers::get_piece(PieceType::PAWN, Player::BLACK), {}, {}},
		{ {}, TestHelpers::get_piece(PieceType::PAWN, Player::WHITE), {}, {}, {}},
		{ {}, {}, {}, {}, {} },
		});

	auto ray_1 = MoveGenerator::get_ray(board, Player::WHITE, { 0, 1 }, { 1, 1 }, Coordinate{ 1, 2 }, false);
	auto ray_2 = MoveGenerator::get_ray(board, Player::WHITE, { -1, 1 }, { 3, 0 }, Coordinate{ 2, 1 }, true);
	auto ray_3 = MoveGenerator::get_ray(board, Player::WHITE, { 1, -1 }, { 0, 3 }, Coordinate{ 1, 2 }, true);

	EXPECT_EQ(ray_1.size(), 3);
	EXPECT_EQ(ray_1.at(0), Coordinate(1, 2));
	EXPECT_EQ(ray_1.at(1), Coordinate(1, 3));
	EXPECT_EQ(ray_1.at(2), Coordinate(1, 4));

	EXPECT_EQ(ray_2.size(), 2);
	EXPECT_EQ(ray_2.at(0), Coordinate(2, 1));
	EXPECT_EQ(ray_2.at(1), Coordinate(1, 2));

	EXPECT_EQ(ray_3.size(), 1);
	EXPECT_EQ(ray_3.at(0), Coordinate(1, 2));
}

#pragma endregion

#pragma region get_jump

TEST(MoveGeneratorTests, TestGetJump)
{
	auto board = Board({
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, TestHelpers::get_piece(PieceType::PAWN, Player::BLACK), {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
	});

	auto jump_1 = MoveGenerator::get_jump(board, Player::WHITE, { 0, 1 }, { 2, 1 }, false);
	auto jump_2 = MoveGenerator::get_jump(board, Player::WHITE, { 0, 1 }, { 3, 1 }, false);
	auto jump_3 = MoveGenerator::get_jump(board, Player::WHITE, { -4, 4 }, { 4, 0 }, false);
	auto jump_4 = MoveGenerator::get_jump(board, Player::WHITE, { -2, 2 }, { 4, 0 }, false);

	EXPECT_FALSE(jump_1.has_value());

	EXPECT_TRUE(jump_2.has_value());
	EXPECT_EQ(jump_2.value(), Coordinate(3, 2));

	EXPECT_TRUE(jump_3.has_value());
	EXPECT_EQ(jump_3.value(), Coordinate(0, 4));

	EXPECT_FALSE(jump_4.has_value());
}

TEST(MoveGeneratorTests, TestGetJump_Attacks)
{
	auto board = Board({
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, TestHelpers::get_piece(PieceType::PAWN, Player::BLACK), {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, TestHelpers::get_piece(PieceType::PAWN, Player::WHITE) },
		});

	auto jump_1 = MoveGenerator::get_jump(board, Player::WHITE, { 0, 1 }, { 2, 1 }, true);
	auto jump_2 = MoveGenerator::get_jump(board, Player::WHITE, { 0, 1 }, { 4, 3 }, true);
	auto jump_3 = MoveGenerator::get_jump(board, Player::BLACK, { 4, 4 }, { 0, 0 }, true);
	auto jump_4 = MoveGenerator::get_jump(board, Player::WHITE, { -2, 2 }, { 4, 0 }, true);

	EXPECT_TRUE(jump_1.has_value());
	EXPECT_EQ(jump_1.value(), Coordinate(2, 2));

	EXPECT_FALSE(jump_2.has_value());

	EXPECT_TRUE(jump_3.has_value());
	EXPECT_EQ(jump_3.value(), Coordinate(4, 4));

	EXPECT_TRUE(jump_4.has_value());
	EXPECT_EQ(jump_4.value(), Coordinate(2, 2));
}

#pragma endregion

#pragma region get_moves

TEST(MoveGeneratorTests, TestGetMoves)
{
	const auto bl = TestHelpers::get_piece(PieceType::PAWN, Player::BLACK);
	const auto wh = TestHelpers::get_piece(PieceType::PAWN, Player::WHITE);
	auto board = Board({
		{ {}, {}, {}, {}, {} },
		{ {}, bl, {}, {}, bl },
		{ {}, {}, {}, {}, {} },
		{ {}, wh, {}, bl, {} },
		{ {}, {}, {}, {}, {} },
	});

	std::vector<Coordinate> rays = { { 0, -1 }, { -2, -1 }, { -1, 0 }, { 0, 1 }, { -1, 1 }, { 1, 0 } };
	std::vector<Coordinate> jumps = {};

	auto moves = MoveGenerator::get_moves(board, Player::WHITE, rays, jumps, { 3, 2 }, {}, false);

	EXPECT_EQ(moves.size(), 5);
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(0, 2)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(1, 2)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(2, 2)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(4, 2)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(2, 3)) != moves.end());
}

TEST(MoveGeneratorTests, TestGetMoves_Attacks)
{
	const auto bl = TestHelpers::get_piece(PieceType::PAWN, Player::BLACK);
	const auto wh = TestHelpers::get_piece(PieceType::PAWN, Player::WHITE);
	auto board = Board({
		{ {}, {}, {}, {}, {} },
		{ {}, bl, {}, {}, bl },
		{ {}, {}, {}, {}, {} },
		{ {}, wh, {}, bl, {} },
		{ {}, {}, {}, {}, {} },
		});

	std::vector<Coordinate> rays = { { 0, -1 }, { -2, -1 }, { -1, 0 }, { 0, 1 }, { -1, 1 }, { 1, 0 } };
	std::vector<Coordinate> jumps = {};

	auto moves = MoveGenerator::get_moves(board, Player::WHITE, rays, jumps, { 3, 2 }, {}, true);

	EXPECT_EQ(moves.size(), 8);
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(0, 2)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(1, 2)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(2, 2)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(4, 2)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(2, 3)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(3, 3)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(1, 1)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(1, 4)) != moves.end());
}

TEST(MoveGeneratorTests, TestGetMoves_Ignoring)
{
	const auto bl = TestHelpers::get_piece(PieceType::PAWN, Player::BLACK);
	const auto wh = TestHelpers::get_piece(PieceType::PAWN, Player::WHITE);
	auto board = Board({
		{ {}, {}, {}, {}, {} },
		{ {}, bl, {}, {}, bl },
		{ {}, {}, {}, {}, {} },
		{ {}, wh, {}, bl, {} },
		{ {}, {}, {}, {}, {} },
		});

	std::vector<Coordinate> rays = { { 0, -1 }, { -2, -1 }, { -1, 0 }, { 0, 1 }, { -1, 1 }, { 1, 0 } };
	std::vector<Coordinate> jumps = {};

	auto moves = MoveGenerator::get_moves(board, Player::WHITE, rays, jumps, { 3, 2 }, Coordinate{ 3, 3 }, true);

	EXPECT_EQ(moves.size(), 9);
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(0, 2)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(1, 2)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(2, 2)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(4, 2)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(2, 3)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(3, 3)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(3, 4)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(1, 1)) != moves.end());
	EXPECT_TRUE(std::find(moves.begin(), moves.end(), Coordinate(1, 4)) != moves.end());
}

#pragma endregion

#pragma region get_opposing_player

TEST(MoveGeneratorTests, TestGetOpposingPlayer)
{
	EXPECT_EQ(MoveGenerator::get_opposing_player(Player::BLACK), Player::WHITE);
	EXPECT_EQ(MoveGenerator::get_opposing_player(Player::WHITE), Player::BLACK);
}

#pragma endregion
