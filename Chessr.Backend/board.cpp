#include "board.hpp"

Coordinate get_board_dimensions(const Grid<Piece>& position)
{
	size_t height = position.size();
	switch (height)
	{
		case 0:
			return { 0, 0 };
		case 1:
			return { position.front().size(), 1 };
		default:
			auto width = position.front().size();
			for (auto& v : position)
			{
				if (v.size() != width)
				{
					throw InvalidBoardException{ "Invalid board dimensions." };
				}
			}

			return { width, height };
	}
}

Board::Board(const Grid<Piece> position) : position(position), dimensions(get_board_dimensions(position))
{
}

bool Board::has_piece(const Coordinate& coordinate) const
{
	const auto& [i, j] = coordinate;
	return this->position[i][j].has_value();
}

const Piece& Board::get_piece(const Coordinate& coordinate) const
{
	const auto& [i, j] = coordinate;
	return this->position[i][j].value();
}

std::vector<Coordinate> Board::positions_of(const PieceType& piece_type, const Player& player) const
{
	std::vector<Coordinate> positions = {};
	const auto& [width, height] = this->dimensions;
	for (auto i = 0; i < height; i++)
	for (auto j = 0; j < width; j++)
	{
		auto& maybe_piece = this->position[i][j];
		if (!maybe_piece.has_value())
		{
			continue;
		}

		auto& piece = maybe_piece.value();
		if (piece.get_type() == piece_type && piece.get_player() == player)
		{
			positions.push_back({ i, j });
		}
	}

	return positions;
}

const Coordinate& Board::get_dimensions() const
{
	return this->dimensions;
}
