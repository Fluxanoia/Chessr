#pragma once

#include <vector>
#include "data.hpp"
#include "maths.hpp"
#include "types.hpp"
#include "exceptions.hpp"

class Board
{
private:

	const Coordinate dimensions;
	const Grid<Piece> position;

public:

	Board(const Grid<Piece> position);
	
	bool has_piece(const Coordinate coordinate) const;
	const Piece& get_piece(const Coordinate coordinate) const;

	std::vector<Coordinate> positions_of(
		const PieceType piece_type,
		const Player player) const;
	
	const Coordinate& get_dimensions() const;

};

