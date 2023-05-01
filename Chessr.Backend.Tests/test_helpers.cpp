#include "pch.h"

#include "test_helpers.hpp"

std::optional<Piece> TestHelpers::get_piece(PieceType piece_type, Player player)
{
	return Piece{ piece_type, player };
}

PieceData TestHelpers::get_piece_data(
	std::vector<Coordinate> attack_rays,
	std::vector<Coordinate> attack_jumps,
	std::vector<Coordinate> push_rays,
	std::vector<Coordinate> push_jumps)
{
	return PieceData(
		"P",
		attack_rays,
		attack_jumps,
		push_rays,
		push_jumps);
}
