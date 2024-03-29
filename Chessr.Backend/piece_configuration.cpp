#include "piece_configuration.hpp"

#pragma region Constructor

std::map<PieceType, std::shared_ptr<PieceData>> generate_piece_data()
{
	std::vector<Coordinate> all_directions = {
		Maths::UP,
		Maths::DOWN,
		Maths::LEFT,
		Maths::RIGHT,
		Maths::UP_LEFT,
		Maths::UP_RIGHT,
		Maths::DOWN_LEFT,
		Maths::DOWN_RIGHT
	};

	std::vector<Coordinate> diagonals = {
		Maths::UP_LEFT,
		Maths::UP_RIGHT,
		Maths::DOWN_LEFT,
		Maths::DOWN_RIGHT
	};

	std::vector<Coordinate> orthogonals = {
		Maths::UP,
		Maths::DOWN,
		Maths::LEFT,
		Maths::RIGHT
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

	std::vector<Coordinate> pawn_push_vectors = { Maths::UP };
	std::vector<Coordinate> pawn_attack_vectors = {
		{ -1, -1 },
		{ -1, 1 }
	};

	std::vector<Coordinate> none = {};

	auto queen = std::make_shared<PieceData>("Q", all_directions, none, all_directions, none);
	auto bishop = std::make_shared<PieceData>("B", diagonals, none, diagonals, none);
	auto rook = std::make_shared<PieceData>("R", orthogonals, none, orthogonals, none);
	auto knight = std::make_shared<PieceData>("N", none, knight_vectors, none, knight_vectors);
	auto king = std::make_shared<KingPieceData>("K", none, all_directions, none, all_directions);
	auto pawn = std::make_shared<PawnPieceData>("P", none, pawn_attack_vectors, none, pawn_push_vectors);

	return std::map<PieceType, std::shared_ptr<PieceData>>{
		{ PieceType::QUEEN, queen },
		{ PieceType::BISHOP, bishop },
		{ PieceType::ROOK, rook },
		{ PieceType::KNIGHT, knight },
		{ PieceType::PAWN, pawn },
		{ PieceType::KING, king },
	};
}

std::vector<PieceType> generate_piece_types(const std::map<PieceType, std::shared_ptr<PieceData>> map)
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

#pragma endregion

#pragma region Getters

std::optional<PieceType> PieceConfiguration::get_piece_type(std::string representation) const
{
	for (const auto& [key, value] : this->data)
	{
		if (value->get_representation() == representation)
		{
			return key;
		}
	}
	return {};
}

const std::shared_ptr<PieceData> PieceConfiguration::get_piece_data(const PieceType piece_type) const
{
	return this->data.at(piece_type);
}

const std::vector<PieceType>& PieceConfiguration::get_piece_types() const
{
	return this->piece_types;
}

#pragma endregion

#pragma region Notation

std::optional<Coordinate> PieceConfiguration::get_coordinate_from_notation(const std::string notation, const CoordinateValue board_height) const
{
	std::string lowered_notation = {};
	for (const auto& c : notation)
	{
		lowered_notation += static_cast<char>(std::tolower(c));
	}

	std::string row = "";
	std::string column = "";

	for (const auto& c : lowered_notation)
	{
		auto is_digit = '0' <= c && c <= '9';
		auto is_alphabet = 'a' <= c && c <= 'z';
		if ((!is_digit && !is_alphabet) || (is_alphabet && row.size() > 0))
		{
			return {};
		}
		if (is_alphabet)
		{
			column += c;
		}
		else
		{
			row += c;
		}
	}

	if (row.size() == 0 && column.size() == 0)
	{
		return {};
	}

	auto j = 0;
	for (const auto& x : column)
	{
		j *= 26;
		j += static_cast<int>(x) - static_cast<int>('a');
	}

	auto i = board_height - std::stoi(row);
	return Coordinate{ i, j };
}

std::string PieceConfiguration::get_notation_from_coordinate(const Coordinate coordinate, const CoordinateValue board_height) const
{
	return get_file_from_coordinate(coordinate.second) + get_rank_from_coordinate(coordinate.first, board_height);
}

std::string PieceConfiguration::get_file_from_coordinate(CoordinateValue file) const
{
	file++;
	std::string repr = "";
	while (file > 0)
	{
		auto r = (file - 1) % 26;
		repr = std::to_string(static_cast<char>(static_cast<int>('a') + r)) + repr;
		file = (file - r) / 26;
	}
	return repr;
}

std::string PieceConfiguration::get_rank_from_coordinate(const CoordinateValue rank, const CoordinateValue board_height) const
{
	return std::to_string(board_height - rank);
}

#pragma endregion
