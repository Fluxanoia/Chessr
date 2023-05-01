#include "move_generator.hpp"

#pragma region Endangerment, Blocking, and Pinning

FlagBoard MoveGenerator::get_king_move_mask(
	const Board& board,
	const Player& player,
	const Coordinate& coordinate)
{
	FlagBoard king_move_mask = { board.get_dimensions(), true };

	const auto& [width, height] = board.get_dimensions();
	const auto& piece_configuration = PieceConfiguration::get_instance();
	const auto opposing_player = MoveGenerator::get_opposing_player(player);
	for (auto i = 0; i < height; i++)
	{
		for (auto j = 0; j < width; j++)
		{
			Coordinate cell = { i, j };
			if (!board.has_piece(cell))
			{
				continue;
			}

			auto& piece = board.get_piece(cell);
			if (piece.get_player() != opposing_player)
			{
				continue;
			}

			auto possible_attacks = MoveGenerator::get_possible_attacks(
				board,
				opposing_player,
				piece_configuration.get_data(piece.get_type()),
				cell,
				coordinate);

			king_move_mask.unflag(possible_attacks);
		}
	}

	return king_move_mask;
}

std::vector<Coordinate> MoveGenerator::get_possible_attacks(
	const Board& board,
	const Player& player,
	const PieceData& piece_data,
	const Coordinate& coordinate,
	const std::optional<Coordinate>& ignore_coordinate)
{
	auto& rays = piece_data.get_attack_rays(player);
	auto& jumps = piece_data.get_attack_jumps(player);
	return get_moves(board, player, rays, jumps, coordinate, ignore_coordinate, true);
}

std::vector<Coordinate> MoveGenerator::get_attacking_coordinates(
	const Board& board,
	const Player& player,
	const Coordinate& coordinate)
{
	auto& piece_configuration = PieceConfiguration::get_instance();
	const auto opposing_player = get_opposing_player(player);

	std::vector<Coordinate> attacking_cells = {};
	for (auto& piece_type : piece_configuration.get_piece_types())
	{
		const auto& piece_data = piece_configuration.get_data(piece_type);
		auto& rays = piece_data.get_attack_rays(player, true);
		auto& jumps = piece_data.get_attack_jumps(player, true);
		auto possible_attacking_cells = get_moves(
			board,
			player,
			rays,
			jumps,
			coordinate,
			{},
			true);

		for (auto& cell : possible_attacking_cells)
		{
			if (!board.has_piece(cell))
			{
				continue;
			}

			auto& piece = board.get_piece(cell);
			if (piece.get_player() == opposing_player && piece.get_type() == piece_type)
			{
				attacking_cells.push_back(cell);
			}
		}
	}

	return attacking_cells;
}

std::vector<Coordinate> MoveGenerator::get_blocks_to_attack(
	const Board& board,
	const Player& player,
	const PieceData& piece_data,
	const Coordinate& from,
	const Coordinate& to)
{
	for (auto& ray : piece_data.get_attack_rays(player))
	{
		auto cells = get_ray(board, player, ray, from, {}, true);
		if (cells.size() > 0 && cells.back() == to)
		{
			cells.pop_back();
			return cells;
		}
	}
	return {};
}

std::vector<PinnedPiece> MoveGenerator::get_pins(
	const Board& board,
	const Player& player)
{
	auto& piece_configuration = PieceConfiguration::get_instance();
	const auto opposing_player = get_opposing_player(player);
	const auto king_positions = board.positions_of(PieceType::KING, opposing_player);

	std::vector<PinnedPiece> pinned_pieces = {};
	for (const auto& piece_type : piece_configuration.get_piece_types())
	{
		const auto& piece_data = piece_configuration.get_data(piece_type);
		auto& rays = piece_data.get_attack_rays(player);
		auto& reverse_rays = piece_data.get_attack_rays(player, true);

		for (const auto& king_position : king_positions)
		for (const auto& coordinate : board.positions_of(piece_type, opposing_player))
		for (auto i = 0; i < rays.size(); i++)
		{
			auto outgoing = get_ray(board, opposing_player, rays[i], coordinate, {}, true);
			auto incoming = get_ray(board, opposing_player, reverse_rays[i], king_position, {}, true);
			if (outgoing.size() == 0 || incoming.size() == 0 || outgoing.back() != incoming.back())
			{
				continue;
			}

			const auto& pin_coordinate = outgoing.back();
			if (!board.has_piece(pin_coordinate) || board.get_piece(pin_coordinate).get_player() != player)
			{
				continue;
			}

			auto& possible_moves = outgoing;
			possible_moves.insert(outgoing.end(), incoming.begin(), incoming.end());
			possible_moves.push_back(coordinate);

			auto found = false;
			for (auto& pinned_piece : pinned_pieces)
			{
				if (pinned_piece.get_coordinate() == pin_coordinate)
				{
					found = true;
					pinned_piece.get_move_mask().restrict(possible_moves);
					break;
				}
			}

			if (!found)
			{
				FlagBoard move_mask = { board.get_dimensions(), true };
				move_mask.restrict(possible_moves);
				pinned_pieces.emplace_back(pin_coordinate, move_mask);
			}
		}
	}

	return pinned_pieces;
}

#pragma endregion

#pragma region Valid Move Calculations

std::vector<Coordinate> MoveGenerator::get_valid_attack_moves(
	const Board& board,
	const Player& player,
	const PieceData& piece_data,
	const Coordinate& coordinate)
{
	auto& rays = piece_data.get_attack_rays(player);
	auto& jumps = piece_data.get_attack_jumps(player);
	auto attacks = get_moves(board, player, rays, jumps, coordinate, {}, true);

	auto it = attacks.begin();
	while (it != attacks.end())
	{
		const auto& attack = *it;
		if (board.has_piece(attack) && board.get_piece(attack).get_player() != player)
		{
			it++;
		}
		else
		{
			it = attacks.erase(it);
		}
	}

	return attacks;
}

std::vector<Coordinate> MoveGenerator::get_valid_push_moves(
	const Board& board,
	const Player& player,
	const PieceData& piece_data,
	const Coordinate& coordinate)
{
	auto& rays = piece_data.get_push_rays(player);
	auto& jumps = piece_data.get_push_jumps(player);
	return get_moves(board, player, rays, jumps, coordinate, {}, false);
}

std::vector<Coordinate> MoveGenerator::get_valid_moves(
	const Board& board,
	const Player& player,
	const PieceData& piece_data,
	const Coordinate& coordinate)
{
	auto moves = get_valid_push_moves(board, player, piece_data, coordinate);
	auto attacks = get_valid_attack_moves(board, player, piece_data, coordinate);
	moves.insert(moves.end(), attacks.begin(), attacks.end());
	return moves;
}

#pragma endregion

#pragma region Fundamental Calculations

std::vector<Coordinate> MoveGenerator::get_ray(
	const Board& board,
	const Player& player,
	const Coordinate& ray,
	const Coordinate& coordinate,
	const std::optional<Coordinate>& ignore_coordinate,
	const bool attack)
{
	std::vector<Coordinate> cells = {};

	auto cell = add_coordinates(coordinate, ray);
	while (in_bounds(board.get_dimensions(), cell))
	{
		const auto& [i, j] = cell;
		auto ignore = ignore_coordinate.has_value() && ignore_coordinate.value() == cell;

		if (ignore || !board.has_piece(cell))
		{
			cells.emplace_back(i, j);
		}
		else
		{
			if (attack && board.get_piece(cell).get_player() != player)
			{
				cells.emplace_back(i, j);
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
	const bool attack)
{
	auto cell = add_coordinates(coordinate, jump);
	if (!in_bounds(board.get_dimensions(), cell))
	{
		return {};
	}

	if (!board.has_piece(cell))
	{
		return cell;
	}

	if (attack && board.get_piece(cell).get_player() != player)
	{
		return cell;
	}

	return {};
}

std::vector<Coordinate> MoveGenerator::get_moves(
	const Board& board,
	const Player& player,
	const std::vector<Coordinate>& rays,
	const std::vector<Coordinate>& jumps,
	const Coordinate& coordinate,
	const std::optional<Coordinate>& ignore_coordinate,
	const bool attack)
{
	std::vector<Coordinate> cells = {};
	for (auto& ray : rays)
	{
		for (auto& cell : get_ray(board, player, ray, coordinate, ignore_coordinate, attack))
		{
			cells.push_back(cell);
		}
	}

	for (auto& jump : jumps)
	{
		auto cell = get_jump(board, player, jump, coordinate, attack);
		if (cell.has_value())
		{
			cells.push_back(cell.value());
		}
	}

	return cells;
}

#pragma endregion
