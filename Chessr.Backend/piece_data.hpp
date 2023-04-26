#pragma once

#include <string>
#include "types.hpp"

class PieceData
{
private:

    const std::string representation;
    const std::vector<Coordinate> attack_rays;
    const std::vector<Coordinate> attack_jumps;
    const std::vector<Coordinate> push_rays;
    const std::vector<Coordinate> push_jumps;

    const std::vector<Coordinate> flipped_attack_rays;
    const std::vector<Coordinate> flipped_attack_jumps;
    const std::vector<Coordinate> flipped_push_rays;
    const std::vector<Coordinate> flipped_push_jumps;

    const std::vector<Coordinate> reversed_attack_rays;
    const std::vector<Coordinate> reversed_attack_jumps;
    const std::vector<Coordinate> reversed_push_rays;
    const std::vector<Coordinate> reversed_push_jumps;

    const std::vector<Coordinate> flipped_reversed_attack_rays;
    const std::vector<Coordinate> flipped_reversed_attack_jumps;
    const std::vector<Coordinate> flipped_reversed_push_rays;
    const std::vector<Coordinate> flipped_reversed_push_jumps;

public:

    PieceData(
        const std::string representation,
        const std::vector<Coordinate> attack_rays,
        const std::vector<Coordinate> attack_jumps,
        const std::vector<Coordinate> push_rays,
        const std::vector<Coordinate> push_jumps);

    const std::string get_representation() const;
    const std::vector<Coordinate> get_attack_rays(const Player& player, const bool& reverse = false) const;
    const std::vector<Coordinate> get_attack_jumps(const Player& player, const bool& reverse = false) const;
    const std::vector<Coordinate> get_push_rays(const Player& player, const bool& reverse = false) const;
    const std::vector<Coordinate> get_push_jumps(const Player& player, const bool& reverse = false) const;

};
