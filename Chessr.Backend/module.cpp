#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <sstream>
#include "types.hpp"
#include "data.hpp"
#include "chess_engine.hpp"
#include "board.hpp"

namespace py = pybind11;

PYBIND11_MODULE(backend, m) {
    py::class_<ChessEngine>(m, "ChessEngine")
        .def(py::init<const Grid<Piece>>())
        .def("get_moves", &ChessEngine::get_moves);

    py::class_<FlagBoard>(m, "FlagBoard")
        .def(py::init<const Coordinate>())
        .def("__repr__",
            [](const FlagBoard& x)
            {
                auto stream = std::stringstream{ "<FlagBoard with structure:\n" };

                for (const auto& row : x)
                {
                    for (const auto& b : row)
                    {
                        stream << " " << b ? "1" : "0";
                    }
                    stream << " \n";
                }

                stream << ">\n";
                return stream.str();
            }
        );

    py::class_<Piece>(m, "Piece")
        .def(py::init<PieceType, Player>())
        .def_property_readonly("type", &Piece::get_type)
        .def_property_readonly("player", &Piece::get_player);

    py::class_<Move>(m, "Move")
        .def(py::init<Coordinate, Coordinate>())
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
