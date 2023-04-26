#pragma once

#include <vector>
#include "board.hpp"
#include "types.hpp"
#include "piece_data.hpp"
#include "move_generator.hpp"

class FlagBoard : public std::vector<std::vector<bool>>
{
private:

    const Coordinate dimensions;

public: 

    FlagBoard(const Coordinate& dimensions);

    void flag_attacks(
        const Board& board,
        const Player& player,
        const PieceData& piece_data,
        const Coordinate& coordinate,
        const std::optional<Coordinate>& ignore_coordinate,
        const bool ignore_pieces,
        const bool reverse_rays);

    void flag_ray(
        const Board& board,
        const Player& player,
        const Coordinate& ray,
        const Coordinate& coordinate,
        const std::optional<Coordinate>& ignore_coordinate,
        const bool ignore_pieces);

    void flag_jump(
        const Board& board,
        const Player& player,
        const Coordinate& jump,
        const Coordinate& coordinate,
        const std::optional<Coordinate>& ignore_coordinate,
        const bool ignore_pieces);

    std::vector<Coordinate> mask(
        const std::vector<Coordinate> coordinates,
        const bool invert = false) const;

};
