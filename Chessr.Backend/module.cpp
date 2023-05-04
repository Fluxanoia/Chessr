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
        .def("get_state", &ChessEngine::get_state)
        .def("get_current_player", &ChessEngine::get_current_player)
        .def("make_move", &ChessEngine::make_move);

    py::class_<PieceConfiguration>(m, "PieceConfiguration")
        .def("get_instance", &PieceConfiguration::get_instance)
        .def("get_piece_type", &PieceConfiguration::get_piece_type)
        .def("get_coordinate_from_notation", &PieceConfiguration::get_coordinate_from_notation)
        .def("get_notation_from_coordinate", &PieceConfiguration::get_notation_from_coordinate);

    py::class_<Piece>(m, "Piece")
        .def(py::init<PieceType, Player>())
        .def_property_readonly("type", &Piece::get_type)
        .def_property_readonly("player", &Piece::get_player);

    py::class_<Move>(m, "Move")
        .def_property_readonly("property", &Move::get_property)
        .def_property_readonly("set_promotion_type", &Move::set_promotion_type);

    py::enum_<MoveProperty>(m, "MoveProperty")
        .value("NONE", MoveProperty::NONE)
        .value("DOUBLE_MOVE", MoveProperty::DOUBLE_MOVE)
        .value("EN_PASSANT", MoveProperty::EN_PASSANT)
        .value("CASTLE", MoveProperty::CASTLE)
        .value("PROMOTION", MoveProperty::PROMOTION);

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

    py::enum_<State>(m, "State")
        .value("NONE", State::NONE)
        .value("CHECK", State::CHECK)
        .value("CHECKMATE", State::CHECKMATE)
        .value("STALEMATE", State::STALEMATE);
}
