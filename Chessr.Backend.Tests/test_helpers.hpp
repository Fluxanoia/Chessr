#pragma once

#include <optional>
#include "../Chessr.Backend/piece.hpp"
#include "../Chessr.Backend/piece_data.hpp"

class TestHelpers
{
public:

	static std::optional<Piece> get_piece(PieceType piece_type, Player player);
	static std::shared_ptr<PieceData> TestHelpers::get_piece_data(
		std::vector<Coordinate> attack_rays,
		std::vector<Coordinate> attack_jumps,
		std::vector<Coordinate> push_rays,
		std::vector<Coordinate> push_jumps);

	static bool contains_move(
		const std::vector<std::shared_ptr<Move>>& moves,
		const Coordinate from,
		const Coordinate to);
	static std::shared_ptr<Move> get_move(
		const std::vector<std::shared_ptr<Move>>& moves,
		const Coordinate from,
		const Coordinate to);

};
