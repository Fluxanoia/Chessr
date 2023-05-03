#include "consequence.hpp"

Consequence::Consequence(const ConsequenceType type) : type(type)
{
}

ConsequenceType Consequence::get_type() const
{
	return this->type;
}

MoveConsequence::MoveConsequence(const Coordinate from, const Coordinate to) : Consequence(ConsequenceType::MOVE), from(from), to(to)
{
}

Coordinate MoveConsequence::get_from() const
{
	return this->from;
}

Coordinate MoveConsequence::get_to() const
{
	return this->to;
}

RemoveConsequence::RemoveConsequence(const Coordinate coordinate) : Consequence(ConsequenceType::REMOVE), coordinate(coordinate)
{
}

Coordinate RemoveConsequence::get_coordinate() const
{
	return this->coordinate;
}

ChangeConsequence::ChangeConsequence(const Coordinate coordinate, const PieceType piece_type)
	: Consequence(ConsequenceType::CHANGE), coordinate(coordinate), piece_type(piece_type)
{
}

Coordinate ChangeConsequence::get_coordinate() const
{
	return this->coordinate;
}

PieceType ChangeConsequence::get_piece_type() const
{
	return this->piece_type;
}
