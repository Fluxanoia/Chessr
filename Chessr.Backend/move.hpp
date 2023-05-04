#pragma once

#include <memory>
#include "types.hpp"
#include "consequence.hpp"
#include "exceptions.hpp"	

class Move {
private:

	MoveProperty move_property;
	std::vector<std::shared_ptr<Consequence>> consequences;

	std::optional<PieceType> promotion_piece_type = {};

public:

	Move(
		const std::vector<std::shared_ptr<Consequence>> consequences,
		const MoveProperty move_property = MoveProperty::NONE);

	const MoveProperty& get_property() const;
	const std::vector<std::shared_ptr<Consequence>>& get_consequences() const;
	const std::optional<PieceType>& get_promotion_piece_type() const;

	std::optional<std::shared_ptr<MoveConsequence>> get_move_consequence() const;

	bool moves_from(const Coordinate coordinate) const;
	bool moves_to(const Coordinate coordinate) const;
	bool attacks() const;
	bool is_attacking(const Coordinate coordinate) const;

	void set_promotion_type(const PieceType piece_type);
};
