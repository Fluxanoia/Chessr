#include "chess_engine.hpp"

struct KingInformation
{
	const Coordinate coordinate;
	const FlagBoard move_mask;
	const std::vector<Coordinate> checkers;

	KingInformation(Coordinate coordinate, FlagBoard move_mask, std::vector<Coordinate> checkers)
		: coordinate(coordinate), move_mask(move_mask), checkers(checkers)
	{
	}
};

ChessEngine::ChessEngine(const Grid<Piece>& starting_position, const Player starting_player) : current_player(starting_player)
{
	this->positions.emplace_back(starting_position);
	this->calculate_moves();
}

void ChessEngine::make_move(const Move move)
{
	const auto& current_board = this->positions.back();
	if (!current_board.has_piece(move.get_from()))
	{
		return;
	}

	const auto& piece = current_board.get_piece(move.get_from());

#pragma region Board Modifications

	const auto& [from_i, from_j] = move.get_from();
	const auto& [to_i, to_j] = move.get_to();
	Grid<Piece> position = current_board.get_grid();
	position[to_i][to_j].emplace(piece);
	position[from_i][from_j].reset();

	// TODO: move side-effects

	this->positions.emplace_back(position);
	this->played_moves.push_back(move);
	this->current_player = MoveGenerator::get_opposing_player(current_player);

#pragma endregion

	this->calculate_moves();

	this->game_state = this->current_moves.size() == 0
		? this->currently_in_check ? GameState::CHECKMATE : GameState::STALEMATE
		: this->currently_in_check ? GameState::CHECK : GameState::NONE;

	this->move_history.push_back(get_move_representation(move));
}

std::vector<Move> ChessEngine::get_current_moves() const
{
	return this->current_moves;
}

std::vector<std::string> ChessEngine::get_move_history() const
{
	return this->move_history;
}

GameState ChessEngine::get_game_state() const
{
	return this->game_state;
}

std::string ChessEngine::get_move_representation(const Move move) const
{
	const auto& from = move.get_from();
	const auto& to = move.get_to();
	switch (move.get_property())
	{
		case MoveProperty::CASTLE:
			return from.second - to.second > 0 ? "O-O-O" : "O-O";
	}

	const auto& current_board = this->positions.back();
	if (!current_board.has_piece(from))
	{
		return "-";
	}

	const auto& piece = current_board.get_piece(from);
	const auto& piece_data = PieceConfiguration::get_instance().get_data(piece.get_type());
	const auto attack = current_board.has_piece(to);

	auto destination = get_notation_from_coordinate(to, current_board.get_dimensions().second);

	std::string ambiguity = "";
	bool rank_ambigious = current_board.rank_contains_multiple_of(from.first, piece.get_type(), piece.get_player());
	bool file_ambigious = current_board.file_contains_multiple_of(from.second, piece.get_type(), piece.get_player());
	if (file_ambigious)
	{
		ambiguity += get_file_from_coordinate(from.second);
	}
	if (rank_ambigious)
	{
		ambiguity += get_rank_from_coordinate(from.first, current_board.get_dimensions().second);
	}

	std::string piece_string;
	switch (piece.get_type())
	{
		case PieceType::PAWN:
			piece_string = "";
			file_ambigious = file_ambigious || attack;
			break;
		default:
			piece_string = piece_data.get_representation();
			break;
	}

	std::string capture = attack ? "x" : "";
	std::string suffix = currently_in_check ? current_moves.size() == 0 ? "#" : "+" : "";

	return piece_string + ambiguity + capture + destination;
}

std::string ChessEngine::get_notation_from_coordinate(const Coordinate coordinate, const CoordinateValue board_height)
{
	return get_file_from_coordinate(coordinate.second) + get_rank_from_coordinate(coordinate.first, board_height);
}

std::string ChessEngine::get_file_from_coordinate(CoordinateValue file)
{
	file++;
	std::string repr = "";
	while (file > 0)
	{
		auto r = (file - 1) % 26;
		repr = std::to_string((char)((int)'a' + r)) + repr;
		file = (file - r) / 26;
	}
	return repr;
}

std::string ChessEngine::get_rank_from_coordinate(const CoordinateValue rank, const CoordinateValue board_height)
{
	return std::to_string(board_height - rank);
}

void ChessEngine::calculate_moves()
{
	const auto& board = this->positions.back();
	const auto& [width, height] = board.get_dimensions();
	const auto& piece_configuration = PieceConfiguration::get_instance();

	const auto player = current_player;
	const auto opposing_player = MoveGenerator::get_opposing_player(current_player);

	this->current_moves = std::vector<Move>{};

#pragma region King Information

	auto king_informations = std::vector<KingInformation>{};
	for (auto& coordinate : board.positions_of(PieceType::KING, player))
	{
		king_informations.emplace_back(
			coordinate,
			MoveGenerator::get_king_move_mask(board, player, coordinate),
			MoveGenerator::get_attacking_coordinates(board, player, coordinate));
	}

	std::vector<std::reference_wrapper<const KingInformation>> single_checks = {};
	std::vector<std::reference_wrapper<const KingInformation>> double_checks = {};
	for (const auto& king_information : king_informations)
	{
		switch (king_information.checkers.size())
		{
			case 0:
				break;
			case 1:
				single_checks.push_back(king_information);
				break;
			default:
				double_checks.push_back(king_information);
				break;
		}
	}

	this->currently_in_check = single_checks.size() + double_checks.size() > 0;

#pragma endregion

#pragma region Double Checks

	const auto& king_piece_data = piece_configuration.get_data(PieceType::KING);

	switch (double_checks.size())
	{
		case 0:
			// Continue below.
			break;
		case 1:
		{
			// A king is under double check, so only moves by that king are valid.
			const auto& double_check = double_checks.at(0);
			const auto& double_check_moves = [&board, &player, &king_piece_data, &double_check]()
			{
				auto moves = MoveGenerator::get_valid_moves(
					board,
					player,
					king_piece_data,
					double_check.get().coordinate);
				double_check.get().move_mask.mask(moves);
				return moves;
			}();

			switch (single_checks.size())
			{
				case 0:
				{
					// This king must evade check. Possibly checkmate.
					for (const auto& destination : double_check_moves)
					{
						this->current_moves.emplace_back(double_check.get().coordinate, destination);
					}
					return;
				}
				default:
					// This king must evade check and stop the check on other kings.
					// Since it cannot block check, it must take the piece.
					std::set<Coordinate> other_checkers = {};
					for (const auto& single_check : single_checks)
					{
						for (const auto& checker : single_check.get().checkers)
						{
							other_checkers.insert(checker);
						}
					}

					if (other_checkers.size() > 1)
					{
						// The king can't take more than one piece. Checkmate.
						return;
					}

					const auto& other_checker = *other_checkers.begin();
					auto capturable = std::find(
						double_check_moves.begin(),
						double_check_moves.end(),
						other_checker) != double_check_moves.end();

					if (capturable)
					{
						// We can capture the piece putting the other kings in check.
						this->current_moves.emplace_back(double_check.get().coordinate, other_checker);
					}
					return;
			}
			break;
		}
		default:
			// Two or more kings must both evade check simultaneously, impossible. Checkmate.
			return;
	}

#pragma endregion

#pragma region King Move Aggregation

	for (const auto& king_information : king_informations)
	{
		auto attacks = MoveGenerator::get_valid_attack_moves(
			board,
			player,
			king_piece_data,
			king_information.coordinate);
		auto pushes = MoveGenerator::get_valid_push_moves(
			board,
			player,
			king_piece_data,
			king_information.coordinate);

		king_information.move_mask.mask(attacks);
		king_information.move_mask.mask(pushes);

		for (const auto& attack : attacks)
		{
			this->current_moves.emplace_back(king_information.coordinate, attack);
		}

		for (const auto& push : pushes)
		{
			this->current_moves.emplace_back(king_information.coordinate, push);
		}
	}

#pragma endregion

#pragma region Masking

	std::set<Coordinate> all_checkers = {};
	for (const auto& single_check : single_checks)
	{
		for (const auto& checker : single_check.get().checkers)
		{
			all_checkers.insert(checker);
		}
	}

	FlagBoard attackable = { board.get_dimensions(), true };
	switch (all_checkers.size())
	{
		case 0:
			break;
		case 1:
			// We can only capture the checker, if we choose to attack.
			attackable.restrict({ *all_checkers.begin() });
			break;
		default:
			// We can't take more than one piece at once, so we can't attack.
			attackable.set_all(false);
			break;
	}

	FlagBoard pushable = { board.get_dimensions(), true };
	for (const auto& king_information : king_informations)
	{
		for (const auto& checker : all_checkers)
		{
			auto& piece = board.get_piece(checker);
			const auto blocks = MoveGenerator::get_blocks_to_attack(
				board,
				opposing_player,
				piece_configuration.get_data(piece.get_type()),
				checker,
				king_information.coordinate);
			pushable.restrict(blocks);
		}
	}

#pragma endregion

#pragma region Pin Move Aggregation

	auto pins = MoveGenerator::get_pins(board, player);
	for (auto& pin : pins)
	{
		if (!board.has_piece(pin.get_coordinate()))
		{
			continue;
		}

		const auto& piece = board.get_piece(pin.get_coordinate());
		if (piece.get_player() != player || piece.get_type() == PieceType::KING)
		{
			continue;
		}

		const auto& piece_data = piece_configuration.get_data(piece.get_type());

		auto attacks = MoveGenerator::get_valid_attack_moves(
			board,
			player,
			piece_data,
			pin.get_coordinate());

		auto pushes = MoveGenerator::get_valid_push_moves(
			board,
			player,
			piece_data,
			pin.get_coordinate());

		pin.get_move_mask().mask(attacks);
		pin.get_move_mask().mask(pushes);

		attackable.mask(attacks);
		pushable.mask(pushes);

		for (const auto& attack : attacks)
		{
			this->current_moves.emplace_back(pin.get_coordinate(), attack);
		}

		for (const auto& push : pushes)
		{
			this->current_moves.emplace_back(pin.get_coordinate(), push);
		}
	}

#pragma endregion

#pragma region Final Move Aggregation

	const auto pin_coordinates = [](const std::vector<PinnedPiece>& pins)
	{
		std::vector<Coordinate> coordinates = {};
		for (const auto& pin : pins)
		{
			coordinates.emplace_back(pin.get_coordinate());
		}
		return coordinates;
	}(pins);

	for (auto i = 0; i < height; i++)
	{
		for (auto j = 0; j < width; j++)
		{
			const Coordinate cell = { i, j };
			if (!board.has_piece(cell))
			{
				continue;
			}

			const auto& piece = board.get_piece(cell);
			if (piece.get_player() != player || piece.get_type() == PieceType::KING)
			{
				continue;
			}

			if (std::find(pin_coordinates.begin(), pin_coordinates.end(), cell) != pin_coordinates.end())
			{
				continue;
			}

			const auto& piece_data = piece_configuration.get_data(piece.get_type());

			auto attacks = MoveGenerator::get_valid_attack_moves(
				board,
				player,
				piece_data,
				cell);

			auto pushes = MoveGenerator::get_valid_push_moves(
				board,
				player,
				piece_data,
				cell);

			attackable.mask(attacks);
			pushable.mask(pushes);

			for (const auto& attack : attacks)
			{
				this->current_moves.emplace_back(cell, attack);
			}

			for (const auto& push : pushes)
			{
				this->current_moves.emplace_back(cell, push);
			}
		}
	}

#pragma endregion

}
