#include "piece_data.hpp"

std::shared_ptr<Move> create_basic_move(
	const MoveType move_type,
	const MoveStyle move_style,
	const Coordinate move_vector,
	const Coordinate from,
	const Coordinate to,
	bool attack)
{
	std::vector<std::shared_ptr<Consequence>> consequences = { };
	if (attack)
	{
		consequences.push_back(std::make_shared<RemoveConsequence>(to));
	}
	consequences.push_back(std::make_shared<MoveConsequence>(move_type, move_style, move_vector, from, to));
	return std::make_shared<Move>(consequences);
}

#pragma region Constructor

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
	flipped_attack_rays(Maths::flip_vectors(attack_rays)),
	flipped_attack_jumps(Maths::flip_vectors(attack_jumps)),
	flipped_push_rays(Maths::flip_vectors(push_rays)),
	flipped_push_jumps(Maths::flip_vectors(push_jumps))
{
}

#pragma endregion

#pragma region Getters

const std::string& PieceData::get_representation() const
{
	return this->representation;
}

std::vector<Coordinate> PieceData::get_vectors(const MoveType type, const MoveStyle style, const Player& player) const
{
	const auto& context_attack_rays = player == Player::WHITE ? this->attack_rays : this->flipped_attack_rays;
	const auto& context_attack_jumps = player == Player::WHITE ? this->attack_jumps : this->flipped_attack_jumps;
	const auto& context_push_rays = player == Player::WHITE ? this->push_rays : this->flipped_push_rays;
	const auto& context_push_jumps = player == Player::WHITE ? this->push_jumps : this->flipped_push_jumps;

	std::vector<Coordinate> vectors;
	switch (type)
	{
		case MoveType::ALL:
		{
			if (style == MoveStyle::ALL || style == MoveStyle::RAY)
			{
				vectors.insert(vectors.end(), context_push_rays.begin(), context_push_rays.end());
				vectors.insert(vectors.end(), context_attack_rays.begin(), context_attack_rays.end());
			}
			if (style == MoveStyle::ALL || style == MoveStyle::JUMP)
			{
				vectors.insert(vectors.end(), context_push_jumps.begin(), context_push_jumps.end());
				vectors.insert(vectors.end(), context_attack_jumps.begin(), context_attack_jumps.end());
			}
			break;
		}
		case MoveType::PUSH:
		{
			if (style == MoveStyle::ALL || style == MoveStyle::RAY)
			{
				vectors.insert(vectors.end(), context_push_rays.begin(), context_push_rays.end());
			}
			if (style == MoveStyle::ALL || style == MoveStyle::JUMP)
			{
				vectors.insert(vectors.end(), context_push_jumps.begin(), context_push_jumps.end());
			}
			break;
		}
		case MoveType::ATTACK:
		{
			if (style == MoveStyle::ALL || style == MoveStyle::RAY)
			{
				vectors.insert(vectors.end(), context_attack_rays.begin(), context_attack_rays.end());
			}
			if (style == MoveStyle::ALL || style == MoveStyle::JUMP)
			{
				vectors.insert(vectors.end(), context_attack_jumps.begin(), context_attack_jumps.end());
			}
			break;
		}
	}
	return vectors;
}

#pragma endregion

#pragma region Generating Moves

std::vector<Coordinate> PieceData::get_ray(
	const Boards& boards,
	const Player& player,
	const Coordinate& ray,
	const Coordinate& coordinate,
	const std::optional<Coordinate>& ignore_coordinate,
	const bool attack) const
{
	std::vector<Coordinate> cells = {};
	auto cell = Maths::add_coordinates(coordinate, ray);
	const auto& board = boards.get_current_board();
	while (Maths::in_bounds(board.get_dimensions(), cell))
	{
		const auto& [i, j] = cell;
		auto ignore = ignore_coordinate.has_value() && ignore_coordinate.value() == cell;

		if (ignore || !board.has_piece(cell))
		{
			cells.push_back({ i, j });
		}
		else
		{
			if (attack && board.get_piece(cell).get_player() != player)
			{
				cells.push_back({ i, j });
			}

			break;
		}

		cell = Maths::add_coordinates(cell, ray);
	}

	return cells;
}

std::optional<Coordinate> PieceData::get_jump(
	const Boards& boards,
	const Player& player,
	const Coordinate& jump,
	const Coordinate& coordinate,
	const bool attack) const
{
	auto cell = Maths::add_coordinates(coordinate, jump);
	const auto& board = boards.get_current_board();
	if (!Maths::in_bounds(board.get_dimensions(), cell))
	{
		return {};
	}

	if (!board.has_piece(cell) || (attack && board.get_piece(cell).get_player() != player))
	{
		return cell;
	}

	return {};
}

std::vector<std::shared_ptr<Move>> PieceData::get_moves(
	const Boards& boards,
	const Player& player,
	const Coordinate& coordinate,
	const MoveType move_type,
	const MoveStyle move_style,
	const std::optional<Coordinate>& ignore_coordinate) const
{
	std::vector<std::shared_ptr<Move>> moves = {};

	if (move_type == MoveType::ALL)
	{
		const auto pushes = get_moves(boards, player, coordinate, MoveType::PUSH, move_style, ignore_coordinate);
		const auto attacks = get_moves(boards, player, coordinate, MoveType::ATTACK, move_style, ignore_coordinate);
		moves.insert(moves.end(), pushes.begin(), pushes.end());
		moves.insert(moves.end(), attacks.begin(), attacks.end());
		return moves;
	}

	const auto attack = move_type == MoveType::ATTACK;
	const auto& rays = move_style == MoveStyle::ALL || move_style == MoveStyle::RAY
		? get_vectors(move_type, MoveStyle::RAY, player)
		: std::vector<Coordinate>{};
	const auto& jumps = move_style == MoveStyle::ALL || move_style == MoveStyle::JUMP
		? get_vectors(move_type, MoveStyle::JUMP, player)
		: std::vector<Coordinate>{};

	for (auto& ray : rays)
	{
		const auto cells = get_ray(boards, player, ray, coordinate, ignore_coordinate, attack);
		for (const auto& cell : cells)
		{
			moves.push_back(create_basic_move(move_type, MoveStyle::RAY, ray, coordinate, cell, attack));
		}
	}

	for (auto& jump : jumps)
	{
		auto cell = get_jump(boards, player, jump, coordinate, attack);
		if (cell.has_value())
		{
			moves.push_back(create_basic_move(move_type, MoveStyle::JUMP, jump, coordinate, cell.value(), attack));
		}
	}

	return moves;
}

#pragma endregion

#pragma region Pawn Specific Methods

PawnPieceData::PawnPieceData(
	const std::string representation,
	const std::vector<Coordinate> attack_rays,
	const std::vector<Coordinate> attack_jumps,
	const std::vector<Coordinate> push_rays,
	const std::vector<Coordinate> push_jumps) : PieceData(representation, attack_rays, attack_jumps, push_rays, push_jumps)
{
}

std::vector<std::shared_ptr<Move>> PawnPieceData::get_moves(
	const Boards& boards,
	const Player& player,
	const Coordinate& coordinate,
	const MoveType move_type,
	const MoveStyle move_style,
	const std::optional<Coordinate>& ignore_coordinate) const
{
	const auto& current_board = boards.get_current_board();
	auto moves = PieceData::get_moves(boards, player, coordinate, move_type, move_style, ignore_coordinate);

	if (move_type == MoveType::ALL || move_type == MoveType::ATTACK)
	{
		const auto& last_move = boards.get_last_move();
		if (!last_move.has_value() || last_move.value()->get_property() != MoveProperty::DOUBLE_MOVE)
		{
			return moves;
		}

		const auto& last_move_destination = [&last_move]()
		{
			const auto& move_consequence = last_move.value()->get_move_consequence();
			return move_consequence.has_value()
				? std::optional<Coordinate>{ move_consequence.value()->get_to() }
				: std::optional<Coordinate>{};
		}();

		if (!last_move_destination.has_value())
		{
			return moves;
		}

		for (const auto& direction : std::vector<Coordinate>{ Maths::LEFT, Maths::RIGHT })
		{
			const auto cell = Maths::add_coordinates(coordinate, direction);
			if (!current_board.has_piece(cell) || cell != last_move_destination.value())
			{
				continue;
			}

			const auto& piece = current_board.get_piece(cell);
			if (piece.get_player() == player || piece.get_type() != PieceType::PAWN)
			{
				continue;
			}

			const auto move_vector = Maths::add_coordinates(direction, Maths::flip_vector(Maths::UP, player));
			const auto pawn_destination = Maths::add_coordinates(coordinate, move_vector);

			auto pawn_consequence = std::make_shared<MoveConsequence>(MoveType::ATTACK, MoveStyle::JUMP, move_vector, coordinate, pawn_destination);
			auto remove_consequence = std::make_shared<RemoveConsequence>(cell);

			std::vector<std::shared_ptr<Consequence>> consequences = { pawn_consequence, remove_consequence };
			auto move = std::make_shared<Move>(consequences, MoveProperty::EN_PASSANT);

			moves.push_back(move);
		}
	}
	
	if (move_type == MoveType::ALL || move_type == MoveType::PUSH)
	{
		auto it = moves.begin();
		const auto final_rank = player == Player::WHITE
			? 0
			: current_board.get_dimensions().second - 1;
		while (it != moves.end())
		{
			const auto& move = (*it)->get_move_consequence();
			if (!move.has_value())
			{
				continue;
			}
			if (move.value()->get_to().first == final_rank)
			{
				it = moves.erase(it);
				std::vector<std::shared_ptr<Consequence>> consequences = { move.value() };
				moves.insert(it, std::make_shared<Move>(consequences, MoveProperty::PROMOTION));
			}
			else
			{
				it++;
			}
		}

		if (!boards.has_moved(coordinate))
		{
			const auto move_vector = Maths::flip_vector({ -2, 0 }, player);
			
			auto consequence = std::make_shared<MoveConsequence>(MoveType::PUSH, MoveStyle::JUMP, move_vector, coordinate, Maths::add_coordinates(coordinate, move_vector));
			
			std::vector<std::shared_ptr<Consequence>> consequences = { consequence };
			auto move = std::make_shared<Move>(consequences, MoveProperty::DOUBLE_MOVE);
			
			moves.push_back(move);
		}
	}

	return moves;
}

#pragma endregion

#pragma region King Specific Methods

KingPieceData::KingPieceData(
	const std::string representation,
	const std::vector<Coordinate> attack_rays,
	const std::vector<Coordinate> attack_jumps,
	const std::vector<Coordinate> push_rays,
	const std::vector<Coordinate> push_jumps) : PieceData(representation, attack_rays, attack_jumps, push_rays, push_jumps)
{
}

std::vector<std::shared_ptr<Move>> KingPieceData::get_moves(
	const Boards& boards,
	const Player& player,
	const Coordinate& coordinate,
	const MoveType move_type,
	const MoveStyle move_style,
	const std::optional<Coordinate>& ignore_coordinate) const
{
	const auto& current_board = boards.get_current_board();
	auto moves = PieceData::get_moves(boards, player, coordinate, move_type, move_style, ignore_coordinate);
	if (move_type == MoveType::ATTACK || boards.has_moved(coordinate) || current_board.is_in_check())
	{
		return moves;
	}

	for (const auto& direction : std::vector<Coordinate>{ Maths::LEFT, Maths::RIGHT })
	{
		const auto ray = PieceData::get_ray(
			boards,
			player,
			direction,
			coordinate,
			{},
			false);

		if (ray.size() < 2 || !current_board.has_piece(ray.back()))
		{
			continue;
		}

		const auto& rook_coordinate = ray.back();
		const auto& piece = current_board.get_piece(rook_coordinate);
		if (piece.get_player() != player
			|| piece.get_type() != PieceType::ROOK
			|| boards.has_moved(rook_coordinate))
		{
			continue;
		}

		const auto king_vector = Maths::subtract_coordinates(ray.at(1), coordinate);
		const auto rook_vector = Maths::subtract_coordinates(ray.at(0), rook_coordinate);

		auto king_consequence = std::make_shared<MoveConsequence>(MoveType::PUSH, MoveStyle::JUMP, king_vector, coordinate, ray.at(1));
		auto rook_consequence = std::make_shared<MoveConsequence>(MoveType::PUSH, MoveStyle::JUMP, rook_vector, rook_coordinate, ray.at(0));

		std::vector<std::shared_ptr<Consequence>> consequences = { king_consequence, rook_consequence };
		auto move = std::make_shared<Move>(consequences, MoveProperty::CASTLE);

		moves.push_back(move);
	}

	return moves;
}

#pragma endregion
