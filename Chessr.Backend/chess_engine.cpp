#include "chess_engine.hpp"

namespace py = pybind11;

#pragma region Constructor

ChessEngine::ChessEngine(PieceConfiguration& piece_configuration) : piece_configuration(piece_configuration)
{
}

#pragma endregion

#pragma region Public Move Logic

void ChessEngine::start(
	const Grid<Piece>& starting_position,
	const Player starting_player)
{
	state = State::NONE;
	current_moves = {};
	move_history = {};

	boards = Boards(starting_position, starting_player);
	this->calculate_moves();
}

std::vector<std::shared_ptr<Consequence>> ChessEngine::make_move(const std::shared_ptr<Move> move)
{
	if (!this->boards.has_value())
	{
		return {};
	}

	this->boards.value().apply_move(move);

	this->calculate_moves();

	const auto& board = boards.value().get_current_board();
	this->state = this->current_moves.size() == 0
		? board.is_in_check() ? State::CHECKMATE : State::STALEMATE
		: board.is_in_check() ? State::CHECK : State::NONE;
	this->move_history.push_back(get_move_representation(move));

	return move->get_consequences();
}

#pragma endregion

#pragma region Private Move Logic

void ChessEngine::calculate_moves()
{
	if (!this->boards.has_value())
	{
		return;
	}

	if (!require_gil)
	{
		py::gil_scoped_release release;
	}

	auto& board = boards.value().get_current_board();
	const auto& player = boards.value().get_current_player();
	const auto& [width, height] = board.get_dimensions();

	const auto opposing_player = Maths::get_opposing_player(player);

	this->current_moves = {};

#pragma region King Information

	auto king_informations = std::vector<KingInformation>{};
	for (auto& coordinate : board.positions_of(PieceType::KING, player))
	{
		king_informations.emplace_back(
			coordinate,
			MoveGenerator::get_king_move_mask(
				boards.value(), piece_configuration, player, coordinate),
			MoveGenerator::get_attacking_coordinates(
				boards.value(), piece_configuration, player, coordinate));
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

	if (single_checks.size() + double_checks.size() > 0)
	{
		board.set_in_check();
	}

#pragma endregion

#pragma region Double Checks

	const auto& king_piece_data = piece_configuration.get_piece_data(PieceType::KING);

	switch (double_checks.size())
	{
		case 0:
			// Continue below.
			break;
		case 1:
		{
			// A king is under double check, so only moves by that king are valid.
			const auto& double_check = double_checks.at(0);
			auto moves = MoveGenerator::get_valid_moves(
				boards.value(),
				player,
				king_piece_data,
				double_check.get().coordinate);

			double_check.get().move_mask->mask(moves);

			switch (single_checks.size())
			{
				case 0:
				{
					// This king must evade check. Possibly checkmate.
					this->current_moves = moves;
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
					
					FlagBoard flag_board = { board.get_dimensions() };
					flag_board.flag(other_checker);
					flag_board.mask(moves);

					this->current_moves = moves;
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
			boards.value(),
			player,
			king_piece_data,
			king_information.coordinate);
		auto pushes = MoveGenerator::get_valid_push_moves(
			boards.value(),
			player,
			king_piece_data,
			king_information.coordinate);

		king_information.move_mask->mask(attacks);
		king_information.move_mask->mask(pushes);

		for (const auto& attack : attacks)
		{
			this->current_moves.push_back(attack);
		}

		for (const auto& push : pushes)
		{
			this->current_moves.push_back(push);
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
				boards.value(),
				opposing_player,
				piece_configuration.get_piece_data(piece.get_type()),
				checker,
				king_information.coordinate);
			pushable.restrict(blocks);
		}
	}

#pragma endregion

#pragma region Pin Move Aggregation

	auto pins = MoveGenerator::get_pins(boards.value(), piece_configuration, player);
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

		const auto piece_data = piece_configuration.get_piece_data(piece.get_type());

		auto attacks = MoveGenerator::get_valid_attack_moves(
			boards.value(),
			player,
			piece_data,
			pin.get_coordinate());

		auto pushes = MoveGenerator::get_valid_push_moves(
			boards.value(),
			player,
			piece_data,
			pin.get_coordinate());

		pin.get_move_mask()->mask(attacks);
		pin.get_move_mask()->mask(pushes);

		attackable.mask(attacks);
		pushable.mask(pushes);

		for (const auto& attack : attacks)
		{
			this->current_moves.push_back(attack);
		}

		for (const auto& push : pushes)
		{
			this->current_moves.push_back(push);
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

			const auto& piece_data = piece_configuration.get_piece_data(piece.get_type());

			auto attacks = MoveGenerator::get_valid_attack_moves(
				boards.value(),
				player,
				piece_data,
				cell);

			auto pushes = MoveGenerator::get_valid_push_moves(
				boards.value(),
				player,
				piece_data,
				cell);

			attackable.mask(attacks);
			pushable.mask(pushes);

			for (const auto& attack : attacks)
			{
				this->current_moves.push_back(attack);
			}

			for (const auto& push : pushes)
			{
				this->current_moves.push_back(push);
			}
		}
	}

#pragma endregion

}

std::string ChessEngine::get_move_representation(const std::shared_ptr<Move> move)
{
	if (!this->boards.has_value())
	{
		throw InvalidOperationException("Unexpecting missing boards.");
	}

	const auto move_consequence = move->get_move_consequence();
	if (!move_consequence.has_value())
	{
		return "-";
	}

	const auto& from = move_consequence.value()->get_from();
	const auto& to = move_consequence.value()->get_to();
	switch (move->get_property())
	{
		case MoveProperty::CASTLE:
			return from.second - to.second > 0 ? "O-O-O" : "O-O";
	}

	const auto& current_board = boards.value().get_previous_board();
	if (!current_board.has_piece(from))
	{
		return "-";
	}

	const auto& piece = current_board.get_piece(from);
	const auto& piece_data = piece_configuration.get_piece_data(piece.get_type());
	const auto attack = move->attacks();

	auto destination = piece_configuration.get_notation_from_coordinate(to, current_board.get_dimensions().second);

	std::string ambiguity = "";
	bool rank_ambigious = current_board.rank_contains_multiple_of(from.first, piece.get_type(), piece.get_player());
	bool file_ambigious = current_board.file_contains_multiple_of(from.second, piece.get_type(), piece.get_player());
	if (file_ambigious)
	{
		ambiguity += piece_configuration.get_file_from_coordinate(from.second);
	}
	if (rank_ambigious)
	{
		ambiguity += piece_configuration.get_rank_from_coordinate(from.first, current_board.get_dimensions().second);
	}

	std::string piece_string;
	switch (piece.get_type())
	{
		case PieceType::PAWN:
			piece_string = "";
			file_ambigious = file_ambigious || attack;
			break;
		default:
			piece_string = piece_data->get_representation();
			break;
	}

	std::string capture = attack ? "x" : "";
	std::string suffix = state == State::CHECK ? "+" : state == State::CHECKMATE ? "#" : "";

	return piece_string + ambiguity + capture + destination;
}

#pragma endregion

#pragma region Getters

std::vector<std::shared_ptr<Move>> ChessEngine::get_current_moves() const
{
	return this->current_moves;
}

const PieceConfiguration& ChessEngine::get_piece_configuration() const
{
	return this->piece_configuration;
}

std::vector<std::string> ChessEngine::get_move_history() const
{
	return this->move_history;
}

State ChessEngine::get_state() const
{
	return this->state;
}

Player ChessEngine::get_current_player() const
{
	if (!this->boards.has_value())
	{
		throw InvalidOperationException("Unexpecting missing boards.");
	}
	return this->boards.value().get_current_player();
}

#pragma endregion

void ChessEngine::do_not_release_gil()
{
	require_gil = true;
}
