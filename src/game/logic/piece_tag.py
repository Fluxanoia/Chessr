from enum import auto

from src.utils.enums import ArrayEnum


class PieceTagType(ArrayEnum):
    HAS_MOVED = auto()
    EN_PASSANT = auto()

class PieceTag():

    def __init__(self, tag_type : PieceTagType):
        self.__tag_type = tag_type

    def update_move(self) -> bool:
        return True

    @property
    def type(self) -> PieceTagType:
        return self.__tag_type

    @staticmethod
    def get_tag(tag_type : PieceTagType) -> 'PieceTag':
        if tag_type == PieceTagType.HAS_MOVED:
            return HasMovedPieceTag()
        if tag_type == PieceTagType.EN_PASSANT:
            return EnPassantPieceTag()
        raise SystemExit(f'Unexpected piece tag type, \'{tag_type}\'.')

class HasMovedPieceTag(PieceTag):

    def __init__(self):
        super().__init__(PieceTagType.HAS_MOVED)

class EnPassantPieceTag(PieceTag):

    def __init__(self):
        super().__init__(PieceTagType.EN_PASSANT)

    def update_move(self) -> bool:
        return False