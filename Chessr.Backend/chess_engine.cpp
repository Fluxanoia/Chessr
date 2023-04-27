#include "chess_engine.hpp"

ChessEngine::ChessEngine(const Grid<Piece> starting_position) {
	this->positions.push_back(Board{ starting_position });
}

typedef struct _KingInformation
{
	const Coordinate& coordinate;
	const FlagBoard& move_mask;
	const std::vector<Coordinate> checkers;
} KingInformation;

const std::vector<Move> ChessEngine::get_moves(const Player player) const {
	const auto& board = this->positions.back();
	const auto& [width, height] = board.get_dimensions();
	const auto& piece_configuration = PieceConfiguration::get_instance();
	const auto opposing_player = MoveGenerator::get_opposing_player(player);

#pragma region King Information

	auto king_informations = std::vector<KingInformation>{};
	for (auto& coordinate : board.positions_of(PieceType::KING, player))
	{
		KingInformation king_information = {
			coordinate,
			MoveGenerator::get_king_move_mask(board, player, coordinate),
			MoveGenerator::get_attacking_coordinates(board, player, coordinate)
		};
		king_informations.push_back(king_information);
	}

	std::vector<KingInformation> single_checks = {};
	std::vector<KingInformation> double_checks = {};
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
			const auto double_check_moves = double_check.move_mask.mask(
				MoveGenerator::get_valid_moves(
					board,
					player,
					king_piece_data,
					double_check.coordinate));

			switch (single_checks.size())
			{
				case 0:
				{
					// This king must evade check. Possibly checkmate.
					std::vector<Move> moves = {};
					for (const auto& destination : double_check_moves)
					{
						moves.push_back(Move{ double_check.coordinate, destination });
					}
					return moves;
				}
				default:
					// This king must evade check and stop the check on other kings.
					// Since it cannot block check, it must take the piece.
					std::set<Coordinate> other_checkers = {};
					for (const auto& single_check : single_checks)
					{
						for (const auto& checker : single_check.checkers)
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
						return std::vector<Move>{ { double_check.coordinate, other_checker } };
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
		for (const auto& checker : single_check.checkers)
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

	for (const auto& king_information : king_informations)
	{
		const auto attacks = attackable.mask(
			king_information.move_mask.mask(
				MoveGenerator::get_valid_attack_moves(
					board,
					player,
					king_piece_data,
					king_information.coordinate)));

		const auto pushes = pushable.mask(
			king_information.move_mask.mask(
				MoveGenerator::get_valid_push_moves(
					board,
					player,
					king_piece_data,
					king_information.coordinate)));

		// TODO something
	}

	// TODO: add every other move

	return {};
}
