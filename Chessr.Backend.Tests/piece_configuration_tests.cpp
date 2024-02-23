#include "pch.h"

#include "../Chessr.Backend/piece_configuration.hpp"

TEST(PieceConfigurationTests, TestGetNotationFromCoordinate)
{
	PieceConfiguration piece_config = {};
	EXPECT_EQ(piece_config.get_notation_from_coordinate({ 0, 0 }, 5), "a5");
	EXPECT_EQ(piece_config.get_notation_from_coordinate({ 0, 25 }, 5), "z5");
	EXPECT_EQ(piece_config.get_notation_from_coordinate({ 0, 26 }, 5), "aa5");
	EXPECT_EQ(piece_config.get_notation_from_coordinate({ 2, 29 }, 5), "ad3");
	EXPECT_EQ(piece_config.get_notation_from_coordinate({ 2, 705 }, 5), "aad3");
}

TEST(PieceConfigurationTests, TestGetCoordinateFromNotation)
{
	PieceConfiguration piece_config = {};
	EXPECT_EQ(piece_config.get_coordinate_from_notation("a5", 5), Coordinate(0, 0));
	EXPECT_EQ(piece_config.get_coordinate_from_notation("z5", 5), Coordinate(0, 25));
	EXPECT_EQ(piece_config.get_coordinate_from_notation("aa5", 5), Coordinate(0, 26));
	EXPECT_EQ(piece_config.get_coordinate_from_notation("ad3", 5).value(), Coordinate(2, 29));
	EXPECT_EQ(piece_config.get_coordinate_from_notation("aad3", 5).value(), Coordinate(2, 705));
}
