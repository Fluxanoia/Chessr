#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "types.hpp"
#include "move.hpp"
#include "chess_engine.hpp"
#include "board.hpp"

namespace py = pybind11;

PYBIND11_MODULE(backend, m) {
    py::class_<ChessEngine>(m, "ChessEngine")
        .def(py::init<const Grid<Piece>, Player>())
        .def("get_move_history", &ChessEngine::get_move_history)
        .def("get_current_moves", &ChessEngine::get_current_moves)
        .def("make_move", &ChessEngine::make_move);

    py::class_<Piece>(m, "Piece")
        .def(py::init<PieceType, Player>())
        .def_property_readonly("type", &Piece::get_type)
        .def_property_readonly("player", &Piece::get_player);

    py::class_<Move>(m, "Move")
        .def_property_readonly("from_gxy", &Move::get_from)
        .def_property_readonly("to_gxy", &Move::get_to);

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
