#pragma once

#include <map>
#include <string>
#include <vector>
#include <algorithm>
#include "piece_data.hpp"

class PieceConfiguration
{
private:

    const std::map<PieceType, std::shared_ptr<PieceData>> data;
    const std::vector<PieceType> piece_types;

public:

    PieceConfiguration();

    const std::shared_ptr<PieceData> get_piece_data(const PieceType piece_type) const;
    const std::vector<PieceType>& get_piece_types() const;
    std::optional<PieceType> get_piece_type(std::string representation) const;
    std::optional<Coordinate> get_coordinate_from_notation(const std::string notation, const CoordinateValue board_height) const;
    std::string get_notation_from_coordinate(const Coordinate coordinate, const CoordinateValue board_height) const;
    std::string get_file_from_coordinate(CoordinateValue file) const;
    std::string get_rank_from_coordinate(const CoordinateValue rank, const CoordinateValue board_height) const;

};
