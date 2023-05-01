#pragma once

#include "types.hpp"

class Piece
{
private:

	const PieceType type;
	const Player player;

public:

	Piece(const PieceType type, const Player player);

	const PieceType& get_type() const;
	const Player& get_player() const;

};
