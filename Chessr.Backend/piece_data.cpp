#include "piece_data.hpp"

std::vector<Coordinate> flip(const std::vector<Coordinate>& coordinates)
{
	std::vector<Coordinate> flipped = {};
	for (auto& coordinate : coordinates)
	{
		flipped.emplace_back(-coordinate.first, coordinate.second);
	}
	return flipped;
}

PieceData::PieceData(
	const std::string representation,
	const std::vector<Coordinate> attack_rays,
	const std::vector<Coordinate> attack_jumps,
	const std::vector<Coordinate> push_rays,
	const std::vector<Coordinate> push_jumps)
	: representation(representation),
	attack_rays(attack_rays),
	attack_jumps(attack_jumps),
	push_rays(push_rays),
	push_jumps(push_jumps),
	flipped_attack_rays(flip(attack_rays)),
	flipped_attack_jumps(flip(attack_jumps)),
	flipped_push_rays(flip(push_rays)),
	flipped_push_jumps(flip(push_jumps))
{
}

const std::string& PieceData::get_representation() const
{
	return this->representation;
}

const std::vector<Coordinate>& PieceData::get_attack_rays(const Player& player) const
{
	return player == Player::WHITE ? this->attack_rays : this->flipped_attack_rays;
}

const std::vector<Coordinate>& PieceData::get_attack_jumps(const Player& player) const
{
	return player == Player::WHITE ? this->attack_jumps : this->flipped_attack_jumps;
}

const std::vector<Coordinate>& PieceData::get_push_rays(const Player& player) const
{
	return player == Player::WHITE ? this->push_rays : this->flipped_push_rays;
}

const std::vector<Coordinate>& PieceData::get_push_jumps(const Player& player) const
{
	return player == Player::WHITE ? this->push_jumps : this->flipped_push_jumps;
}
