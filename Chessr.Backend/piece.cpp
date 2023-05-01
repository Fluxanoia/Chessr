#include "piece.hpp"

Piece::Piece(const PieceType type, const Player player) : type(type), player(player) {}

const PieceType& Piece::get_type() const
{
	return this->type;
}

const Player& Piece::get_player() const
{
	return this->player;
}
