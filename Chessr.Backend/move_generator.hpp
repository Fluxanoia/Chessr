#pragma once

#include <vector>
#include <memory>
#include <optional>
#include <algorithm>
#include "board.hpp"
#include "flag_board.hpp"
#include "pinned_piece.hpp"
#include "piece_configuration.hpp"

class MoveGenerator
{
public:

#pragma region Endangerment, Blocking, and Pinning

	/// <summary>
	/// Calculates a flag board representing the squares that the king can move to based on possible enemy attacks.
	/// </summary>
	static std::shared_ptr<FlagBoard> get_king_move_mask(
		const Boards& boards,
		const Player& player,
		const Coordinate& coordinate);

	/// <summary>
	/// Calculates the cells that a piece endangers.
	/// </summary>
	static std::vector<Coordinate> get_possible_attacks(
		const Boards& boards,
		const Player& player,
		const PieceData& piece_data,
		const Coordinate& coordinate,
		const std::optional<Coordinate>& ignore_coordinate);

	/// <summary>
	/// Calculates the cells of enemy pieces that are endangering the given coordinate.
	/// </summary>
	static std::vector<Coordinate> get_attacking_coordinates(
		const Boards& boards,
		const Player& player,
		const Coordinate& coordinate);

	/// <summary>
	/// Calculates the cells to move to that would block an attack from the given piece.
	/// </summary>
	static std::vector<Coordinate> get_blocks_to_attack(
		const Boards& boards,
		const Player& player,
		const PieceData& piece_data,
		const Coordinate& from,
		const Coordinate& to);

	/// <summary>
	/// Calculates the pinned pieces on the board.
	/// </summary>
	static std::vector<PinnedPiece> get_pins(
		const Boards& boards,
		const Player& player);

#pragma endregion

#pragma region Valid Move Calculations

	/// <summary>
	/// Calculates the valid push moves for a given piece.
	/// </summary>
	static std::vector<std::shared_ptr<Move>> get_valid_push_moves(
		const Boards& boards,
		const Player& player,
		const PieceData& piece_data,
		const Coordinate& coordinate);

	/// <summary>
	/// Calculates the valid attack moves for a given piece.
	/// </summary>
	static std::vector<std::shared_ptr<Move>> get_valid_attack_moves(
		const Boards& boards,
		const Player& player,
		const PieceData& piece_data,
		const Coordinate& coordinate);

	/// <summary>
	/// Calculates the valid moves for a given piece.
	/// </summary>
	static std::vector<std::shared_ptr<Move>> get_valid_moves(
		const Boards& boards,
		const Player& player,
		const PieceData& piece_data,
		const Coordinate& coordinate);

#pragma endregion

};
