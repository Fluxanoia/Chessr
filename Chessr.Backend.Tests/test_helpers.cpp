#include "pch.h"

#include "test_helpers.hpp"

std::optional<Piece> TestHelpers::get_piece(PieceType piece_type, Player player)
{
	return Piece{ piece_type, player };
}

std::shared_ptr<PieceData> TestHelpers::get_piece_data(
	std::vector<Coordinate> attack_rays,
	std::vector<Coordinate> attack_jumps,
	std::vector<Coordinate> push_rays,
	std::vector<Coordinate> push_jumps)
{
	return std::make_shared<PieceData>(
		"P",
		attack_rays,
		attack_jumps,
		push_rays,
		push_jumps);
}

bool TestHelpers::contains_move(
	const std::vector<std::shared_ptr<Move>>& moves,
	const Coordinate from,
	const Coordinate to)
{
	for (const auto& move : moves)
	{
		const auto& move_consequence = move->get_move_consequence();
		if (!move_consequence.has_value())
		{
			continue;
		}

		if (move_consequence.value()->get_from() == from
			&& move_consequence.value()->get_to() == to)
		{
			return true;
		}
	}
	return false;
}

std::shared_ptr<Move> TestHelpers::get_move(
	const std::vector<std::shared_ptr<Move>>& moves,
	const Coordinate from,
	const Coordinate to) 
{
	for (const auto& move : moves)
	{
		const auto& move_consequence = move->get_move_consequence();
		if (!move_consequence.has_value())
		{
			continue;
		}

		if (move_consequence.value()->get_from() == from
			&& move_consequence.value()->get_to() == to)
		{
			return move;
		}
	}
	return nullptr;
}
