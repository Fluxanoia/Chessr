#pragma once

#include <tuple>
#include "types.hpp"

class Piece {
private:
	const PieceType type;
	const Player player;

public:
	Piece(PieceType type, Player player) : type(type), player(player) {}

	const PieceType& get_type() const
	{
		return this->type;
	}

	const Player& get_player() const
	{
		return this->player;
	}
};

class Move {
private:
	const Coordinate from;
	const Coordinate to;

public:
	Move(Coordinate from, Coordinate to) : from(from), to(to) {}

	const Coordinate& get_from() const
	{
		return this->from;
	}

	const Coordinate& get_to() const
	{
		return this->to;
	}
};
