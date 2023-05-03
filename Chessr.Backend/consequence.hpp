#pragma once

#include "types.hpp"

enum class ConsequenceType
{
	MOVE,
	REMOVE,
	CHANGE
};

class Consequence
{
private:

	const ConsequenceType type;

public:

	Consequence(const ConsequenceType type);

	ConsequenceType get_type() const;

};

class MoveConsequence : public Consequence
{
private:

	const Coordinate from;
	const Coordinate to;

public:

	MoveConsequence(const Coordinate from, const Coordinate to);
	
	Coordinate get_from() const;
	Coordinate get_to() const;

};

class RemoveConsequence : public Consequence
{
private:

	const Coordinate coordinate;

public:

	RemoveConsequence(const Coordinate coordinate);

	Coordinate get_coordinate() const;

};

class ChangeConsequence : public Consequence
{
private:

	const Coordinate coordinate;
	const PieceType piece_type;

public:

	ChangeConsequence(const Coordinate coordinate, const PieceType piece_type);

	Coordinate get_coordinate() const;
	PieceType get_piece_type() const;

};
