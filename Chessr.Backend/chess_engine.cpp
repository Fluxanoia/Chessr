#include "chess_engine.hpp"

ChessEngine::ChessEngine(const Grid<Piece> starting_position) {
	this->positions.push_back(Board{ starting_position });
}

typedef struct _KingInformation
{
	const Coordinate& coordinate;
	FlagBoard& danger_flags;
	std::set<Coordinate> checkers;
} KingInformation;

const std::vector<Move> ChessEngine::get_moves(const Player player) const {
	auto& piece_configuration = PieceConfiguration::get_instance();
	const auto& board = this->positions.back();
	auto opposing_player = player == Player::WHITE ? Player::BLACK : Player::WHITE;
	const auto& [width, height] = board.get_dimensions();

#pragma region King Information

	auto king_informations = std::vector<KingInformation>{};
	for (auto& king_position : board.positions_of(PieceType::KING, player))
	{
		FlagBoard king_danger_flags = { board.get_dimensions() };
		KingInformation king_information = {
			king_position,
			king_danger_flags,
			{}
		};

#pragma region Danger Flags

		// Generate a board encoding the squares that the king cannot move to.
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

				auto& config = piece_configuration.get_data(piece.get_type());
				king_danger_flags.flag_attacks(
					board,
					opposing_player,
					config,
					cell,
					king_position,
					false,
					false);
			}
		}

#pragma endregion

#pragma region Checks

		// Calculate the pieces putting the king in check, if any.
		for (auto& piece_type : piece_configuration.get_piece_types())
		{
			auto& config = piece_configuration.get_data(piece_type);
			const auto attack_cells = MoveGenerator::get_attacks(
				board,
				opposing_player,
				config,
				king_position,
				std::make_optional<Coordinate>(),
				true,
				true);

			for (auto& cell : attack_cells)
			{
				if (!board.has_piece(cell))
				{
					continue;
				}

				auto& piece = board.get_piece(cell);
				if (piece.get_player() == opposing_player && piece.get_type() == piece_type)
				{
					king_information.checkers.insert(cell);
				}
			}

#pragma endregion

			king_informations.push_back(king_information);
		}
	}

#pragma endregion

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

#pragma region Double Check Logic

	auto& king_config = piece_configuration.get_data(PieceType::KING);
	switch (double_checks.size())
	{
		case 0:
			break;
		case 1:
		{
			// A king is under double check, so only moves by that king are valid.
			const auto& double_check = double_checks.at(0);
			const auto double_check_destinations = double_check.danger_flags.mask(
				MoveGenerator::get_all_moves(
					board,
					player,
					king_config,
					double_check.coordinate),
				true);

			switch (single_checks.size())
			{
				case 0:
				{
					// This king must evade check. Possibly checkmate.
					std::vector<Move> moves = {};
					for (const auto& destination : double_check_destinations)
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
						double_check_destinations.begin(),
						double_check_destinations.end(),
						other_checker) != double_check_destinations.end();

					if (capturable)
					{
						// We can capture the piece putting the other kings in check.
						std::vector<Move> moves = {};
						moves.push_back({ double_check.coordinate, other_checker });
						return moves;
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

	// There are no double checks, so we consider single checks.

	// TODO

	return {};
}
