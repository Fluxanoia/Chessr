#include "pinned_piece.hpp"

PinnedPiece::PinnedPiece(const Coordinate coordinate, std::shared_ptr<FlagBoard> move_mask) : coordinate(coordinate), move_mask(move_mask)
{
}

const Coordinate& PinnedPiece::get_coordinate() const
{
	return this->coordinate;
}

std::shared_ptr<FlagBoard> PinnedPiece::get_move_mask()
{
	return this->move_mask;
}
