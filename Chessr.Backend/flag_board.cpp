#include "flag_board.hpp"

#pragma region Public Methods

FlagBoard::FlagBoard(const Coordinate dimensions, const bool default_value)
	: flags(), dimensions(dimensions)
{
	const auto& [width, height] = this->dimensions;
	for (auto i = 0; i < height; i++)
	{
		this->flags.emplace_back(width, default_value);
	}
}

void FlagBoard::flag(const std::optional<Coordinate>& coordinate) { set_coordinates(coordinate, true); }
void FlagBoard::flag(const std::vector<Coordinate>& coordinates) { set_coordinates(coordinates, true); }
void FlagBoard::unflag(const std::optional<Coordinate>& coordinate) { set_coordinates(coordinate, false); }
void FlagBoard::unflag(const std::vector<Coordinate>& coordinates) { set_coordinates(coordinates, false); }

void FlagBoard::set_all(const bool value)
{
	const auto& [width, height] = this->dimensions;
	for (auto i = 0; i < height; i++)
	{
		for (auto j = 0; j < width; j++)
		{
			this->flags[i][j] = value;
		}
	}
}

void FlagBoard::restrict(const std::vector<Coordinate>& coordinates)
{
	const auto& [width, height] = this->dimensions;
	for (auto i = 0; i < height; i++)
	{
		for (auto j = 0; j < width; j++)
		{
			if (std::find(coordinates.begin(), coordinates.end(), Coordinate{ i, j }) == coordinates.end())
			{
				this->flags[i][j] = false;
			}
		}
	}
}

void FlagBoard::mask(std::vector<Coordinate>& coordinates) const
{
	auto it = coordinates.begin();
	while (it != coordinates.end())
	{
		const auto& [i, j] = *it;
		if (this->flags[i][j])
		{
			it++;
		}
		else
		{
			it = coordinates.erase(it);
		}
	}
}

std::vector<Coordinate> FlagBoard::get_flagged() const
{
	std::vector<Coordinate> flagged = {};
	const auto& [width, height] = this->dimensions;
	for (auto i = 0; i < height; i++)
	{
		for (auto j = 0; j < width; j++)
		{
			if (this->flags[i][j])
			{
				flagged.emplace_back(i, j);
			}
		}
	}
	return flagged;
}

#pragma endregion

#pragma region Private Methods

void FlagBoard::set_coordinates(const std::optional<Coordinate>& coordinate, const bool value)
{
	if (!coordinate.has_value())
	{
		return;
	}

	const auto& [i, j] = coordinate.value();
	this->flags[i][j] = value;
}

void FlagBoard::set_coordinates(const std::vector<Coordinate>& coordinates, const bool value)
{
	for (auto& cell : coordinates)
	{
		const auto& [i, j] = cell;
		this->flags[i][j] = value;
	}
}

#pragma endregion

