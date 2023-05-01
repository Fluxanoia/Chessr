#include "pinned_piece.hpp"

PinnedPiece::PinnedPiece(const Coordinate coordinate, FlagBoard& move_mask) : coordinate(coordinate), move_mask(move_mask)
{
}

const Coordinate& PinnedPiece::get_coordinate() const
{
	return this->coordinate;
}

FlagBoard& PinnedPiece::get_move_mask() const
{
	return this->move_mask;
}
