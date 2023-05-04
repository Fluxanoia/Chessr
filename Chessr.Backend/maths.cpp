#include "maths.hpp"

const Coordinate Maths::UP = { -1, 0 };
const Coordinate Maths::DOWN = { 1, 0 };
const Coordinate Maths::LEFT = { 0, -1 };
const Coordinate Maths::RIGHT = { 0, 1 };
const Coordinate Maths::UP_LEFT = { -1, -1 };
const Coordinate Maths::UP_RIGHT = { -1, 1 };
const Coordinate Maths::DOWN_LEFT = { 1, -1 };
const Coordinate Maths::DOWN_RIGHT = { 1, 1 };

Coordinate Maths::flip_vector(const Coordinate coordinate)
{
	return { -coordinate.first, coordinate.second };
}

Coordinate Maths::flip_vector(const Coordinate coordinate, const Player player)
{
	return player == Player::WHITE ? coordinate : flip_vector(coordinate);
}

std::vector<Coordinate> Maths::flip_vectors(const std::vector<Coordinate>& coordinates)
{
	std::vector<Coordinate> flipped = {};
	for (auto& coordinate : coordinates)
	{
		flipped.push_back(flip_vector(coordinate));
	}
	return flipped;
}

std::vector<Coordinate> Maths::flip_vectors(const std::vector<Coordinate>& coordinates, const Player player)
{
	return player == Player::WHITE ? coordinates : flip_vectors(coordinates);
}
