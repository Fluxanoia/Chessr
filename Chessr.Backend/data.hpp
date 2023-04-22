#pragma once

#include <tuple>
#include "enums.hpp"

class Piece {
private:
	const PieceType type;
	const Player player;

public:
	Piece(PieceType type, Player player) : type(type), player(player) {}

	PieceType get_type() {
		return this->type;
	}

	Player get_player() {
		return this->player;
	}
};

class Move {
private:
	const std::tuple<int, int> from;
	const std::tuple<int, int> to;

public:
	Move(std::tuple<int, int> from, std::tuple<int, int> to) : from(from), to(to) {}

	std::tuple<int, int> get_from() {
		return this->from;
	}

	std::tuple<int, int> get_to() {
		return this->to;
	}
};
