#pragma once

#include "types.hpp"

inline Coordinate add_coordinates(const Coordinate& a, const Coordinate& b)
{
    const auto& [i, j] = a;
    const auto& [x, y] = b;
    return { i + x, j + y };
}

inline bool in_bounds(const Coordinate& dimensions, const Coordinate& coordinate)
{
    const auto& [i, j] = coordinate;
    const auto& [width, height] = dimensions;
    return i >= 0 && j >= 0 && i < height && j < width;
}
