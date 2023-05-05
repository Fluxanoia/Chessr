#include "move.hpp"

Move::Move(
	const std::vector<std::shared_ptr<Consequence>> consequences,
	const MoveProperty move_property)
	: consequences(consequences), move_property(move_property)
{
}

const MoveProperty& Move::get_property() const
{
	return this->move_property;
}

const std::vector<std::shared_ptr<Consequence>>& Move::get_consequences() const
{
	return this->consequences;
}

void Move::set_promotion_type(const PieceType piece_type)
{
	if (this->move_property != MoveProperty::PROMOTION)
	{
		throw InvalidOperationException("There was an attempt to set the promotion piece type for a non-promotion move.");
	}
	auto move_consequence = get_move_consequence();
	if (!move_consequence.has_value())
	{
		return;
	}

	this->consequences.push_back(
		std::make_shared<ChangeConsequence>(move_consequence.value()->get_to(), piece_type)
	);
}

std::optional<std::shared_ptr<MoveConsequence>> Move::get_move_consequence() const
{
	for (const auto& consequence : consequences)
	{
		if (consequence->get_type() == ConsequenceType::MOVE)
		{
			auto cast = std::dynamic_pointer_cast<MoveConsequence>(consequence);
			if (cast == nullptr)
			{
				return {};
			}
			return cast;
		}
	}
	return {};
}

bool Move::moves_from(const Coordinate coordinate) const
{
	for (const auto& consequence : consequences)
	{
		if (consequence->get_type() == ConsequenceType::MOVE)
		{
			continue;
		}
		auto cast = std::dynamic_pointer_cast<MoveConsequence>(consequence);
		if (cast != nullptr && cast->get_from() == coordinate)
		{
			return true;
		}
	}
	return false;
}

bool Move::moves_to(const Coordinate coordinate) const
{
	for (const auto& consequence : consequences)
	{
		if (consequence->get_type() != ConsequenceType::MOVE)
		{
			continue;
		}
		auto cast = std::dynamic_pointer_cast<MoveConsequence>(consequence);
		if (cast != nullptr && cast->get_to() == coordinate)
		{
			return true;
		}
	}
	return false;
}

bool Move::attacks() const
{
	for (const auto& consequence : consequences)
	{
		if (consequence->get_type() == ConsequenceType::REMOVE)
		{
			return true;
		}
	}
	return false;
}

bool Move::is_attacking(const Coordinate coordinate) const
{
	for (const auto& consequence : consequences)
	{
		if (consequence->get_type() != ConsequenceType::REMOVE)
		{
			continue;
		}
		auto cast = std::dynamic_pointer_cast<RemoveConsequence>(consequence);
		if (cast != nullptr && cast->get_coordinate() == coordinate)
		{
			return true;
		}
	}

	return false;
}
