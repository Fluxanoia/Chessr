from __future__ import division

import math
from enum import auto, unique

from src.utils.enums import ArrayEnum


@unique
class TweenType(ArrayEnum):
    LINEAR = auto()
    EASE_IN_QUAD = auto()
    EASE_OUT_QUAD = auto()
    EASE_IN_OUT_QUAD = auto()
    EASE_IN_CUBIC = auto()
    EASE_OUT_CUBIC = auto()
    EASE_IN_OUT_CUBIC = auto()
    EASE_IN_QUART = auto()
    EASE_OUT_QUART = auto()
    EASE_IN_OUT_QUART = auto()
    EASE_IN_QUINT = auto()
    EASE_OUT_QUINT = auto()
    EASE_IN_OUT_QUINT = auto()
    EASE_IN_SINE = auto()
    EASE_OUT_SINE = auto()
    EASE_IN_OUT_SINE = auto()
    EASE_IN_EXPO = auto()
    EASE_OUT_EXPO = auto()
    EASE_IN_OUT_EXPO = auto()
    EASE_IN_CIRC = auto()
    EASE_OUT_CIRC = auto()
    EASE_IN_OUT_CIRC = auto()
    EASE_IN_ELASTIC = auto()
    EASE_OUT_ELASTIC = auto()
    EASE_IN_OUT_ELASTIC = auto()
    EASE_IN_BACK = auto()
    EASE_OUT_BACK = auto()
    EASE_IN_OUT_BACK = auto()
    EASE_IN_BOUNCE = auto()
    EASE_OUT_BOUNCE = auto()
    EASE_IN_OUT_BOUNCE = auto()

# Adapted from https://github.com/asweigart/pytweening

def tween(tween_type : TweenType, n : float) -> float:
    if not 0.0 <= n <= 1.0:
        raise SystemExit('The tween argument must be between 0.0 and 1.0.')

    if tween_type is TweenType.LINEAR:
        return n

    if tween_type is TweenType.EASE_IN_QUAD:
        return n ** 2
    if tween_type is TweenType.EASE_OUT_QUAD:
        return -n * (n - 2)
    if tween_type is TweenType.EASE_IN_OUT_QUAD:
        return __ease_in_out_quad(n)

    if tween_type is TweenType.EASE_IN_CUBIC:
        return n ** 3
    if tween_type is TweenType.EASE_OUT_CUBIC:
        return (n - 1) ** 3 + 1
    if tween_type is TweenType.EASE_IN_OUT_CUBIC:
        return __ease_in_out_cubic(n)

    if tween_type is TweenType.EASE_IN_QUART:
        return n ** 4
    if tween_type is TweenType.EASE_OUT_QUART:
        return -((n - 1) ** 4 - 1)
    if tween_type is TweenType.EASE_IN_OUT_QUART:
        return __ease_in_out_quart(n)

    if tween_type is TweenType.EASE_IN_QUINT:
        return n ** 5
    if tween_type is TweenType.EASE_OUT_QUINT:
        return (n - 1) ** 5 + 1
    if tween_type is TweenType.EASE_IN_OUT_QUINT:
        return __ease_in_out_quint(n)

    if tween_type is TweenType.EASE_IN_SINE:
        return -1 * math.cos(n * math.pi / 2) + 1
    if tween_type is TweenType.EASE_OUT_SINE:
        return math.sin(n * math.pi / 2)
    if tween_type is TweenType.EASE_IN_OUT_SINE:
        return -0.5 * (math.cos(math.pi * n) - 1)

    if tween_type is TweenType.EASE_IN_EXPO:
        return __ease_in_expo(n)
    if tween_type is TweenType.EASE_OUT_EXPO:
        return __ease_out_expo(n)
    if tween_type is TweenType.EASE_IN_OUT_EXPO:
        return __ease_in_out_expo(n)

    if tween_type is TweenType.EASE_IN_CIRC:
        return -1 * (math.sqrt(1 - n * n) - 1)
    if tween_type is TweenType.EASE_OUT_CIRC:
        return __ease_out_circ(n)
    if tween_type is TweenType.EASE_IN_OUT_CIRC:
        return __ease_in_out_circ(n)

    if tween_type is TweenType.EASE_IN_ELASTIC:
        return __ease_in_elastic(n)
    if tween_type is TweenType.EASE_OUT_ELASTIC:
        return __ease_out_elastic(n)
    if tween_type is TweenType.EASE_IN_OUT_ELASTIC:
        return __ease_in_out_elastic(n)

    if tween_type is TweenType.EASE_IN_BACK:
        return __ease_in_back(n)
    if tween_type is TweenType.EASE_OUT_BACK:
        return __ease_out_back(n)
    if tween_type is TweenType.EASE_IN_OUT_BACK:
        return __ease_in_out_back(n)

    if tween_type is TweenType.EASE_IN_BOUNCE:
        return __ease_in_bounce(n)
    if tween_type is TweenType.EASE_OUT_BOUNCE:
        return __ease_out_bounce(n)
    if tween_type is TweenType.EASE_IN_OUT_BOUNCE:
        return __ease_in_out_bounce(n)

    raise SystemExit(f'Unexpected TweenType \'{tween_type}\'.')

def __ease_in_out_quad(n : float) -> float:
    if n < 0.5:
        return 2 * n ** 2
    else:
        n = n * 2 - 1
        return -0.5 * (n * (n - 2) - 1)

def __ease_in_out_cubic(n : float) -> float:
    n = 2 * n
    if n < 1:
        return 0.5 * n ** 3
    else:
        n = n - 2
        return 0.5 * (n ** 3 + 2)

def __ease_in_out_quart(n : float) -> float:
    n = 2 * n
    if n < 1:
        return 0.5 * n**4
    else:
        n = n - 2
        return -0.5 * (n**4 - 2)

def __ease_in_out_quint(n : float) -> float:
    n = 2 * n
    if n < 1:
        return 0.5 * n ** 5
    else:
        n = n - 2
        return 0.5 * (n ** 5 + 2)

def __ease_in_expo(n : float) -> float:
    if n == 0:
        return 0
    else:
        return 2 ** (10 * (n - 1))

def __ease_out_expo(n : float) -> float:
    if n == 1:
        return 1
    else:
        return -(2 ** (-10 * n)) + 1

def __ease_in_out_expo(n : float) -> float:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        n = n * 2
        if n < 1:
            return 0.5 * 2 ** (10 * (n - 1))
        else:
            n -= 1
            return 0.5 * (-1 * (2 ** (-10 * n)) + 2)

def __ease_out_circ(n : float) -> float:
    n -= 1
    return math.sqrt(1 - (n * n))

def __ease_in_out_circ(n : float) -> float:
    n = n * 2
    if n < 1:
        return -0.5 * (math.sqrt(1 - n ** 2) - 1)
    else:
        n = n - 2
        return 0.5 * (math.sqrt(1 - n ** 2) + 1)

def __ease_in_elastic(n : float, amplitude : float = 1, period : float = 0.3) -> float:
    return 1 - __ease_out_elastic(1 - n, amplitude = amplitude, period = period)

def __ease_out_elastic(n : float, amplitude : float = 1, period : float = 0.3) -> float:
    if amplitude < 1:
        amplitude = 1
        s = period / 4
    else:
        s = period / (2 * math.pi) * math.asin(1 / amplitude)
    return amplitude * 2 ** (-10 * n) * math.sin((n - s) * (2 * math.pi / period)) + 1

def __ease_in_out_elastic(n : float, amplitude : float = 1, period : float = 0.5) -> float:
    n *= 2
    if n < 1:
        return __ease_in_elastic(n, amplitude = amplitude, period = period) / 2
    else:
        return __ease_out_elastic(n - 1, amplitude = amplitude, period = period) / 2 + 0.5

def __ease_in_back(n : float, s : float = 1.70158) -> float:
    return n * n * ((s + 1) * n - s)

def __ease_out_back(n : float, s : float = 1.70158) -> float:
    n = n - 1
    return n * n * ((s + 1) * n + s) + 1

def __ease_in_out_back(n : float, s : float = 1.70158) -> float:
    n = n * 2
    if n < 1:
        s *= 1.525
        return 0.5 * (n * n * ((s + 1) * n - s))
    else:
        n -= 2
        s *= 1.525
        return 0.5 * (n * n * ((s + 1) * n + s) + 2)

def __ease_in_bounce(n : float) -> float:
    return 1 - __ease_out_bounce(1 - n)

def __ease_out_bounce(n : float) -> float:
    if n < (1 / 2.75):
        return 7.5625 * n * n
    elif n < (2 / 2.75):
        n -= (1.5 / 2.75)
        return 7.5625 * n * n + 0.75
    elif n < (2.5 / 2.75):
        n -= (2.25 / 2.75)
        return 7.5625 * n * n + 0.9375
    else:
        n -= (2.65 / 2.75)
        return 7.5625 * n * n + 0.984375

def __ease_in_out_bounce(n : float) -> float:
    if n < 0.5:
        return __ease_in_bounce(n * 2) * 0.5
    else:
        return __ease_out_bounce(n * 2 - 1) * 0.5 + 0.5
