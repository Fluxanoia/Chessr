from enum import auto
from typing import Any, Optional, Type, TypeVar, cast

from src.utils.enums import ArrayEnum
from src.utils.helpers import IntVector


class BoardDataType(ArrayEnum):
    GRID_POSITION = auto()

class BoardEventType(ArrayEnum):
    CLICK = auto()

T = TypeVar('T')

class BoardEvent():

    def __init__(self, event_type : BoardEventType, data : dict[BoardDataType, Any]) -> None:
        self.__event_type = event_type
        self.__data = data

    @property
    def type(self) -> BoardEventType:
        return self.__event_type

    @property
    def data(self) -> dict[BoardDataType, Any]:
        return self.__data

    @property
    def grid_position(self) -> Optional[IntVector]:
        return self.__get_casted_data(BoardDataType.GRID_POSITION, IntVector)

    def __get_casted_data(self, key : BoardDataType, data_type : Type[T]) -> Optional[T]:
        datum = self.__data.get(key, None)
        if datum is None:
            return None
        return cast(data_type, datum)
