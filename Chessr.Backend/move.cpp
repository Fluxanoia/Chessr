#include "move.hpp"

Move::Move(const Coordinate from, const Coordinate to) : from(from), to(to) {}

const Coordinate& Move::get_from() const
{
	return this->from;
}

const Coordinate& Move::get_to() const
{
	return this->to;
}
