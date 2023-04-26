#pragma once

#include <map>
#include "piece_data.hpp"

class PieceConfiguration
{
private:

    const std::map<PieceType, PieceData> data;
    const std::vector<PieceType> piece_types;
    const std::vector<PieceType> piece_types_sans_king;

    PieceConfiguration();

public:

    static const Coordinate UP;
    static const Coordinate DOWN;
    static const Coordinate LEFT;
    static const Coordinate RIGHT;
    static const Coordinate UP_LEFT;
    static const Coordinate UP_RIGHT;
    static const Coordinate DOWN_LEFT;
    static const Coordinate DOWN_RIGHT;

    static const PieceConfiguration& get_instance()
    {
        static PieceConfiguration instance;
        return instance;
    }

    const PieceData& get_data(const PieceType piece_type) const;
    const std::vector<PieceType>& get_piece_types() const;
    const std::vector<PieceType>& get_piece_types_sans_king() const;

    PieceConfiguration(PieceConfiguration const&) = delete;
    void operator=(PieceConfiguration const&) = delete;

};
