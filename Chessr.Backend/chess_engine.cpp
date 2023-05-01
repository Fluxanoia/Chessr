#include "chess_engine.hpp"

ChessEngine::ChessEngine(const Grid<Piece>& starting_position) {
	this->positions.emplace_back(starting_position);
}

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

const std::vector<Move> ChessEngine::get_moves(const Player player) const {
	const auto& board = this->positions.back();
	const auto& [width, height] = board.get_dimensions();
	const auto& piece_configuration = PieceConfiguration::get_instance();
	const auto opposing_player = MoveGenerator::get_opposing_player(player);

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
			const auto& double_check_moves = double_check.get().move_mask.mask(
				MoveGenerator::get_valid_moves(
					board,
					player,
					king_piece_data,
					double_check.get().coordinate));

			switch (single_checks.size())
			{
				case 0:
				{
					// This king must evade check. Possibly checkmate.
					std::vector<Move> moves = {};
					for (const auto& destination : double_check_moves)
					{
						moves.emplace_back(double_check.get().coordinate, destination);
					}
					return moves;
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
						return {};
					}

					const auto& other_checker = *other_checkers.begin();
					auto capturable = std::find(
						double_check_moves.begin(),
						double_check_moves.end(),
						other_checker) != double_check_moves.end();

					if (capturable)
					{
						// We can capture the piece putting the other kings in check.
						return std::vector<Move>{ { double_check.get().coordinate, other_checker } };
					}
					else
					{
						// We cannot capture the piece putting the other kings in check. Checkmate.
						return {};
					}
			}
			break;
		}
		default:
			// Two or more kings must both evade check simultaneously, impossible. Checkmate.
			return {};
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

	std::vector<Move> moves = {};

#pragma region King Move Aggregation

	for (const auto& king_information : king_informations)
	{
		const auto& attacks = attackable.mask(
			king_information.move_mask.mask(
				MoveGenerator::get_valid_attack_moves(
					board,
					player,
					king_piece_data,
					king_information.coordinate)));

		const auto& pushes = pushable.mask(
			king_information.move_mask.mask(
				MoveGenerator::get_valid_push_moves(
					board,
					player,
					king_piece_data,
					king_information.coordinate)));

		for (const auto& attack : attacks)
		{
			moves.emplace_back(king_information.coordinate, attack);
		}

		for (const auto& push : pushes)
		{
			moves.emplace_back(king_information.coordinate, push);
		}
	}

#pragma endregion

#pragma region Pin Move Aggregation

	const auto& pins = MoveGenerator::get_pins(board, player);
	for (const auto& pin : pins)
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

		const auto& attacks = attackable.mask(
			pin.get_move_mask().mask(
				MoveGenerator::get_valid_attack_moves(
					board,
					player,
					piece_data,
					pin.get_coordinate())));

		const auto& pushes = pushable.mask(
			pin.get_move_mask().mask(
				MoveGenerator::get_valid_push_moves(
					board,
					player,
					piece_data,
					pin.get_coordinate())));

		for (const auto& attack : attacks)
		{
			moves.emplace_back(pin.get_coordinate(), attack);
		}

		for (const auto& push : pushes)
		{
			moves.emplace_back(pin.get_coordinate(), push);
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

			const auto& attacks = attackable.mask(
				MoveGenerator::get_valid_attack_moves(
					board,
					player,
					piece_data,
					cell));

			const auto& pushes = pushable.mask(
				MoveGenerator::get_valid_push_moves(
					board,
					player,
					piece_data,
					cell));

			for (const auto& attack : attacks)
			{
				moves.emplace_back(cell, attack);
			}

			for (const auto& push : pushes)
			{
				moves.emplace_back(cell, push);
			}
		}
	}

#pragma endregion

	return moves;
}
