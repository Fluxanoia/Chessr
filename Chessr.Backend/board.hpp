#pragma once

#include <vector>
#include "data.hpp"

class Board {
	private:
		std::vector<std::vector<Piece>> position;
	public:
		Board(const std::vector<std::vector<Piece>> position);
};

