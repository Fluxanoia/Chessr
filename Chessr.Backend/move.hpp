#pragma once

#include "types.hpp"

class Move {
private:

	const MoveProperty move_property;
	const Coordinate from;
	const Coordinate to;

public:

	Move(
		const Coordinate from,
		const Coordinate to,
		const MoveProperty move_property = MoveProperty::NONE);

	const Coordinate& get_from() const;
	const Coordinate& get_to() const;
	const MoveProperty& get_property() const;

};
