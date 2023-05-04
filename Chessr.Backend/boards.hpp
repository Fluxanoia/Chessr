#pragma once

#include <vector>
#include <memory>
#include "move.hpp"
#include "board.hpp"
#include "piece.hpp"
#include "consequence.hpp"

class Boards
{
private:

    std::vector<Board> boards;
    std::vector<std::shared_ptr<Move>> moves;
    Player current_player;

public:

    Boards(const Grid<Piece>& starting_grid, const Player starting_player);

    Board& get_current_board();
    const Board& get_current_board() const;
    Board& get_previous_board();
    const Board& get_previous_board() const;

    void apply_move(const std::shared_ptr<Move> move);
    bool has_moved(const Coordinate coordinate) const;
    const Player& get_current_player() const;
    const std::optional<std::shared_ptr<Move>> get_last_move() const;
};
