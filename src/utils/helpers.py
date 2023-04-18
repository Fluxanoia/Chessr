from typing import Any, Collection, Iterable, TypeVar, Union

import pygame as pg

Numeric = Union[int, float]
FloatVector = tuple[float, float]
IntVector = tuple[int, int]

Colour = tuple[int, int, int]

def add_vectors(x : IntVector, y : IntVector) -> IntVector:
    return (x[0] + y[0], x[1] + y[1])

def scale_rect(rect : pg.rect.Rect, scale : float) -> None:
    rect.update(rect.x * scale, rect.y * scale, rect.w * scale, rect.h * scale)

T = TypeVar('T')
def pad(arr : Collection[T], size : int, default : T = None) -> tuple[T, ...]:
    return tuple([*arr] + [default] * (size - len(arr)))

U = TypeVar('U', bound = Numeric)
def clamp(x : U, l : U, u : U) -> U:
    return l if x < l else (u if x > u else x)

def inbounds(grid_width : int, grid_height : int, cell : IntVector) -> bool:
    i, j = cell
    return 0 <= i < grid_height and 0 <= j < grid_width

def get_coord_text(gxy : IntVector, board_height : int) -> str:
    i, j = gxy
    return chr(ord('A') + j) + str(board_height - i)

def is_empty(x : Iterable[Any]) -> bool:
    for _ in x:
        return False
    return True
