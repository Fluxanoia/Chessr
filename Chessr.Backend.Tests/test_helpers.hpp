#pragma once

#include <optional>
#include "../Chessr.Backend/piece.hpp"
#include "../Chessr.Backend/piece_data.hpp"

class TestHelpers
{
public:

	static std::optional<Piece> get_piece(PieceType piece_type, Player player);
	static PieceData TestHelpers::get_piece_data(
		std::vector<Coordinate> attack_rays,
		std::vector<Coordinate> attack_jumps,
		std::vector<Coordinate> push_rays,
		std::vector<Coordinate> push_jumps);

};