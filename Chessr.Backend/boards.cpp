#include "boards.hpp"

Boards::Boards(const Grid<Piece>& starting_position, const Player starting_player) : current_player(starting_player)
{
	this->boards.emplace_back(starting_position);
}

void Boards::apply_move(const std::shared_ptr<Move> move)
{
	Grid<Piece> grid = this->get_current_board().get_grid();

	for (const auto& consequence : move->get_consequences())
	{
		switch (consequence->get_type())
		{
			case ConsequenceType::MOVE:
			{
				const auto& move_consequence = std::dynamic_pointer_cast<MoveConsequence>(consequence);
				if (move_consequence == nullptr)
				{
					throw InvalidOperationException("There was an attempt to cast a MoveConsequence.");
				}

				const auto& [from_i, from_j] = move_consequence->get_from();
				const auto& [to_i, to_j] = move_consequence->get_to();
				const auto& piece = grid[from_i][from_j];

				if (!piece.has_value())
				{
					throw InvalidOperationException("There was an attempt to move a piece that doesn't exist.");
				}
				if (grid[to_i][to_j].has_value())
				{
					throw InvalidOperationException("There was an attempt to move a piece to an inhabited cell.");
				}

				grid[to_i][to_j].emplace(piece.value());
				grid[from_i][from_j].reset();
				break;
			}
			case ConsequenceType::REMOVE:
			{
				const auto& remove_consequence = std::dynamic_pointer_cast<RemoveConsequence>(consequence);
				if (remove_consequence == nullptr)
				{
					throw InvalidOperationException("There was an attempt to cast a RemoveConsequence.");
				}

				const auto& [i, j] = remove_consequence->get_coordinate();
				if (!grid[i][j].has_value())
				{
					throw InvalidOperationException("There was an attempt to remove a piece that doesn't exist.");
				}
				grid[i][j].reset();
				break;
			}
			case ConsequenceType::CHANGE:
			{
				const auto& change_consequence = std::dynamic_pointer_cast<ChangeConsequence>(consequence);
				if (change_consequence == nullptr)
				{
					throw InvalidOperationException("There was an attempt to cast a ChangeConsequence.");
				}

				const auto& [i, j] = change_consequence->get_coordinate();
				const auto& piece = grid[i][j];

				if (!piece.has_value())
				{
					throw InvalidOperationException("There was an attempt to change a piece that doesn't exist.");
				}

				grid[i][j].reset();
				grid[i][j].emplace(change_consequence->get_piece_type(), piece.value().get_player());
				break;
			}
			default:
				throw UnexpectedCaseException("Unexpected consequence type.");
		}
	}

	this->boards.emplace_back(grid);
	this->moves.push_back(move);
	this->current_player = Maths::get_opposing_player(current_player);
}

bool Boards::has_moved(const Coordinate coordinate) const
{
	for (const auto& move : moves)
	for (const auto& consequence : move->get_consequences())
	{
		if (consequence->get_type() != ConsequenceType::MOVE)
		{
			continue;
		}

		const auto& move_consequence = std::dynamic_pointer_cast<MoveConsequence>(consequence);
		if (move_consequence == nullptr)
		{
			continue;
		}

		if (move_consequence->get_to() == coordinate)
		{
			return true;
		}
	}

	return false;
}

Board& Boards::get_current_board()
{
	return boards.back();
}

const Board& Boards::get_current_board() const
{
	return boards.back();
}

Board& Boards::get_previous_board()
{
	return boards.at(boards.size() - 2);
}

const Board& Boards::get_previous_board() const
{
	return boards.at(boards.size() - 2);
}

const Player& Boards::get_current_player() const
{
	return this->current_player;
}

const std::optional<std::shared_ptr<Move>> Boards::get_last_move() const
{
	return moves.size() > 0
		? std::optional<std::shared_ptr<Move>>{moves.back()}
		: std::optional<std::shared_ptr<Move>>{};
}
