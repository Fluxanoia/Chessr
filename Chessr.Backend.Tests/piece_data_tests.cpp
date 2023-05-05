#include "pch.h"
#include "test_helpers.hpp"

#include "../Chessr.Backend/piece_data.hpp"
#include "../Chessr.Backend/piece_configuration.hpp"

#pragma region get_vectors

TEST(PieceDataTests, TestVectors)
{
	PieceData data = {
		"X",
		{ { 1, 1 }, { 2, 2 }, { 3, 3 } },
		{ { -1, -1 }, { -2, -2 }, { -3, -3 } },
		{ { 4, 4 }, { 5, 5 }, { 6, 6 } },
		{ { -4, -4 }, { -5, -5 }, { -6, -6 } }
	};

	const auto& attack_rays = data.get_vectors(MoveType::ATTACK, MoveStyle::RAY, Player::WHITE);
	const auto& attack_jumps = data.get_vectors(MoveType::ATTACK, MoveStyle::JUMP, Player::WHITE);
	const auto& push_rays = data.get_vectors(MoveType::PUSH, MoveStyle::RAY, Player::WHITE);
	const auto& push_jumps = data.get_vectors(MoveType::PUSH, MoveStyle::JUMP, Player::WHITE);

	const auto& black_attack_rays = data.get_vectors(MoveType::ATTACK, MoveStyle::RAY, Player::BLACK);
	const auto& black_attack_jumps = data.get_vectors(MoveType::ATTACK, MoveStyle::JUMP, Player::BLACK);
	const auto& black_push_rays = data.get_vectors(MoveType::PUSH, MoveStyle::RAY, Player::BLACK);
	const auto& black_push_jumps = data.get_vectors(MoveType::PUSH, MoveStyle::JUMP, Player::BLACK);

	EXPECT_EQ(data.get_representation(), "X");

	EXPECT_EQ(attack_rays.size(), 3);
	EXPECT_EQ(attack_jumps.size(), 3);
	EXPECT_EQ(push_rays.size(), 3);
	EXPECT_EQ(push_jumps.size(), 3);

	EXPECT_TRUE(std::find(attack_rays.begin(), attack_rays.end(), Coordinate(1, 1)) != attack_rays.end());
	EXPECT_TRUE(std::find(attack_rays.begin(), attack_rays.end(), Coordinate(2, 2)) != attack_rays.end());
	EXPECT_TRUE(std::find(attack_rays.begin(), attack_rays.end(), Coordinate(3, 3)) != attack_rays.end());

	EXPECT_TRUE(std::find(attack_jumps.begin(), attack_jumps.end(), Coordinate(-1, -1)) != attack_jumps.end());
	EXPECT_TRUE(std::find(attack_jumps.begin(), attack_jumps.end(), Coordinate(-2, -2)) != attack_jumps.end());
	EXPECT_TRUE(std::find(attack_jumps.begin(), attack_jumps.end(), Coordinate(-3, -3)) != attack_jumps.end());

	EXPECT_TRUE(std::find(push_rays.begin(), push_rays.end(), Coordinate(4, 4)) != push_rays.end());
	EXPECT_TRUE(std::find(push_rays.begin(), push_rays.end(), Coordinate(5, 5)) != push_rays.end());
	EXPECT_TRUE(std::find(push_rays.begin(), push_rays.end(), Coordinate(6, 6)) != push_rays.end());

	EXPECT_TRUE(std::find(push_jumps.begin(), push_jumps.end(), Coordinate(-4, -4)) != push_jumps.end());
	EXPECT_TRUE(std::find(push_jumps.begin(), push_jumps.end(), Coordinate(-5, -5)) != push_jumps.end());
	EXPECT_TRUE(std::find(push_jumps.begin(), push_jumps.end(), Coordinate(-6, -6)) != push_jumps.end());

	EXPECT_TRUE(std::find(black_attack_rays.begin(), black_attack_rays.end(), Coordinate(-1, 1)) != black_attack_rays.end());
	EXPECT_TRUE(std::find(black_attack_rays.begin(), black_attack_rays.end(), Coordinate(-2, 2)) != black_attack_rays.end());
	EXPECT_TRUE(std::find(black_attack_rays.begin(), black_attack_rays.end(), Coordinate(-3, 3)) != black_attack_rays.end());

	EXPECT_TRUE(std::find(black_attack_jumps.begin(), black_attack_jumps.end(), Coordinate(1, -1)) != black_attack_jumps.end());
	EXPECT_TRUE(std::find(black_attack_jumps.begin(), black_attack_jumps.end(), Coordinate(2, -2)) != black_attack_jumps.end());
	EXPECT_TRUE(std::find(black_attack_jumps.begin(), black_attack_jumps.end(), Coordinate(3, -3)) != black_attack_jumps.end());

	EXPECT_TRUE(std::find(black_push_rays.begin(), black_push_rays.end(), Coordinate(-4, 4)) != black_push_rays.end());
	EXPECT_TRUE(std::find(black_push_rays.begin(), black_push_rays.end(), Coordinate(-5, 5)) != black_push_rays.end());
	EXPECT_TRUE(std::find(black_push_rays.begin(), black_push_rays.end(), Coordinate(-6, 6)) != black_push_rays.end());

	EXPECT_TRUE(std::find(black_push_jumps.begin(), black_push_jumps.end(), Coordinate(4, -4)) != black_push_jumps.end());
	EXPECT_TRUE(std::find(black_push_jumps.begin(), black_push_jumps.end(), Coordinate(5, -5)) != black_push_jumps.end());
	EXPECT_TRUE(std::find(black_push_jumps.begin(), black_push_jumps.end(), Coordinate(6, -6)) != black_push_jumps.end());
}

#pragma endregion

#pragma region get_ray

TEST(MoveGeneratorTests, TestGetRay)
{
	auto bp = TestHelpers::get_piece(PieceType::PAWN, Player::BLACK);
	auto boards = Boards({
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, bp, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
	}, Player::WHITE);

	auto piece_data = TestHelpers::get_piece_data({}, {}, {}, {});

	auto ray_1 = piece_data->get_ray(boards, Player::WHITE, { 0, 1 }, { 1, 1 }, {}, false);
	auto ray_2 = piece_data->get_ray(boards, Player::WHITE, { -1, 1 }, { 3, 0 }, {}, false);
	auto ray_3 = piece_data->get_ray(boards, Player::WHITE, { 1, 2 }, { 0, 0 }, {}, false);

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
	auto bp = TestHelpers::get_piece(PieceType::PAWN, Player::BLACK);
	auto wp = TestHelpers::get_piece(PieceType::PAWN, Player::WHITE);
	auto boards = Boards({
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, bp, {} },
		{ {}, wp, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
	}, Player::WHITE);

	auto piece_data = TestHelpers::get_piece_data({}, {}, {}, {});

	auto ray_1 = piece_data->get_ray(boards, Player::WHITE, { 0, 1 }, { 1, 1 }, {}, true);
	auto ray_2 = piece_data->get_ray(boards, Player::WHITE, { -1, 1 }, { 3, 0 }, {}, true);
	auto ray_3 = piece_data->get_ray(boards, Player::WHITE, { 1, 2 }, { 0, 1 }, {}, true);

	EXPECT_EQ(ray_1.size(), 2);
	EXPECT_EQ(ray_1.at(0), Coordinate(1, 2));
	EXPECT_EQ(ray_1.at(1), Coordinate(1, 3));

	EXPECT_EQ(ray_2.size(), 0);

	EXPECT_EQ(ray_3.size(), 1);
	EXPECT_EQ(ray_3.at(0), Coordinate(1, 3));
}

TEST(MoveGeneratorTests, TestGetRay_Ignoring)
{
	auto bp = TestHelpers::get_piece(PieceType::PAWN, Player::BLACK);
	auto wp = TestHelpers::get_piece(PieceType::PAWN, Player::WHITE);
	auto boards = Boards({
		{ {}, {}, {}, {}, {} },
		{ {}, {}, bp, {}, {} },
		{ {}, wp, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
	}, Player::WHITE);

	auto piece_data = TestHelpers::get_piece_data({}, {}, {}, {});

	auto ray_1 = piece_data->get_ray(boards, Player::WHITE, { 0, 1 }, { 1, 1 }, Coordinate{ 1, 2 }, false);
	auto ray_2 = piece_data->get_ray(boards, Player::WHITE, { -1, 1 }, { 3, 0 }, Coordinate{ 2, 1 }, true);
	auto ray_3 = piece_data->get_ray(boards, Player::WHITE, { 1, -1 }, { 0, 3 }, Coordinate{ 1, 2 }, true);

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
	auto bp = TestHelpers::get_piece(PieceType::PAWN, Player::BLACK);
	auto boards = Boards({
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, bp, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
	}, Player::WHITE);

	auto piece_data = TestHelpers::get_piece_data({}, {}, {}, {});

	auto jump_1 = piece_data->get_jump(boards, Player::WHITE, { 0, 1 }, { 2, 1 }, false);
	auto jump_2 = piece_data->get_jump(boards, Player::WHITE, { 0, 1 }, { 3, 1 }, false);
	auto jump_3 = piece_data->get_jump(boards, Player::WHITE, { -4, 4 }, { 4, 0 }, false);
	auto jump_4 = piece_data->get_jump(boards, Player::WHITE, { -2, 2 }, { 4, 0 }, false);

	EXPECT_FALSE(jump_1.has_value());

	EXPECT_TRUE(jump_2.has_value());
	EXPECT_EQ(jump_2.value(), Coordinate(3, 2));

	EXPECT_TRUE(jump_3.has_value());
	EXPECT_EQ(jump_3.value(), Coordinate(0, 4));

	EXPECT_FALSE(jump_4.has_value());
}

TEST(MoveGeneratorTests, TestGetJump_Attacks)
{
	auto bp = TestHelpers::get_piece(PieceType::PAWN, Player::BLACK);
	auto wp = TestHelpers::get_piece(PieceType::PAWN, Player::WHITE);
	auto boards = Boards({
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, bp, {}, {} },
		{ {}, {}, {}, {}, {} },
		{ {}, {}, {}, {}, wp },
	}, Player::WHITE);

	auto piece_data = TestHelpers::get_piece_data({}, {}, {}, {});

	auto jump_1 = piece_data->get_jump(boards, Player::WHITE, { 0, 1 }, { 2, 1 }, true);
	auto jump_2 = piece_data->get_jump(boards, Player::WHITE, { 0, 1 }, { 4, 3 }, true);
	auto jump_3 = piece_data->get_jump(boards, Player::BLACK, { 4, 4 }, { 0, 0 }, true);
	auto jump_4 = piece_data->get_jump(boards, Player::WHITE, { -2, 2 }, { 4, 0 }, true);

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
	auto boards = Boards({
		{ {}, {}, {}, {}, {} },
		{ {}, bl, {}, {}, bl },
		{ {}, {}, {}, {}, {} },
		{ {}, wh, {}, bl, {} },
		{ {}, {}, {}, {}, {} },
	}, Player::WHITE);

	auto piece_data = TestHelpers::get_piece_data(
		{},
		{},
		{ { 0, -1 }, { -2, -1 }, { -1, 0 }, { 0, 1 }, { -1, 1 }, { 1, 0 } },
		{});

	auto moves = piece_data->get_moves(boards, Player::WHITE, { 3, 2 }, MoveType::PUSH, MoveStyle::ALL, {});

	EXPECT_EQ(moves.size(), 5);
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(0, 2)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(1, 2)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(2, 2)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(4, 2)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(2, 3)));
}

TEST(MoveGeneratorTests, TestGetMoves_Attacks)
{
	const auto bl = TestHelpers::get_piece(PieceType::PAWN, Player::BLACK);
	const auto wh = TestHelpers::get_piece(PieceType::PAWN, Player::WHITE);
	auto boards = Boards({
		{ {}, {}, {}, {}, {} },
		{ {}, bl, {}, {}, bl },
		{ {}, {}, {}, {}, {} },
		{ {}, wh, {}, bl, {} },
		{ {}, {}, {}, {}, {} },
	}, Player::WHITE);

	auto piece_data = TestHelpers::get_piece_data(
		{ { 0, -1 }, { -2, -1 }, { -1, 0 }, { 0, 1 }, { -1, 1 }, { 1, 0 } },
		{},
		{},
		{});

	auto moves = piece_data->get_moves(boards, Player::WHITE, { 3, 2 }, MoveType::ATTACK, MoveStyle::ALL, {});

	EXPECT_EQ(moves.size(), 8);
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(0, 2)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(1, 2)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(2, 2)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(4, 2)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(2, 3)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(3, 3)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(1, 1)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(1, 4)));
}

TEST(MoveGeneratorTests, TestGetMoves_Ignoring)
{
	const auto bl = TestHelpers::get_piece(PieceType::PAWN, Player::BLACK);
	const auto wh = TestHelpers::get_piece(PieceType::PAWN, Player::WHITE);
	auto boards = Boards({
		{ {}, {}, {}, {}, {} },
		{ {}, bl, {}, {}, bl },
		{ {}, {}, {}, {}, {} },
		{ {}, wh, {}, bl, {} },
		{ {}, {}, {}, {}, {} },
	}, Player::WHITE);

	auto piece_data = TestHelpers::get_piece_data(
		{ { 0, -1 }, { -2, -1 }, { -1, 0 }, { 0, 1 }, { -1, 1 }, { 1, 0 } },
		{},
		{},
		{});

	auto moves = piece_data->get_moves(boards, Player::WHITE, { 3, 2 }, MoveType::ATTACK, MoveStyle::ALL, Coordinate{ 3, 3 });

	EXPECT_EQ(moves.size(), 9);
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(0, 2)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(1, 2)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(2, 2)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(4, 2)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(2, 3)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(3, 3)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(3, 4)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(1, 1)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(3, 2), Coordinate(1, 4)));
}

TEST(MoveGeneratorTests, TestGetMoves_Pawn_DoubleMove)
{
	const auto wp = TestHelpers::get_piece(PieceType::PAWN, Player::WHITE);
	auto boards = Boards({
		{ {}, {}, {} },
		{ {}, {}, {} },
		{ {}, wp, {} },
		{ {}, {}, {} },
	}, Player::WHITE);

	const auto& piece_config = PieceConfiguration();
	const auto& piece_data = piece_config.get_piece_data(PieceType::PAWN);

	auto moves = piece_data->get_moves(boards, Player::WHITE, { 2, 1 }, MoveType::PUSH, MoveStyle::ALL, {});

	EXPECT_EQ(moves.size(), 2);
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(2, 1), Coordinate(1, 1)));
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(2, 1), Coordinate(0, 1)));

	auto move = TestHelpers::get_move(moves, Coordinate(2, 1), Coordinate(0, 1));

	EXPECT_EQ(move->get_property(), MoveProperty::DOUBLE_MOVE);
}

TEST(MoveGeneratorTests, TestGetMoves_Pawn_Promotion)
{
	const auto wp = TestHelpers::get_piece(PieceType::PAWN, Player::WHITE);
	auto boards = Boards({
		{ {}, {}, {} },
		{ {}, wp, {} },
		{ {}, {}, {} },
		{ {}, {}, {} },
		}, Player::WHITE);

	const auto& piece_config = PieceConfiguration();
	const auto& piece_data = piece_config.get_piece_data(PieceType::PAWN);

	auto moves = piece_data->get_moves(boards, Player::WHITE, { 1, 1 }, MoveType::PUSH, MoveStyle::ALL, {});

	EXPECT_EQ(moves.size(), 1);
	EXPECT_TRUE(TestHelpers::contains_move(moves, Coordinate(1, 1), Coordinate(0, 1)));

	auto& move = moves.front();

	EXPECT_EQ(move->get_property(), MoveProperty::PROMOTION);
}

TEST(MoveGeneratorTests, TestGetMoves_Pawn_EnPassant)
{
	const auto wp = TestHelpers::get_piece(PieceType::PAWN, Player::WHITE);
	const auto bp = TestHelpers::get_piece(PieceType::PAWN, Player::BLACK);
	auto boards = Boards({
		{ {}, {}, bp },
		{ {}, {}, {} },
		{ {}, wp, {} },
		{ {}, {}, {} },
		}, Player::BLACK);

	const auto& piece_config = PieceConfiguration();
	const auto& piece_data = piece_config.get_piece_data(PieceType::PAWN);

	auto first_moves = piece_data->get_moves(boards, Player::BLACK, { 0, 2 }, MoveType::ALL, MoveStyle::ALL, {});
	auto first_move = TestHelpers::get_move(first_moves, { 0, 2 }, { 2, 2 });

	boards.apply_move(first_move);

	auto second_moves = piece_data->get_moves(boards, Player::WHITE, { 2, 1 }, MoveType::ALL, MoveStyle::ALL, {});

	EXPECT_TRUE(TestHelpers::contains_move(second_moves, Coordinate(2, 1), Coordinate(1, 2)));

	auto second_move = TestHelpers::get_move(second_moves, Coordinate(2, 1), Coordinate(1, 2));

	EXPECT_EQ(second_move->get_property(), MoveProperty::EN_PASSANT);

	boards.apply_move(second_move);

	const auto& board = boards.get_current_board();

	EXPECT_TRUE(board.has_piece({ 1, 2 }));
	EXPECT_FALSE(board.has_piece({ 2, 2 }));

	const auto& piece = board.get_piece({ 1, 2 });

	EXPECT_EQ(piece.get_type(), PieceType::PAWN);
	EXPECT_EQ(piece.get_player(), Player::WHITE);
}

TEST(MoveGeneratorTests, TestGetMoves_King_CastleKingSide)
{
	const auto wk = TestHelpers::get_piece(PieceType::KING, Player::WHITE);
	const auto wr = TestHelpers::get_piece(PieceType::ROOK, Player::WHITE);
	auto boards = Boards({
		{ wr, {}, {}, {}, wk, {}, {}, wr },
	}, Player::WHITE);

	const auto& piece_config = PieceConfiguration();
	const auto& piece_data = piece_config.get_piece_data(PieceType::KING);

	auto moves = piece_data->get_moves(boards, Player::WHITE, { 0, 4 }, MoveType::PUSH, MoveStyle::ALL, {});
	auto move = TestHelpers::get_move(moves, { 0, 4 }, { 0, 6 });

	EXPECT_EQ(move->get_property(), MoveProperty::CASTLE);

	boards.apply_move(move);

	const auto& board = boards.get_current_board();

	EXPECT_FALSE(board.has_piece({ 0, 4 }));
	EXPECT_TRUE(board.has_piece({ 0, 5 }));
	EXPECT_TRUE(board.has_piece({ 0, 6 }));
	EXPECT_FALSE(board.has_piece({ 0, 7 }));

	const auto& king = board.get_piece({ 0, 6 });
	const auto& rook = board.get_piece({ 0, 5 });

	EXPECT_EQ(king.get_type(), PieceType::KING);
	EXPECT_EQ(rook.get_type(), PieceType::ROOK);
}

TEST(MoveGeneratorTests, TestGetMoves_King_CastleQueenSide)
{
	const auto wk = TestHelpers::get_piece(PieceType::KING, Player::WHITE);
	const auto wr = TestHelpers::get_piece(PieceType::ROOK, Player::WHITE);
	auto boards = Boards({
		{ wr, {}, {}, {}, wk, {}, {}, wr },
		}, Player::WHITE);

	const auto& piece_config = PieceConfiguration();
	const auto& piece_data = piece_config.get_piece_data(PieceType::KING);

	auto moves = piece_data->get_moves(boards, Player::WHITE, { 0, 4 }, MoveType::PUSH, MoveStyle::ALL, {});
	auto move = TestHelpers::get_move(moves, { 0, 4 }, { 0, 2 });

	EXPECT_EQ(move->get_property(), MoveProperty::CASTLE);

	boards.apply_move(move);

	const auto& board = boards.get_current_board();

	EXPECT_FALSE(board.has_piece({ 0, 0 }));
	EXPECT_FALSE(board.has_piece({ 0, 1 }));
	EXPECT_TRUE(board.has_piece({ 0, 2 }));
	EXPECT_TRUE(board.has_piece({ 0, 3 }));
	EXPECT_FALSE(board.has_piece({ 0, 4 }));

	const auto& king = board.get_piece({ 0, 2 });
	const auto& rook = board.get_piece({ 0, 3 });

	EXPECT_EQ(king.get_type(), PieceType::KING);
	EXPECT_EQ(rook.get_type(), PieceType::ROOK);
}

#pragma endregion
