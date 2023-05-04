#pragma once

#include "types.hpp"

class Maths
{
public:

	static const Coordinate UP;
	static const Coordinate DOWN;
	static const Coordinate LEFT;
	static const Coordinate RIGHT;
	static const Coordinate UP_LEFT;
	static const Coordinate UP_RIGHT;
	static const Coordinate DOWN_LEFT;
	static const Coordinate DOWN_RIGHT;

	static Coordinate flip_vector(const Coordinate coordinate);
	static Coordinate flip_vector(const Coordinate coordinate, const Player player);
	static std::vector<Coordinate> flip_vectors(const std::vector<Coordinate>& coordinates);
	static std::vector<Coordinate> flip_vectors(const std::vector<Coordinate>& coordinates, const Player player);

	static inline Coordinate add_coordinates(const Coordinate& a, const Coordinate& b)
	{
		const auto& [i, j] = a;
		const auto& [x, y] = b;
		return { i + x, j + y };
	}

	static inline Coordinate subtract_coordinates(const Coordinate& a, const Coordinate& b)
	{
		const auto& [i, j] = a;
		const auto& [x, y] = b;
		return { i - x, j - y };
	}

	static inline bool in_bounds(const Coordinate& dimensions, const Coordinate& coordinate)
	{
		const auto& [i, j] = coordinate;
		const auto& [width, height] = dimensions;
		return i >= 0 && j >= 0 && i < height&& j < width;
	}

	static inline Player get_opposing_player(const Player& player)
	{
		return player == Player::WHITE ? Player::BLACK : Player::WHITE;
	}
};


