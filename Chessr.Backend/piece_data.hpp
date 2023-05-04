#pragma once

#include <string>
#include <vector>
#include <memory>
#include <algorithm>
#include "move.hpp"
#include "types.hpp"
#include "boards.hpp"

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

public:

	PieceData(
		const std::string representation,
		const std::vector<Coordinate> attack_rays,
		const std::vector<Coordinate> attack_jumps,
		const std::vector<Coordinate> push_rays,
		const std::vector<Coordinate> push_jumps);

	const std::string& get_representation() const;

	std::vector<Coordinate> get_ray(
		const Boards& boards,
		const Player& player,
		const Coordinate& ray,
		const Coordinate& coordinate,
		const std::optional<Coordinate>& ignore_coordinate,
		const bool attack) const;

	std::optional<Coordinate> get_jump(
		const Boards& boards,
		const Player& player,
		const Coordinate& jump,
		const Coordinate& coordinate,
		const bool attack) const;

	virtual std::vector<std::shared_ptr<Move>> get_moves(
		const Boards& boards,
		const Player& player,
		const Coordinate& coordinate,
		const MoveType move_type,
		const MoveStyle move_style,
		const std::optional<Coordinate>& ignore_coordinate) const;

	std::vector<Coordinate> get_vectors(const MoveType type, const MoveStyle style, const Player& player) const;

};

class PawnPieceData : public PieceData
{
public:

	PawnPieceData(
		const std::string representation,
		const std::vector<Coordinate> attack_rays,
		const std::vector<Coordinate> attack_jumps,
		const std::vector<Coordinate> push_rays,
		const std::vector<Coordinate> push_jumps);

	std::vector<std::shared_ptr<Move>> get_moves(
		const Boards& boards,
		const Player& player,
		const Coordinate& coordinate,
		const MoveType move_type,
		const MoveStyle move_style,
		const std::optional<Coordinate>& ignore_coordinate) const override;

};

class KingPieceData : public PieceData
{
public:

	KingPieceData(
		const std::string representation,
		const std::vector<Coordinate> attack_rays,
		const std::vector<Coordinate> attack_jumps,
		const std::vector<Coordinate> push_rays,
		const std::vector<Coordinate> push_jumps);

	std::vector<std::shared_ptr<Move>> get_moves(
		const Boards& boards,
		const Player& player,
		const Coordinate& coordinate,
		const MoveType move_type,
		const MoveStyle move_style,
		const std::optional<Coordinate>& ignore_coordinate) const override;

};
