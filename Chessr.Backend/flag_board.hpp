#pragma once

#include <vector>
#include <algorithm>
#include "types.hpp"

class FlagBoard : public std::vector<std::vector<bool>>
{
private:

    const Coordinate dimensions;

    void set_coordinates(const std::vector<Coordinate> coordinates, const bool value);
    void set_coordinates(const std::optional<Coordinate> coordinates, const bool value);

public: 

    FlagBoard(const Coordinate& dimensions, const bool default_value = false);


    void set_all(const bool value);
    void flag(const std::vector<Coordinate> coordinates);
    void flag(const std::optional<Coordinate> coordinates);
    void unflag(const std::vector<Coordinate> coordinates);
    void unflag(const std::optional<Coordinate> coordinates);
    void restrict(const std::vector<Coordinate> coordinates);

    std::vector<Coordinate> mask(const std::vector<Coordinate> coordinates) const;

};
