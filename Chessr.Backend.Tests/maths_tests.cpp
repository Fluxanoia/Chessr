#include "pch.h"

#include "../Chessr.Backend/maths.hpp"

TEST(MathsTests, TestAddCoordinate)
{
	auto result = Maths::add_coordinates({ -1999, 20 }, { 2, 4 });
	EXPECT_EQ(result.first, -1997);
	EXPECT_EQ(result.second, 24);
}

TEST(MathsTests, TestInBounds)
{
	EXPECT_TRUE(Maths::in_bounds({ 4, 3 }, { 0, 0 }));
	EXPECT_TRUE(Maths::in_bounds({ 4, 3 }, { 1, 0 }));
	EXPECT_TRUE(Maths::in_bounds({ 4, 3 }, { 1, 1 }));

	EXPECT_FALSE(Maths::in_bounds({ 4, 3 }, { 3, -1 }));
	EXPECT_FALSE(Maths::in_bounds({ 4, 3 }, { -1, 4 }));
	EXPECT_FALSE(Maths::in_bounds({ 4, 3 }, { 3, 1 }));
	EXPECT_FALSE(Maths::in_bounds({ 4, 3 }, { 1, 4 }));
	EXPECT_FALSE(Maths::in_bounds({ 4, 3 }, { 4, 3 }));
	EXPECT_FALSE(Maths::in_bounds({ 4, 3 }, { 5, 5 }));
}

TEST(MathsTests, TestGetOpposingPlayer)
{
	EXPECT_EQ(Maths::get_opposing_player(Player::BLACK), Player::WHITE);
	EXPECT_EQ(Maths::get_opposing_player(Player::WHITE), Player::BLACK);
}
