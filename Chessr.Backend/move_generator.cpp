#include "move_generator.hpp"

#pragma region Endangerment, Blocking, and Pinning

std::shared_ptr<FlagBoard> MoveGenerator::get_king_move_mask(
	const Boards& boards,
	const PieceConfiguration& piece_configuration,
	const Player& player,
	const Coordinate& coordinate)
{
	const auto& board = boards.get_current_board();
	auto king_move_mask = std::make_shared<FlagBoard>(board.get_dimensions(), true);

	const auto& [width, height] = board.get_dimensions();
	const auto opposing_player = Maths::get_opposing_player(player);
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
				boards,
				opposing_player,
				piece_configuration.get_data(piece.get_type()),
				cell,
				coordinate);

			king_move_mask->unflag(possible_attacks);
		}
	}

	return king_move_mask;
}

std::vector<Coordinate> MoveGenerator::get_possible_attacks(
	const Boards& boards,
	const Player& player,
	const PieceData& piece_data,
	const Coordinate& coordinate,
	const std::optional<Coordinate>& ignore_coordinate)
{
	const auto moves = piece_data.get_moves(boards, player, coordinate, MoveType::ATTACK, MoveStyle::ALL, ignore_coordinate);

	std::vector<Coordinate> coordinates = {};
	for (const auto& move : moves)
	for (const auto& consequence : move->get_consequences())
	{
		if (consequence->get_type() != ConsequenceType::REMOVE)
		{
			continue;
		}
		const auto& remove_consequence = std::dynamic_pointer_cast<RemoveConsequence>(consequence);
		if (remove_consequence == nullptr)
		{
			continue;
		}
		coordinates.push_back(remove_consequence->get_coordinate());
	}
	return coordinates;
}

std::vector<Coordinate> MoveGenerator::get_attacking_coordinates(
	const Boards& boards,
	const PieceConfiguration& piece_configuration,
	const Player& player,
	const Coordinate& coordinate)
{
	const auto& board = boards.get_current_board();
	const auto& [width, height] = board.get_dimensions();
	const auto opposing_player = Maths::get_opposing_player(player);

	std::vector<Coordinate> attacking_cells = {};
	for (auto i = 0; i < height; i++)
	for (auto j = 0; j < width; j++)
	{
		const Coordinate cell = { i, j };
		if (!board.has_piece(cell))
		{
			continue;
		}

		const auto& piece = board.get_piece(cell);
		if (piece.get_player() == player)
		{
			continue;
		}

		const auto& piece_data = piece_configuration.get_data(piece.get_type());
		auto moves = piece_data.get_moves(
			boards,
			opposing_player,
			cell,
			MoveType::ATTACK,
			MoveStyle::ALL,
			{});

		for (const auto& move : moves)
		{
			if (!move->is_attacking(coordinate))
			{
				continue;
			}

			attacking_cells.push_back(cell);
			break;
		}
	}

	return attacking_cells;
}

std::vector<Coordinate> MoveGenerator::get_blocks_to_attack(
	const Boards& boards,
	const Player& player,
	const PieceData& piece_data,
	const Coordinate& from,
	const Coordinate& to)
{
	for (auto& jump : piece_data.get_moves(boards, player, from, MoveType::ATTACK, MoveStyle::JUMP, {}))
	{
		if (jump->is_attacking(to))
		{
			// We can't block jumps.
			return {};
		}
	}

	for (auto& ray : piece_data.get_moves(boards, player, from, MoveType::ATTACK, MoveStyle::RAY, {}))
	{
		const auto& move_consequence = ray->get_move_consequence();
		if (!move_consequence.has_value())
		{
			continue;
		}

		auto cells = piece_data.get_ray(
			boards,
			player,
			move_consequence.value()->get_move_vector(),
			from,
			{},
			true);

		if (cells.size() > 0 && cells.back() == to)
		{
			cells.pop_back();
			return cells;
		}
	}

	throw InvalidOperationException("Unable to calculate blocks for an attack that can't land.");
}

std::vector<PinnedPiece> MoveGenerator::get_pins(
	const Boards& boards,
	const PieceConfiguration& piece_configuration,
	const Player& player)
{
	const auto& board = boards.get_current_board();
	const auto opposing_player = Maths::get_opposing_player(player);
	const auto king_positions = board.positions_of(PieceType::KING, player);

	std::vector<PinnedPiece> pinned_pieces = {};
	for (const auto& piece_type : piece_configuration.get_piece_types())
	{
		const auto& piece_data = piece_configuration.get_data(piece_type);

		for (const auto& king_position : king_positions)
		for (const auto& coordinate : board.positions_of(piece_type, opposing_player))
		for (const auto& move : piece_data.get_moves(boards, opposing_player, coordinate, MoveType::ATTACK, MoveStyle::RAY, {}))
		{
			const auto& move_consequence = move->get_move_consequence();
			if (!move_consequence.has_value())
			{
				continue;
			}

			const auto& pin_coordinate = move_consequence.value()->get_to();
			if (!board.has_piece(pin_coordinate) || board.get_piece(pin_coordinate).get_player() != player)
			{
				continue;
			}

			auto possible_destinations = piece_data.get_ray(
				boards,
				opposing_player,
				move_consequence.value()->get_move_vector(),
				coordinate,
				pin_coordinate,
				true);

			if (possible_destinations.back() != king_position)
			{
				continue;
			}

			possible_destinations.pop_back();
			possible_destinations.push_back(coordinate);

			const auto existing_pin = std::find_if(
				pinned_pieces.begin(),
				pinned_pieces.end(),
				[&pin_coordinate](const PinnedPiece& piece) { return piece.get_coordinate() == pin_coordinate; });

			if (existing_pin == pinned_pieces.end())
			{
				PinnedPiece pinned_piece = {
					pin_coordinate,
					std::make_shared<FlagBoard>(board.get_dimensions(), true)
				};
				pinned_piece.get_move_mask()->restrict(possible_destinations);
				pinned_pieces.push_back(pinned_piece);
			}
			else
			{
				existing_pin->get_move_mask()->restrict(possible_destinations);
			}
		}
	}

	return pinned_pieces;
}

#pragma endregion

#pragma region Valid Move Calculations

std::vector<std::shared_ptr<Move>> MoveGenerator::get_valid_attack_moves(
	const Boards& boards,
	const Player& player,
	const PieceData& piece_data,
	const Coordinate& coordinate)
{
	const auto& board = boards.get_current_board();
	auto moves = piece_data.get_moves(boards, player, coordinate, MoveType::ATTACK, MoveStyle::ALL, {});

	auto it = moves.begin();
	while (it != moves.end())
	{
		auto valid = true;
		const auto& move = *it;
		for (const auto& consequence : move->get_consequences())
		{
			if (consequence->get_type() != ConsequenceType::REMOVE)
			{
				continue;
			}
			const auto& remove_consequence = std::dynamic_pointer_cast<RemoveConsequence>(consequence);
			if (remove_consequence == nullptr)
			{
				continue;
			}
			const auto& remove_coordinate = remove_consequence->get_coordinate();
			if (!board.has_piece(remove_coordinate) || board.get_piece(remove_coordinate).get_player() == player)
			{
				valid = false;
				break;
			}
		}

		if (valid)
		{
			it++;
		}
		else
		{
			it = moves.erase(it);
		}
	}

	return moves;
}

std::vector<std::shared_ptr<Move>> MoveGenerator::get_valid_push_moves(
	const Boards& boards,
	const Player& player,
	const PieceData& piece_data,
	const Coordinate& coordinate)
{
	return piece_data.get_moves(boards, player, coordinate, MoveType::PUSH, MoveStyle::ALL, {});
}

std::vector<std::shared_ptr<Move>> MoveGenerator::get_valid_moves(
	const Boards& boards,
	const Player& player,
	const PieceData& piece_data,
	const Coordinate& coordinate)
{
	auto moves = get_valid_push_moves(boards, player, piece_data, coordinate);
	auto attacks = get_valid_attack_moves(boards, player, piece_data, coordinate);
	moves.insert(moves.end(), attacks.begin(), attacks.end());
	return moves;
}

#pragma endregion
