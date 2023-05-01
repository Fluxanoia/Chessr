#pragma once

#include <set>
#include <vector>
#include <optional>
#include <algorithm>
#include "move.hpp"
#include "types.hpp"
#include "maths.hpp"
#include "board.hpp"
#include "flag_board.hpp"
#include "pinned_piece.hpp"
#include "move_generator.hpp"
#include "piece_configuration.hpp"

class ChessEngine {
private:

    std::vector<Board> positions;

public:

    ChessEngine(const Grid<Piece>& starting_position);

    const std::vector<Move> get_moves(const Player player) const;

};