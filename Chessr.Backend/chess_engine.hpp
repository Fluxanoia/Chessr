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
    std::vector<Move> played_moves;
    std::vector<std::string> move_history;

    GameState game_state;
    Player current_player;
    bool currently_in_check;
    std::vector<Move> current_moves;

    std::string get_move_representation(const Move move) const;

    void calculate_moves();

public:

    ChessEngine(const Grid<Piece>& starting_position, const Player starting_player);

    void make_move(const Move move);

    GameState get_game_state() const;
    std::vector<Move> get_current_moves() const;
    std::vector<std::string> get_move_history() const;

    static std::string get_notation_from_coordinate(const Coordinate coordinate, const CoordinateValue board_height);
    static std::string get_file_from_coordinate(CoordinateValue file);
    static std::string get_rank_from_coordinate(const CoordinateValue rank, const CoordinateValue board_height);
};