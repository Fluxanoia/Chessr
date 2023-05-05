#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "types.hpp"
#include "move.hpp"
#include "chess_engine.hpp"
#include "board.hpp"

namespace py = pybind11;

class PyConsequence : public Consequence
{
public:

    using Consequence::Consequence;

    ConsequenceType get_type() const override
    {
        PYBIND11_OVERRIDE_PURE(
            ConsequenceType,
            Consequence,
            get_type);
    }

};

PYBIND11_MODULE(backend, m) {
    py::class_<ChessEngine>(m, "ChessEngine")
        .def(py::init<PieceConfiguration&>())
        .def("start", &ChessEngine::start)
        .def("get_piece_configuration", &ChessEngine::get_piece_configuration)
        .def("get_move_history", &ChessEngine::get_move_history)
        .def("get_current_moves", &ChessEngine::get_current_moves)
        .def("get_state", &ChessEngine::get_state)
        .def("get_current_player", &ChessEngine::get_current_player)
        .def("make_move", &ChessEngine::make_move);

    py::class_<Consequence, PyConsequence, std::shared_ptr<Consequence>>(m, "Consequence")
        .def(py::init<>())
        .def("get_type", &Consequence::get_type);

    py::class_<MoveConsequence, Consequence, std::shared_ptr<MoveConsequence>>(m, "MoveConsequence")
        .def_property_readonly("to_gxy", &MoveConsequence::get_to)
        .def_property_readonly("from_gxy", &MoveConsequence::get_from);

    py::class_<RemoveConsequence, Consequence, std::shared_ptr<RemoveConsequence>>(m, "RemoveConsequence")
        .def_property_readonly("gxy", &RemoveConsequence::get_coordinate);

    py::class_<ChangeConsequence, Consequence, std::shared_ptr<ChangeConsequence>>(m, "ChangeConsequence")
        .def_property_readonly("piece_type", &ChangeConsequence::get_piece_type)
        .def_property_readonly("gxy", &ChangeConsequence::get_coordinate);

    py::class_<Move, std::shared_ptr<Move>>(m, "Move")
        .def("get_consequences", &Move::get_consequences)
        .def("moves_to", &Move::moves_to)
        .def("moves_from", &Move::moves_from)
        .def("set_promotion_type", &Move::set_promotion_type)
        .def_property_readonly("property", &Move::get_property);

    py::class_<Piece>(m, "Piece")
        .def(py::init<PieceType, Player>())
        .def_property_readonly("type", &Piece::get_type)
        .def_property_readonly("player", &Piece::get_player);

    py::class_<PieceConfiguration>(m, "PieceConfiguration")
        .def(py::init<>())
        .def("get_piece_type", &PieceConfiguration::get_piece_type)
        .def("get_coordinate_from_notation", &PieceConfiguration::get_coordinate_from_notation)
        .def("get_notation_from_coordinate", &PieceConfiguration::get_notation_from_coordinate);

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

    py::enum_<ConsequenceType>(m, "ConsequenceType")
        .value("MOVE", ConsequenceType::MOVE)
        .value("REMOVE", ConsequenceType::REMOVE)
        .value("CHANGE", ConsequenceType::CHANGE);

    py::enum_<Player>(m, "Player")
        .value("WHITE", Player::WHITE)
        .value("BLACK", Player::BLACK);

    py::enum_<State>(m, "State")
        .value("NONE", State::NONE)
        .value("CHECK", State::CHECK)
        .value("CHECKMATE", State::CHECKMATE)
        .value("STALEMATE", State::STALEMATE);
}
