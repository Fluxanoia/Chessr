#pragma once

#include "types.hpp"

class Move {
private:

	const Coordinate from;
	const Coordinate to;

public:

	Move(const Coordinate from, const Coordinate to);

	const Coordinate& get_from() const;
	const Coordinate& get_to() const;

};
