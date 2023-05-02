#include "pch.h"

#include "../Chessr.Backend/piece_data.hpp"

TEST(PieceDataTests, TestPieceData)
{
	PieceData data = {
		"X",
		{ { 1, 1 }, { 2, 2 }, { 3, 3 } },
		{ { -1, -1 }, { -2, -2 }, { -3, -3 } },
		{ { 4, 4 }, { 5, 5 }, { 6, 6 } },
		{ { -4, -4 }, { -5, -5 }, { -6, -6 } }
	};

	const auto& attack_rays = data.get_attack_rays(Player::WHITE);
	const auto& attack_jumps = data.get_attack_jumps(Player::WHITE);
	const auto& push_rays = data.get_push_rays(Player::WHITE);
	const auto& push_jumps = data.get_push_jumps(Player::WHITE);

	const auto& black_attack_rays = data.get_attack_rays(Player::BLACK);
	const auto& black_attack_jumps = data.get_attack_jumps(Player::BLACK);
	const auto& black_push_rays = data.get_push_rays(Player::BLACK);
	const auto& black_push_jumps = data.get_push_jumps(Player::BLACK);

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
