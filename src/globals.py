from enum import auto
from src.enum import CountEnum

def instance(_type):
    return Singleton.get_instance(_type)

class Singleton:

    __instances = {}

    @staticmethod
    def get_instance(_type):
        if _type in Singleton.__instances:
            return Singleton.__instances[_type]
        raise Exception("No instance of Singleton.")

    def __init__(self):
        if type(self) in Singleton.__instances:
            raise Exception("Invalid initialisation of Singleton.")
        Singleton.__instances[type(self)] = self

class MouseButton(CountEnum):
    LEFT = auto()
    MIDDLE = auto()
    RIGHT = auto()
    SCROLL_UP = auto()
    SCROLL_DOWN = auto()

class Globals(Singleton):

    def __init__(self):
        super().__init__()
        self.__fps = 60
        self.__window_size = (1024, 1024)

    def get_fps(self): return self.__fps
    def get_window_size(self): return self.__window_size

def scale_rect(rect, scale):
    rect.update(rect.x * scale, rect.y * scale, rect.w * scale, rect.h * scale)

def pad(arr, size, default = None):
    return tuple([*arr] + [default] * (size - len(arr)))

def clamp(x, l, u):
    return l if x < l else (u if x > u else x)
