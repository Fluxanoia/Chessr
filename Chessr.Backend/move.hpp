#pragma once

#include "types.hpp"
#include "exceptions.hpp"	

class Move {
private:

	const MoveProperty move_property;
	const Coordinate from;
	const Coordinate to;

	std::optional<PieceType> promotion_piece_type = {};

public:

	Move(
		const Coordinate from,
		const Coordinate to,
		const MoveProperty move_property = MoveProperty::NONE);

	const Coordinate& get_from() const;
	const Coordinate& get_to() const;
	const MoveProperty& get_property() const;
	const std::optional<PieceType>& get_promotion_piece_type() const;

	void set_promotion_type(const PieceType piece_type);
};
