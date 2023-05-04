#pragma once

#include "types.hpp"
#include "exceptions.hpp"

enum class ConsequenceType
{
	MOVE,
	REMOVE,
	CHANGE
};

class Consequence
{
public:

	virtual ~Consequence();

	virtual ConsequenceType get_type() const = 0;

};

class MoveConsequence : public Consequence
{
private:

	const MoveType move_type;
	const MoveStyle move_style;
	const Coordinate move_vector;

	const Coordinate from;
	const Coordinate to;

public:

	MoveConsequence(
		const MoveType move_type,
		const MoveStyle move_style,
		const Coordinate move_vector,
		const Coordinate from,
		const Coordinate to);
	
	ConsequenceType get_type() const;

	const MoveType& get_move_type() const;
	const MoveStyle& get_style() const;
	const Coordinate& get_move_vector() const;

	Coordinate get_from() const;
	Coordinate get_to() const;

};

class RemoveConsequence : public Consequence
{
private:

	const Coordinate coordinate;

public:

	RemoveConsequence(const Coordinate coordinate);

	ConsequenceType get_type() const;
	Coordinate get_coordinate() const;

};

class ChangeConsequence : public Consequence
{
private:

	const Coordinate coordinate;
	const PieceType piece_type;

public:

	ChangeConsequence(const Coordinate coordinate, const PieceType piece_type);

	ConsequenceType get_type() const;
	Coordinate get_coordinate() const;
	PieceType get_piece_type() const;

};
