from collections.abc import Sequence
from typing import Callable, Optional, TypeAlias

from src.utils.helpers import FloatVector
from src.utils.timer import Timer
from src.utils.tween_functions import TweenType, tween

Tweenable : TypeAlias = float | Sequence[float]

class Tween(Timer):

    def __init__(
        self,
        tween_type : TweenType,
        start : Tweenable,
        end : Tweenable,
        duration : int,
        pause : int = 0,
        chain : Optional['Tween'] = None,
        callback : Optional[Callable[[], None]] = None
    ) -> None:
        super().__init__(duration, pause)
        self.__type = tween_type
        self.__chain = chain
        self.__callback = callback
        self.__start = start if isinstance(start, Sequence) else (start,)
        self.__end = end if isinstance(end, Sequence) else (end,)
        self.restart()

    @property
    def value(self) -> float:
        return self.__get_single_value(self.__get_values())
    
    @property
    def values(self) -> Tweenable:
        return self.__get_values()

    @property
    def start_value(self) -> float:
        return self.__get_single_value(self.__start)

    @property
    def start_values(self) -> Tweenable:
        return self.__start

    @property
    def end_value(self) -> float:
        return self.__get_single_value(self.__end)

    @property
    def end_values(self) -> Tweenable:
        return self.__end

    def get_callback(self) -> Optional[Callable[[], None]]:
        return self.__callback

    def get_chained(self) -> Optional['Tween']:
        if self.__chain is not None:
            self.__chain.restart()
        return self.__chain
    
    def __get_values(self) -> Tweenable:
        percentage = tween(self.__type, self.get_percentage_done())

        def interpolate(x : FloatVector) -> float:
            return x[0] + percentage * (x[1] - x[0])

        return tuple(map(interpolate, zip(self.__start, self.__end, strict = True)))

    def __get_single_value(self, v : Tweenable) -> float:
        if isinstance(v, float):
            return v
        if len(v) == 1:
            return v[0]
        raise SystemExit('The tween object had multiple values when one was expected.')
