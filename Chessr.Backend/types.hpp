#pragma once

#include <vector>
#include <optional>

template <class T>
using Grid = std::vector<std::vector<std::optional<T>>>;
using CoordinateValue = signed long long;
using Coordinate = std::pair<CoordinateValue, CoordinateValue>;

enum class PieceType
{
    QUEEN = 0,
    KING,
    BISHOP,
    ROOK,
    KNIGHT,
    PAWN
};

enum class Player
{
    WHITE = 0,
    BLACK
};

enum class State
{
    NONE = 0,
    CHECK,
    CHECKMATE,
    STALEMATE
};

enum class MoveProperty
{
    NONE = 0,
    DOUBLE_MOVE,
    EN_PASSANT,
    CASTLE,
    PROMOTION
};

enum class MoveType
{
    ALL = 0,
    PUSH,
    ATTACK
};

enum class MoveStyle
{
    ALL = 0,
    JUMP,
    RAY
};
