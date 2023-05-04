#pragma once

#include "flag_board.hpp"

class PinnedPiece
{
private:

	const Coordinate coordinate;
	std::shared_ptr<FlagBoard> move_mask;

public:

	PinnedPiece(const Coordinate coordinate, std::shared_ptr<FlagBoard> move_mask);

	const Coordinate& get_coordinate() const;
	std::shared_ptr<FlagBoard> get_move_mask();

};

