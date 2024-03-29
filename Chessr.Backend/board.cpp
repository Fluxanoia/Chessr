#include "board.hpp"

Coordinate get_board_dimensions(const Grid<Piece>& grid)
{
	size_t height = grid.size();
	switch (height)
	{
		case 0:
			return { 0, 0 };
		case 1:
			return { grid.front().size(), 1 };
		default:
			auto width = grid.front().size();
			for (auto& v : grid)
			{
				if (v.size() != width)
				{
					throw InvalidBoardException{ "Invalid board dimensions." };
				}
			}

			return { width, height };
	}
}

Board::Board(const Grid<Piece> grid) : grid(grid), dimensions(get_board_dimensions(grid))
{
}

bool Board::is_in_check() const
{
	return in_check;
}

void Board::set_in_check()
{
	this->in_check = true;
}

bool Board::has_piece(const Coordinate& coordinate) const
{
	const auto& [i, j] = coordinate;
	return this->grid[i][j].has_value();
}

const Piece& Board::get_piece(const Coordinate& coordinate) const
{
	const auto& [i, j] = coordinate;
	return this->grid[i][j].value();
}

bool Board::rank_contains_multiple_of(
	const CoordinateValue rank,
	const PieceType piece_type,
	const Player player) const
{
	auto found = 0;
	for (const auto& cell : this->grid[rank])
	{
		if (!cell.has_value())
		{
			continue;
		}
		
		const auto& piece = cell.value();
		if (piece.get_type() == piece_type && piece.get_player() == player)
		{
			found++;
		}

		if (found > 1)
		{
			return true;
		}
	}

	return false;
}

bool Board::file_contains_multiple_of(
	const CoordinateValue file,
	const PieceType piece_type,
	const Player player) const
{
	auto found = 0;
	for (const auto& rank : this->grid)
	{
		const auto& cell = rank[file];
		if (!cell.has_value())
		{
			continue;
		}

		const auto& piece = cell.value();
		if (piece.get_type() == piece_type && piece.get_player() == player)
		{
			found++;
		}

		if (found > 1)
		{
			return true;
		}
	}

	return false;
}

std::vector<Coordinate> Board::positions_of(const PieceType piece_type, const Player player) const
{
	std::vector<Coordinate> positions = {};
	const auto& [width, height] = this->dimensions;
	for (auto i = 0; i < height; i++)
	for (auto j = 0; j < width; j++)
	{
		auto& maybe_piece = this->grid[i][j];
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

Coordinate Board::get_dimensions() const
{
	return this->dimensions;
}

const Grid<Piece>& Board::get_grid() const
{
	return this->grid;
}
