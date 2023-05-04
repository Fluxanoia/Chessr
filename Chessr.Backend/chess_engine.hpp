#pragma once

#include <set>
#include <vector>
#include <optional>
#include <algorithm>
#include "move.hpp"
#include "types.hpp"
#include "maths.hpp"
#include "board.hpp"
#include "boards.hpp"
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
        const std::shared_ptr<FlagBoard> move_mask;
        const std::vector<Coordinate> checkers;

        KingInformation(Coordinate coordinate, std::shared_ptr<FlagBoard> move_mask, std::vector<Coordinate> checkers)
            : coordinate(coordinate), move_mask(move_mask), checkers(checkers)
        {
        }
    };

    State state;
    std::vector<std::shared_ptr<Move>> current_moves;

    Boards boards;
    std::vector<std::string> move_history;

    std::string get_move_representation(const std::shared_ptr<Move> move);

    void calculate_moves();

public:

    ChessEngine(const Grid<Piece>& starting_position, const Player starting_player);

    std::vector<std::shared_ptr<Consequence>> make_move(const std::shared_ptr<Move> move);

    State get_state() const;
    Player get_current_player() const;
    std::vector<std::shared_ptr<Move>> get_current_moves() const;
    std::vector<std::string> get_move_history() const;
};