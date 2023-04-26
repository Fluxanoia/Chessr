#pragma once

#include <vector>
#include <optional>
#include "board.hpp"
#include "piece_configuration.hpp"

class MoveGenerator
{
public:

    static std::vector<Coordinate> get_attacks(
        const Board& board,
        const Player& player,
        const PieceData& piece_data,
        const Coordinate& coordinate,
        const std::optional<Coordinate>& ignore_coordinate,
        const bool ignore_pieces,
        const bool reverse_rays);

    static std::vector<Coordinate> get_pushes(
        const Board& board,
        const Player& player,
        const PieceData& piece_data,
        const Coordinate& coordinate);

    static std::vector<Coordinate> get_moves(
        const Board& board,
        const Player& player,
        const std::vector<Coordinate>& rays,
        const std::vector<Coordinate>& jumps,
        const Coordinate& coordinate,
        const std::optional<Coordinate>& ignore_coordinate,
        const bool ignore_pieces);

    static std::vector<Coordinate> get_all_moves(
        const Board& board,
        const Player& player,
        const PieceData& piece_data,
        const Coordinate& coordinate);

    static std::vector<Coordinate> get_ray(
        const Board& board,
        const Player& player,
        const Coordinate& ray,
        const Coordinate& coordinate,
        const std::optional<Coordinate>& ignore_coordinate,
        const bool ignore_pieces);

    static std::optional<Coordinate> get_jump(
        const Board& board,
        const Player& player,
        const Coordinate& jump,
        const Coordinate& coordinate,
        const bool ignore_pieces);

};
