#include "move_generator.hpp"

std::vector<Coordinate> MoveGenerator::get_attacks(
	const Board& board,
	const Player& player,
	const PieceData& piece_data,
	const Coordinate& coordinate,
	const std::optional<Coordinate>& ignore_coordinate,
	const bool ignore_pieces,
	const bool reverse_rays)
{
	auto& rays = piece_data.get_attack_rays(player, reverse_rays);
	auto& jumps = piece_data.get_attack_jumps(player, reverse_rays);
	return get_moves(board, player, rays, jumps, coordinate, ignore_coordinate, ignore_pieces);
}

std::vector<Coordinate> MoveGenerator::get_pushes(
	const Board& board,
	const Player& player,
	const PieceData& piece_data,
	const Coordinate& coordinate)
{
	auto& rays = piece_data.get_push_rays(player, false);
	auto& jumps = piece_data.get_push_jumps(player, false);
	return get_moves(board, player, rays, jumps, coordinate, std::optional<Coordinate>(), false);
}

std::vector<Coordinate> MoveGenerator::get_moves(
	const Board& board,
	const Player& player,
	const std::vector<Coordinate>& rays,
	const std::vector<Coordinate>& jumps,
	const Coordinate& coordinate,
	const std::optional<Coordinate>& ignore_coordinate,
	const bool ignore_pieces)
{
	std::vector<Coordinate> cells = {};
	for (auto& ray : rays)
	{
		auto cells = get_ray(board, player, ray, coordinate, ignore_coordinate, ignore_pieces);
		cells.insert(cells.end(), cells.begin(), cells.end());
	}

	for (auto& jump : jumps)
	{
		auto cell = get_jump(board, player, jump, coordinate, ignore_pieces);
		if (cell.has_value())
		{
			cells.push_back(cell.value());
		}
	}

	return cells;
}

std::vector<Coordinate> MoveGenerator::get_all_moves(
	const Board& board,
	const Player& player,
	const PieceData& piece_data,
	const Coordinate& coordinate)
{
	auto pushes = get_pushes(board, player, piece_data, coordinate);
	auto attacks = get_attacks(board, player, piece_data, coordinate, std::optional<Coordinate>(), false, false);

	for (const auto& attack : attacks)
	{
		if (!board.has_piece(attack))
		{
			continue;
		}

		const auto& piece = board.get_piece(attack);
		if (piece.get_player() != player)
		{
			pushes.push_back(attack);
		}
	}

	return pushes;
}

std::vector<Coordinate> MoveGenerator::get_ray(
	const Board& board,
	const Player& player,
	const Coordinate& ray,
	const Coordinate& coordinate,
	const std::optional<Coordinate>& ignore_coordinate,
	const bool ignore_pieces)
{
	std::vector<Coordinate> cells = {};

	auto cell = add_coordinates(coordinate, ray);
	while (in_bounds(board.get_dimensions(), cell))
	{
		const auto& [i, j] = cell;
		auto ignore = ignore_pieces || (ignore_coordinate.has_value() && ignore_coordinate.value() == cell);

		if (ignore || !board.has_piece(cell))
		{
			cells.push_back(cell);
		}
		else
		{
			auto& piece = board.get_piece(cell);
			if (piece.get_player() != player)
			{
				cells.push_back(cell);
			}

			break;
		}

		cell = add_coordinates(cell, ray);
	}

	return cells;
}

std::optional<Coordinate> MoveGenerator::get_jump(
	const Board& board,
	const Player& player,
	const Coordinate& jump,
	const Coordinate& coordinate,
	const bool ignore_pieces)
{
	auto cell = add_coordinates(coordinate, jump);
	if (!in_bounds(board.get_dimensions(), cell))
	{
		return std::optional<Coordinate>();
	}

	if (ignore_pieces || (!board.has_piece(cell) || board.get_piece(cell).get_player() != player))
	{
		return cell;
	}

	return std::optional<Coordinate>();
}
