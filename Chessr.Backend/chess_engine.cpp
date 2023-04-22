#include <pybind11/pybind11.h>
#include "enums.hpp"
#include "data.hpp"
#include "board.hpp"

namespace py = pybind11;

class ChessEngine {
private:

    std::vector<Board*> positions;

public:
    ChessEngine(const std::vector<std::vector<Piece>> starting_position) {
        this->positions.push_back(new Board(starting_position));
    }

    std::vector<Move> get_moves(Player player) {
        std::vector<Move> moves = {};
        Move move = {
            std::tuple<int, int>{ 1, 2 },
            std::tuple<int, int>{ 3, 4 }
        };
        moves.push_back(move);
        return moves;
    }
};

PYBIND11_MODULE(backend, m) {
    py::class_<ChessEngine>(m, "ChessEngine")
        .def(py::init<const std::vector<std::vector<Piece>>>())
        .def("get_moves", &ChessEngine::get_moves);

    py::class_<Piece>(m, "Piece")
        .def_property_readonly("type", &Piece::get_type)
        .def_property_readonly("player", &Piece::get_player);

    py::class_<Move>(m, "Move")
        .def_property_readonly("from", &Move::get_from)
        .def_property_readonly("to", &Move::get_to);

    py::enum_<PieceType>(m, "PieceType")
        .value("QUEEN", PieceType::QUEEN)
        .value("KING", PieceType::KING)
        .value("BISHOP", PieceType::BISHOP)
        .value("ROOK", PieceType::ROOK)
        .value("KNIGHT", PieceType::KNIGHT)
        .value("PAWN", PieceType::PAWN);

    py::enum_<Player>(m, "Player")
        .value("WHITE", Player::WHITE)
        .value("BLACK", Player::BLACK);
}
