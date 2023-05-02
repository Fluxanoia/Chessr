#pragma once

#include "flag_board.hpp"

class PinnedPiece
{
private:

	const Coordinate coordinate;
	FlagBoard move_mask;

public:

	PinnedPiece(const Coordinate coordinate, FlagBoard move_mask);

	const Coordinate& get_coordinate() const;
	FlagBoard& get_move_mask();

};

