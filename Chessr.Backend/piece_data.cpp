#include "piece_data.hpp"

std::vector<Coordinate> flip(const std::vector<Coordinate>& coordinates)
{
	auto flipped = std::vector<Coordinate>{};
	for (auto& coordinate : coordinates)
	{
		flipped.push_back({ -coordinate.first, coordinate.second });
	}
	return flipped;
}

std::vector<Coordinate> reverse(const std::vector<Coordinate>& coordinates)
{
	auto flipped = std::vector<Coordinate>{};
	for (auto& coordinate : coordinates)
	{
		flipped.push_back({ -coordinate.first, -coordinate.second });
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
	flipped_push_jumps(flip(push_jumps)),
	reversed_attack_rays(reverse(attack_rays)),
	reversed_attack_jumps(reverse(attack_jumps)),
	reversed_push_rays(reverse(push_rays)),
	reversed_push_jumps(reverse(push_jumps)),
	flipped_reversed_attack_rays(reverse(flip(attack_rays))),
	flipped_reversed_attack_jumps(reverse(flip(attack_jumps))),
	flipped_reversed_push_rays(reverse(flip(push_rays))),
	flipped_reversed_push_jumps(reverse(flip(push_jumps)))
{
}

const std::string PieceData::get_representation() const
{
	return this->representation;
}

const std::vector<Coordinate> PieceData::get_attack_rays(const Player& player, const bool& reverse) const
{
	return player == Player::WHITE
		? (reverse ? this->reversed_attack_rays : this->attack_rays)
		: (reverse ? this->flipped_reversed_attack_rays : this->flipped_attack_rays);
}

const std::vector<Coordinate> PieceData::get_attack_jumps(const Player& player, const bool& reverse) const
{
	return player == Player::WHITE
		? (reverse ? this->reversed_attack_jumps : this->attack_jumps)
		: (reverse ? this->flipped_reversed_attack_jumps : this->flipped_attack_jumps);
}

const std::vector<Coordinate> PieceData::get_push_rays(const Player& player, const bool& reverse) const
{
	return player == Player::WHITE
		? (reverse ? this->reversed_push_rays : this->push_rays)
		: (reverse ? this->flipped_reversed_push_rays : this->flipped_push_rays);
}

const std::vector<Coordinate> PieceData::get_push_jumps(const Player& player, const bool& reverse) const
{
	return player == Player::WHITE
		? (reverse ? this->reversed_push_jumps : this->push_jumps)
		: (reverse ? this->flipped_reversed_push_jumps : this->flipped_push_jumps);
}
