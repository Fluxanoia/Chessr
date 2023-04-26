#include "board.hpp"

Coordinate get_board_dimensions(const Grid<Piece> position)
{
	size_t height = position.size();
	switch (height)
	{
		case 0:
			return std::pair{ 0, 0 };
		case 1:
			return std::pair{ position.begin()->size(), 1 };
		default:
			size_t width = position.begin()->size();

			for (auto v = position.begin(); v != position.end(); v++)
			{
				if (v->size() != width)
				{
					throw InvalidBoardException{ "Invalid board dimensions." };
				}
			}

			return std::pair{ width, height };
	}
}

Board::Board(const Grid<Piece> position) : position(position), dimensions(get_board_dimensions(position))
{
}

bool Board::has_piece(const Coordinate coordinate) const
{
	const auto& [i, j] = coordinate;
	return this->position[i][j].has_value();
}

const Piece& Board::get_piece(const Coordinate coordinate) const
{
	const auto& [i, j] = coordinate;
	return this->position[i][j].value();
}

std::vector<Coordinate> Board::positions_of(const PieceType piece_type, const Player player) const
{
	const auto& [width, height] = this->dimensions;

	std::vector<Coordinate> positions{};
	for (auto i = 0; i < height; i++)
	{
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
	}

	return positions;
}

const Coordinate& Board::get_dimensions() const
{
	return this->dimensions;
}
