from collections.abc import Sequence
from typing import Optional, TypeAlias

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
        chain : Optional['Tween'] = None
    ) -> None:
        super().__init__(duration, pause)
        self.__type = tween_type
        self.__chain = chain
        self.__start = start if isinstance(start, Sequence) else (start,)
        self.__end = end if isinstance(end, Sequence) else (end,)
        self.restart()

    def value(self) -> Tweenable:
        percentage = tween(self.__type, self.get_percentage_done())

        def interpolate(x : FloatVector) -> float:
            return x[0] + percentage * (x[1] - x[0])

        return tuple(map(interpolate, zip(self.__start, self.__end, strict = True)))

    def get_single_value(self) -> float:
        v = self.value()
        if isinstance(v, float):
            return v
        if len(v) == 1:
            return v[0]
        raise SystemExit('The tween object had multiple values when one was expected.')

    def get_chained(self) -> Optional['Tween']:
        if self.__chain is not None:
            self.__chain.restart()
        return self.__chain
