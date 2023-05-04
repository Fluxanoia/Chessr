#pragma once

#include <vector>
#include "move.hpp"
#include "piece.hpp"
#include "maths.hpp"
#include "types.hpp"
#include "exceptions.hpp"

class Board
{
private:

	const Coordinate dimensions;
	const Grid<Piece> grid;
	bool in_check = false;

public:

	Board(const Grid<Piece> position);
	
	bool is_in_check() const;
	void set_in_check();

	bool has_piece(const Coordinate& coordinate) const;
	const Piece& get_piece(const Coordinate& coordinate) const;

	bool rank_contains_multiple_of(
		const CoordinateValue rank,
		const PieceType piece_type,
		const Player player) const;
	bool file_contains_multiple_of(
		const CoordinateValue file,
		const PieceType piece_type,
		const Player player) const;
	std::vector<Coordinate> positions_of(
		const PieceType piece_type,
		const Player player) const;
	
	Coordinate get_dimensions() const;
	const Grid<Piece>& get_grid() const;

};

