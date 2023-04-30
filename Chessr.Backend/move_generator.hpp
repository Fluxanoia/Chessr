#pragma once

#include <vector>
#include <optional>
#include <algorithm>
#include "board.hpp"
#include "flag_board.hpp"
#include "piece_configuration.hpp"

typedef struct _PinnedPiece
{
	const Coordinate& coordinate;
	FlagBoard move_mask;
} PinnedPiece;

class MoveGenerator
{
public:

	static FlagBoard get_king_move_mask(
		const Board& board,
		const Player& player,
		const Coordinate& coordinate);

	static std::vector<Coordinate> get_possible_attacks(
		const Board& board,
		const Player& player,
		const PieceData& piece_data,
		const Coordinate& coordinate,
		const std::optional<Coordinate>& ignore_coordinate);

	static std::vector<Coordinate> get_attacking_coordinates(
		const Board& board,
		const Player& player,
		const Coordinate& coordinate);

	static std::vector<Coordinate> get_valid_push_moves(
		const Board& board,
		const Player& player,
		const PieceData& piece_data,
		const Coordinate& coordinate);

	static std::vector<Coordinate> get_valid_attack_moves(
		const Board& board,
		const Player& player,
		const PieceData& piece_data,
		const Coordinate& coordinate);

	static std::vector<Coordinate> get_valid_moves(
		const Board& board,
		const Player& player,
		const PieceData& piece_data,
		const Coordinate& coordinate);

	static std::vector<Coordinate> get_blocks_to_attack(
		const Board& board,
		const Player& player,
		const PieceData& piece_data,
		const Coordinate& from,
		const Coordinate& to);

	static std::vector<PinnedPiece> get_pins(
		const Board& board,
		const Player& player);

	static inline Player get_opposing_player(const Player& player)
	{
		return player == Player::WHITE ? Player::BLACK : Player::WHITE;
	}

	static std::vector<Coordinate> get_ray(
		const Board& board,
		const Player& player,
		const Coordinate& ray,
		const Coordinate& coordinate,
		const std::optional<Coordinate>& ignore_coordinate,
		const bool attack);

	static std::optional<Coordinate> get_jump(
		const Board& board,
		const Player& player,
		const Coordinate& jump,
		const Coordinate& coordinate,
		const bool attack);

	static std::vector<Coordinate> get_moves(
		const Board& board,
		const Player& player,
		const std::vector<Coordinate>& rays,
		const std::vector<Coordinate>& jumps,
		const Coordinate& coordinate,
		const std::optional<Coordinate>& ignore_coordinate,
		const bool attack);

};
