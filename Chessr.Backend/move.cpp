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

const std::optional<PieceType>& Move::get_promotion_piece_type() const
{
	return this->promotion_piece_type;
}

void Move::set_promotion_type(const PieceType piece_type)
{
	if (this->move_property != MoveProperty::PROMOTION)
	{
		throw InvalidOperationException("There was an attempt to set the promotion piece type for a non-promotion move.");
	}
	this->promotion_piece_type = piece_type;
}
