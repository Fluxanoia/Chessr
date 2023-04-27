#include "flag_board.hpp"

#pragma region Public Methods

FlagBoard::FlagBoard(const Coordinate& dimensions, const bool default_value)
	: std::vector<std::vector<bool>>(), dimensions(dimensions)
{
	const auto& [width, height] = this->dimensions;
	for (auto i = 0; i < height; i++)
	{
		this->push_back(std::vector<bool>(width, default_value));
	}
}

void FlagBoard::flag(const std::optional<Coordinate> coordinate)
{
	set_coordinates(coordinate, true);
}

void FlagBoard::flag(const std::vector<Coordinate> coordinates)
{
	set_coordinates(coordinates, true);
}

void FlagBoard::unflag(const std::optional<Coordinate> coordinate)
{
	set_coordinates(coordinate, false);
}

void FlagBoard::unflag(const std::vector<Coordinate> coordinates)
{
	set_coordinates(coordinates, false);
}

void FlagBoard::set_all(const bool value)
{
	const auto& [width, height] = this->dimensions;
	for (auto i = 0; i < height; i++)
	{
		for (auto j = 0; j < width; j++)
		{
			this->operator[](i)[j] = value;
		}
	}
}

void FlagBoard::restrict(const std::vector<Coordinate> coordinates)
{
	const auto& [width, height] = this->dimensions;
	for (auto i = 0; i < height; i++)
	{
		for (auto j = 0; j < width; j++)
		{
			if (std::find(coordinates.begin(), coordinates.end(), Coordinate{ i, j }) == coordinates.end())
			{
				this->operator[](i)[j] = false;
			}
		}
	}
}

std::vector<Coordinate> FlagBoard::mask(const std::vector<Coordinate> coordinates) const
{
	std::vector<Coordinate> masked = {};
	for (auto& coordinate : coordinates)
	{
		const auto& [i, j] = coordinate;
		if (this->operator[](i)[j])
		{
			masked.push_back(coordinate);
		}
	}
	return masked;
}

#pragma endregion

#pragma region Private Methods

void FlagBoard::set_coordinates(const std::optional<Coordinate> coordinate, const bool value)
{
	if (!coordinate.has_value())
	{
		return;
	}

	const auto& [i, j] = coordinate.value();
	this->operator[](i)[j] = value;
}

void FlagBoard::set_coordinates(const std::vector<Coordinate> coordinates, const bool value)
{
	for (auto& cell : coordinates)
	{
		const auto& [i, j] = cell;
		this->operator[](i)[j] = value;
	}
}

#pragma endregion

