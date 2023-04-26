#include "flag_board.hpp"

FlagBoard::FlagBoard(const Coordinate& dimensions) : std::vector<std::vector<bool>>(), dimensions(dimensions)
{
    const auto& [width, height] = this->dimensions;
    for (auto i = 0; i < height; i++)
    {
        this->push_back(std::vector<bool>(width, false));
    }
}

void FlagBoard::flag_attacks(
    const Board& board,
    const Player& player,
    const PieceData& piece_data,
    const Coordinate& coordinate,
    const std::optional<Coordinate>& ignore_coordinate,
    const bool ignore_pieces,
    const bool reverse_rays)
{
    auto cells = MoveGenerator::get_attacks(board, player, piece_data, coordinate, ignore_coordinate, ignore_pieces, reverse_rays);
    for (auto& cell : cells)
    {
        const auto& [i, j] = cell;
        this->operator[](i)[j] = true;
    }
}

void FlagBoard::flag_ray(
    const Board& board,
    const Player& player,
    const Coordinate& ray,
    const Coordinate& coordinate,
    const std::optional<Coordinate>& ignore_coordinate,
    const bool ignore_pieces)
{
    auto cells = MoveGenerator::get_ray(board, player, ray, coordinate, ignore_coordinate, ignore_pieces);
    for (auto& cell : cells)
    {
        const auto& [i, j] = cell;
        this->operator[](i)[j] = true;
    }
}

void FlagBoard::flag_jump(
    const Board& board,
    const Player& player,
    const Coordinate& jump,
    const Coordinate& coordinate,
    const std::optional<Coordinate>& ignore_coordinate,
    const bool ignore_pieces)
{
    auto cell = MoveGenerator::get_jump(board, player, jump, coordinate, ignore_pieces);
    if (!cell.has_value())
    {
        return;
    }

    const auto& [i, j] = cell.value();
    this->operator[](i)[j] = true;
}

std::vector<Coordinate> FlagBoard::mask(
    const std::vector<Coordinate> coordinates,
    const bool invert) const
{
    std::vector<Coordinate> masked = {};
    for (auto& coordinate : coordinates)
    {
        const auto& [i, j] = coordinate;
        if (this->operator[](i)[j] != invert)
        {
            masked.push_back(coordinate);
        }
    }
    return masked;
}
