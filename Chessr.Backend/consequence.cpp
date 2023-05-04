#include "consequence.hpp"

Consequence::~Consequence()
{
}

MoveConsequence::MoveConsequence(
	const MoveType move_type,
	const MoveStyle move_style,
	const Coordinate move_vector, 
	const Coordinate from,
	const Coordinate to)
	: move_type(move_type),
	move_style(move_style),
	move_vector(move_vector),
	from(from),
	to(to)
{
	if (move_type == MoveType::ALL)
	{
		throw InvalidOperationException("Invalid MoveType.");
	}
	if (move_style == MoveStyle::ALL)
	{
		throw InvalidOperationException("Invalid MoveStyle.");
	}
}

ConsequenceType MoveConsequence::get_type() const
{
	return ConsequenceType::MOVE;
}

const MoveType& MoveConsequence::get_move_type() const
{
	return this->move_type;
}

const MoveStyle& MoveConsequence::get_style() const
{
	return this->move_style;
}

const Coordinate& MoveConsequence::get_move_vector() const
{
	return this->move_vector;
}

Coordinate MoveConsequence::get_from() const
{
	return this->from;
}

Coordinate MoveConsequence::get_to() const
{
	return this->to;
}

RemoveConsequence::RemoveConsequence(const Coordinate coordinate) : coordinate(coordinate)
{
}

ConsequenceType RemoveConsequence::get_type() const
{
	return ConsequenceType::REMOVE;
}

Coordinate RemoveConsequence::get_coordinate() const
{
	return this->coordinate;
}

ChangeConsequence::ChangeConsequence(const Coordinate coordinate, const PieceType piece_type)
	: coordinate(coordinate), piece_type(piece_type)
{
}

ConsequenceType ChangeConsequence::get_type() const
{
	return ConsequenceType::CHANGE;
}

Coordinate ChangeConsequence::get_coordinate() const
{
	return this->coordinate;
}

PieceType ChangeConsequence::get_piece_type() const
{
	return this->piece_type;
}
