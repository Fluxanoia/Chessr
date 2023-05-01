#include "piece_configuration.hpp"

const Coordinate PieceConfiguration::UP = { -1, 0 };
const Coordinate PieceConfiguration::DOWN = { 1, 0 };
const Coordinate PieceConfiguration::LEFT = { 0, -1 };
const Coordinate PieceConfiguration::RIGHT = { 0, 1 };
const Coordinate PieceConfiguration::UP_LEFT = { -1, -1 };
const Coordinate PieceConfiguration::UP_RIGHT = { -1, 1 };
const Coordinate PieceConfiguration::DOWN_LEFT = { 1, -1 };
const Coordinate PieceConfiguration::DOWN_RIGHT = { 1, 1 };

std::map<PieceType, PieceData> generate_piece_data()
{
	std::vector<Coordinate> all_directions = {
		PieceConfiguration::UP,
		PieceConfiguration::DOWN,
		PieceConfiguration::LEFT,
		PieceConfiguration::RIGHT,
		PieceConfiguration::UP_LEFT,
		PieceConfiguration::UP_RIGHT,
		PieceConfiguration::DOWN_LEFT,
		PieceConfiguration::DOWN_RIGHT
	};

	std::vector<Coordinate> diagonals = {
		PieceConfiguration::UP_LEFT,
		PieceConfiguration::UP_RIGHT,
		PieceConfiguration::DOWN_LEFT,
		PieceConfiguration::DOWN_RIGHT
	};

	std::vector<Coordinate> orthogonals = {
		PieceConfiguration::UP,
		PieceConfiguration::DOWN,
		PieceConfiguration::LEFT,
		PieceConfiguration::RIGHT
	};

	std::vector<Coordinate> knight_vectors = {
		{ -2, -1 },
		{ -2, 1 },
		{ 2, -1 },
		{ 2, 1 },
		{ -1, 2 },
		{ 1, 2 },
		{ -1, -2 },
		{ 1, -2 },
	};

	PieceData queen = { "Q", all_directions, {}, all_directions, {} };
	PieceData king = { "K", {}, all_directions, {}, all_directions };
	PieceData bishop = { "B", diagonals, {}, diagonals, {} };
	PieceData rook = { "R", orthogonals, {}, orthogonals, {} };
	PieceData knight = { "N", {}, knight_vectors, {}, knight_vectors };
	PieceData pawn = { "P", {}, { PieceConfiguration::UP }, {}, { { -1, -1 }, { -1, 1 } } };

	return std::map<PieceType, PieceData>{
		{ PieceType::QUEEN, queen },
		{ PieceType::BISHOP, bishop },
		{ PieceType::ROOK, rook },
		{ PieceType::KNIGHT, knight },
		{ PieceType::PAWN, pawn },
		{ PieceType::KING, king },
	};
}

std::vector<PieceType> generate_piece_types(std::map<PieceType, PieceData> map)
{
	std::vector<PieceType> types = {};
	for (const auto& [key, _] : map)
	{
		types.push_back(key);
	}
	return types;
}

PieceConfiguration::PieceConfiguration()
	: data(generate_piece_data()), piece_types(generate_piece_types(data))
{
}

const PieceData& PieceConfiguration::get_data(const PieceType piece_type) const
{
	return this->data.at(piece_type);
}

const std::vector<PieceType>& PieceConfiguration::get_piece_types() const
{
	return this->piece_types;
}
