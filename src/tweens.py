from enum import Enum, unique
import pytweening as pt
from src.timer import Timer

class Tween(Timer):

    def __init__(self, _type, start, end, duration, pause=0, chain=None):
        super().__init__(duration, pause)
        self.__type = _type
        self.__chain = chain
        self.__start = start
        self.__end = end
        self.restart()

    def value(self):
        percentage = self.__type(super().value() / float(self.get_duration()))
        def tween(x): return x[0] + (x[1] - x[0]) * percentage
        for i in (list, tuple):
            if isinstance(self.__start, i) and isinstance(self.__end, i):
                return i(map(tween, zip(self.__start, self.__end)))
        return tween((self.__start, self.__end))

    def get_chained(self):
        if self.__chain is not None:
            self.__chain.restart()
        return self.__chain

@unique
class TweenType(Enum):
    LINEAR = pt.linear
    EASE_IN_QUAD = pt.easeInQuad
    EASE_OUT_QUAD = pt.easeOutQuad
    EASE_IN_OUT_QUAD = pt.easeInOutQuad
    EASE_IN_CUBIC = pt.easeInCubic
    EASE_OUT_CUBIC = pt.easeOutCubic
    EASE_IN_OUT_CUBIC = pt.easeInOutCubic
    EASE_IN_QUART = pt.easeInQuart
    EASE_OUT_QUART = pt.easeOutQuart
    EASE_IN_OUT_QUART = pt.easeInOutQuad
    EASE_IN_QUINT = pt.easeInQuint
    EASE_OUT_QUINT = pt.easeOutQuint
    EASE_IN_OUT_QUINT = pt.easeInOutQuart
    EASE_IN_SINE = pt.easeInSine
    EASE_OUT_SINE = pt.easeOutSine
    EASE_IN_OUT_SINE = pt.easeInOutSine
    EASE_IN_EXPO = pt.easeInExpo
    EASE_OUT_EXPO = pt.easeOutExpo
    EASE_IN_OUT_EXPO = pt.easeInOutExpo
    EASE_IN_CIRC = pt.easeInCirc
    EASE_OUT_CIRC = pt.easeOutCirc
    EASE_IN_OUT_CIRC = pt.easeInOutCirc
    EASE_IN_ELASTIC = pt.easeInElastic
    EASE_OUT_ELASTIC = pt.easeOutElastic
    EASE_IN_OUT_ELASTIC = pt.easeInOutElastic
    EASE_IN_BACK = pt.easeInBack
    EASE_OUT_BACK = pt.easeOutBack
    EASE_IN_OUT_BACK = pt.easeInOutBack
    EASE_IN_BOUNCE = pt.easeInBounce
    EASE_OUT_BOUNCE = pt.easeOutBounce
    EASE_IN_OUT_BOUNCE = pt.easeInOutBounce
