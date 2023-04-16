from typing import Iterable, Optional

from src.logic.piece_tag import PieceTag, PieceTagType
from src.utils.enums import PieceType, Side


class LogicPiece():

    def __init__(
        self,
        piece_type : PieceType,
        side : Side,
        tags : Optional[Iterable[PieceTag]] = None
    ):
        self.__piece_type = piece_type
        self.__side = side
        self.__tags : list[PieceTag] = [] if tags is None else list(tags)

    def delete(self) -> None:
        return

    def change_type(self, piece_type : PieceType) -> None:
        self.__piece_type = piece_type

    def update_tags(self) -> None:
        self.__tags = list(filter(lambda x : x.update(), self.__tags))

    def add_tag(self, tag : PieceTag) -> None:
        self.__tags.append(tag)

    def has_tag(self, tag_type : PieceTagType) -> bool:
        return tag_type in map(lambda x : x.type, self.__tags)

    def copy(self) -> "LogicPiece":
        copied_tags = map(lambda x : x.copy(), self.__tags)
        return LogicPiece(self.type, self.side, copied_tags)

    @property
    def type(self) -> PieceType:
        return self.__piece_type
    
    @property
    def side(self) -> Side:
        return self.__side
