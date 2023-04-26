#pragma once

#include <vector>
#include <optional>

template <class T>
using Grid = std::vector<std::vector<std::optional<T>>>;

typedef signed long long CoordinateValue;
typedef std::pair<CoordinateValue, CoordinateValue> Coordinate;

enum class PieceType
{
    QUEEN = 0,
    KING,
    BISHOP,
    ROOK,
    KNIGHT,
    PAWN,

    PIECE_TYPE_MAX
};

enum class Player
{
    WHITE = 0,
    BLACK
};
