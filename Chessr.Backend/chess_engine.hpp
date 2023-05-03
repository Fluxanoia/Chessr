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
#include "consequence.hpp"
#include "pinned_piece.hpp"
#include "move_generator.hpp"
#include "piece_configuration.hpp"

class ChessEngine {
private:

    struct KingInformation
    {
        const Coordinate coordinate;
        const FlagBoard move_mask;
        const std::vector<Coordinate> checkers;

        KingInformation(Coordinate coordinate, FlagBoard move_mask, std::vector<Coordinate> checkers)
            : coordinate(coordinate), move_mask(move_mask), checkers(checkers)
        {
        }
    };

    std::vector<Board> positions;
    std::vector<Move> played_moves;
    std::vector<std::string> move_history;

    State game_state;
    Player current_player;
    bool currently_in_check;
    std::vector<Move> current_moves;

    std::string get_move_representation(const Move move) const;

    void calculate_moves();

public:

    ChessEngine(const Grid<Piece>& starting_position, const Player starting_player);

    std::vector<Consequence> make_move(const Move move);

    State get_state() const;
    Player get_current_player() const;
    std::vector<Move> get_current_moves() const;
    std::vector<std::string> get_move_history() const;
};