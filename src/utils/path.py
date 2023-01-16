import os
from typing import TypeAlias, Union

PathLike : TypeAlias = Union['Path', tuple[str, ...], str]

class Path:

    def __init__(self, pathlike : PathLike):
        self.__segments = self.__get_segments_from_pathlike(pathlike)

    def get_relative_path(self, pathlike : PathLike) -> 'Path':
        segments = (*self.__segments, *self.__get_segments_from_pathlike(pathlike))
        return Path(segments)

    def get_literal_path(self) -> str:
        path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(path, *self.__segments)

    def get_segments(self) -> tuple[str, ...]:
        return self.__segments

    def __get_segments_from_pathlike(self, pathlike : PathLike) -> tuple[str, ...]:
        if isinstance(pathlike, Path):
            pathlike = pathlike.get_segments()
        if not isinstance(pathlike, tuple):
            pathlike = (pathlike,)
        return pathlike
