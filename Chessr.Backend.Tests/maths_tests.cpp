#include "pch.h"

#include "../Chessr.Backend/maths.hpp"

TEST(MathsTests, TestAddCoordinate)
{
	auto result = Maths::add_coordinates({ -1999, 20 }, { 2, 4 });
	EXPECT_EQ(result.first, -1997);
	EXPECT_EQ(result.second, 24);
}

TEST(MathsTests, TestSubtractCoordinate)
{
	auto result = Maths::subtract_coordinates({ -1999, 20 }, { 2, 4 });
	EXPECT_EQ(result.first, -2001);
	EXPECT_EQ(result.second, 16);
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

TEST(MathsTests, TestFlipVector)
{
	EXPECT_EQ(Maths::flip_vector({ 101, 201 }), Coordinate(-101, 201));
	EXPECT_EQ(Maths::flip_vector({ -101, 201 }), Coordinate(101, 201));
}

TEST(MathsTests, TestFlipVectors)
{
	const std::vector<Coordinate> vectors = {
		{ 101, 201 },
		{ -102, -202 },
		{ 103, -203 }
	};

	const auto& flipped = Maths::flip_vectors(vectors);

	EXPECT_EQ(vectors.at(0), Coordinate(101, 201));
	EXPECT_EQ(vectors.at(1), Coordinate(-102, -202));
	EXPECT_EQ(vectors.at(2), Coordinate(103, -203));

	EXPECT_EQ(flipped.at(0), Coordinate(-101, 201));
	EXPECT_EQ(flipped.at(1), Coordinate(102, -202));
	EXPECT_EQ(flipped.at(2), Coordinate(-103, -203));
}

TEST(MathsTests, TestFlipVectorsWithPlayer)
{
	const std::vector<Coordinate> vectors = {
		{ 101, 201 },
		{ -102, -202 },
		{ 103, -203 }
	};

	const auto& not_flipped = Maths::flip_vectors(vectors, Player::WHITE);

	EXPECT_EQ(vectors.at(0), Coordinate(101, 201));
	EXPECT_EQ(vectors.at(1), Coordinate(-102, -202));
	EXPECT_EQ(vectors.at(2), Coordinate(103, -203));

	EXPECT_EQ(not_flipped.at(0), Coordinate(101, 201));
	EXPECT_EQ(not_flipped.at(1), Coordinate(-102, -202));
	EXPECT_EQ(not_flipped.at(2), Coordinate(103, -203));

	const auto& flipped = Maths::flip_vectors(vectors, Player::BLACK);

	EXPECT_EQ(vectors.at(0), Coordinate(101, 201));
	EXPECT_EQ(vectors.at(1), Coordinate(-102, -202));
	EXPECT_EQ(vectors.at(2), Coordinate(103, -203));

	EXPECT_EQ(flipped.at(0), Coordinate(-101, 201));
	EXPECT_EQ(flipped.at(1), Coordinate(102, -202));
	EXPECT_EQ(flipped.at(2), Coordinate(-103, -203));
}
