#pragma once

#include <vector>
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
	/// <param name="board">The board to fetch piece data from.</param>
	/// <param name="player">The player of the king.</param>
	/// <param name="coordinate">The position of the king.</param>
	/// <returns>A flag board representing the squares that the king can move to based on possible enemy attacks.</returns>
	static FlagBoard get_king_move_mask(
		const Board& board,
		const Player& player,
		const Coordinate& coordinate);

	/// <summary>
	/// Calculates the cells that a piece endangers.
	/// </summary>
	/// <param name="board">The board to fetch piece data from.</param>
	/// <param name="player">The player of the piece.</param>
	/// <param name="piece_data">The data of the piece.</param>
	/// <param name="coordinate">The position of the piece.</param>
	/// <param name="ignore_coordinate">A coordinate to ignore for ray calculations.</param>
	/// <returns>The cells that a piece endangers.</returns>
	static std::vector<Coordinate> get_possible_attacks(
		const Board& board,
		const Player& player,
		const PieceData& piece_data,
		const Coordinate& coordinate,
		const std::optional<Coordinate>& ignore_coordinate);

	/// <summary>
	/// Calculates the cells of enemy pieces that are endangering the given coordinate.
	/// </summary>
	/// <param name="board">The board to fetch piece data from.</param>
	/// <param name="player">The player of the piece.</param>
	/// <param name="coordinate">The position of the piece.</param>
	/// <returns>The cells that are endangering the given coordinate.</returns>
	static std::vector<Coordinate> get_attacking_coordinates(
		const Board& board,
		const Player& player,
		const Coordinate& coordinate);

	/// <summary>
	/// Calculates the cells to move to that would block an attack from the given piece.
	/// </summary>
	/// <param name="board">The board to fetch piece data from.</param>
	/// <param name="player">The player of the attacking piece.</param>
	/// <param name="piece_data">The data of the attacking piece.</param>
	/// <param name="from">The position of the attacking piece.</param>
	/// <param name="to">The destination of the attacking piece.</param>
	/// <returns>The cells to move to that would block an attack from the given piece.</returns>
	static std::vector<Coordinate> get_blocks_to_attack(
		const Board& board,
		const Player& player,
		const PieceData& piece_data,
		const Coordinate& from,
		const Coordinate& to);

	/// <summary>
	/// Calculates the pinned pieces on the board.
	/// </summary>
	/// <param name="board">The board to fetch piece data from.</param>
	/// <param name="player">The player to calculate the pins for.</param>
	/// <returns>The pinned pieces on the board.</returns>
	static std::vector<PinnedPiece> get_pins(
		const Board& board,
		const Player& player);

#pragma endregion

#pragma region Valid Move Calculations

	/// <summary>
	/// Calculates the valid push moves for a given piece.
	/// </summary>
	/// <param name="board">The board to fetch piece data from.</param>
	/// <param name="player">The player of the piece.</param>
	/// <param name="piece_data">The data of the piece.</param>
	/// <param name="coordinate">The position of the piece.</param>
	/// <returns>The valid push moves for a given piece.</returns>
	static std::vector<Coordinate> get_valid_push_moves(
		const Board& board,
		const Player& player,
		const PieceData& piece_data,
		const Coordinate& coordinate);

	/// <summary>
	/// Calculates the valid attack moves for a given piece.
	/// </summary>
	/// <param name="board">The board to fetch piece data from.</param>
	/// <param name="player">The player of the piece.</param>
	/// <param name="piece_data">The data of the piece.</param>
	/// <param name="coordinate">The position of the piece.</param>
	/// <returns>The valid attack moves for a given piece.</returns>
	static std::vector<Coordinate> get_valid_attack_moves(
		const Board& board,
		const Player& player,
		const PieceData& piece_data,
		const Coordinate& coordinate);

	/// <summary>
	/// Calculates the valid moves for a given piece.
	/// </summary>
	/// <param name="board">The board to fetch piece data from.</param>
	/// <param name="player">The player of the piece.</param>
	/// <param name="piece_data">The data of the piece.</param>
	/// <param name="coordinate">The position of the piece.</param>
	/// <returns>The valid moves for a given piece.</returns>
	static std::vector<Coordinate> get_valid_moves(
		const Board& board,
		const Player& player,
		const PieceData& piece_data,
		const Coordinate& coordinate);

#pragma endregion

#pragma region Fundamental Calculations

	/// <summary>
	/// Returns the possible moves for the given rays and jumps.
	/// </summary>
	/// <param name="board">The board to fetch piece data from.</param>
	/// <param name="player">The player of the piece.</param>
	/// <param name="rays">The vectors representing the rays.</param>
	/// <param name="jumps">The vectors representing the jumps.</param>
	/// <param name="coordinate">The position of the piece.</param>
	/// <param name="ignore_coordinate">A coordinate to ignore for ray calculations.</param>
	/// <param name="attack">Whether this is an attack or a push move.</param>
	/// <returns>The cells that the piece can move to for the given rays and jumps.</returns>
	static std::vector<Coordinate> get_moves(
		const Board& board,
		const Player& player,
		const std::vector<Coordinate>& rays,
		const std::vector<Coordinate>& jumps,
		const Coordinate& coordinate,
		const std::optional<Coordinate>& ignore_coordinate,
		const bool attack);

	/// <summary>
	/// Calculates the result of a ray move.
	/// </summary>
	/// <param name="board">The board to fetch piece data from.</param>
	/// <param name="player">The player of the piece.</param>
	/// <param name="ray">The vector representing the ray.</param>
	/// <param name="coordinate">The position of the piece.</param>
	/// <param name="ignore_coordinate">A coordinate to ignore pieces on.</param>
	/// <param name="attack">Whether this is an attack or a push move.</param>
	/// <returns>The cells that the piece can move to along the ray.</returns>
	static std::vector<Coordinate> get_ray(
		const Board& board,
		const Player& player,
		const Coordinate& ray,
		const Coordinate& coordinate,
		const std::optional<Coordinate>& ignore_coordinate,
		const bool attack);

	/// <summary>
	/// Calculates the result of a jump move.
	/// </summary>
	/// <param name="board">The board to fetch piece data from.</param>
	/// <param name="player">The player of the piece.</param>
	/// <param name="jump">The vector representing the jump.</param>
	/// <param name="coordinate">The position of the piece.</param>
	/// <param name="attack">Whether this is an attack or a push move.</param>
	/// <returns>The resultant cell or an empty optional if the move isn't possible.</returns>
	static std::optional<Coordinate> get_jump(
		const Board& board,
		const Player& player,
		const Coordinate& jump,
		const Coordinate& coordinate,
		const bool attack);

#pragma endregion

#pragma region Helpers

	/// <summary>
	/// Calculates the opposing player.
	/// </summary>
	/// <param name="player">The player to calculate from.</param>
	/// <returns>The opposing player.</returns>
	static inline Player get_opposing_player(const Player& player)
	{
		return player == Player::WHITE ? Player::BLACK : Player::WHITE;
	}

#pragma endregion

};
