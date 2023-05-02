#include "move.hpp"

Move::Move(
	const Coordinate from,
	const Coordinate to,
	const MoveProperty move_property)
	: from(from), to(to), move_property(move_property)
{
}

const Coordinate& Move::get_from() const
{
	return this->from;
}

const Coordinate& Move::get_to() const
{
	return this->to;
}

const MoveProperty& Move::get_property() const
{
	return this->move_property;
}
