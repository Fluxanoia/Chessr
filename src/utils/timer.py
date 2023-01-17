import pygame as pg


class Timer():

    def __init__(self, duration : int, pause : int = 0) -> None:
        self.__duration = duration
        self.__pause = pause
        self.restart()

    def restart(self) -> None:
        self.__start_time = pg.time.get_ticks() + self.__pause

    def has_not_started(self) -> bool:
        return pg.time.get_ticks() <= self.__start_time
    def finished(self) -> bool:
        return pg.time.get_ticks() >= self.__start_time + self.__duration

    def current_time(self) -> int:
        if self.has_not_started():
            return 0
        if self.finished():
            return self.__duration
        return pg.time.get_ticks() - self.__start_time

    def get_percentage_done(self) -> float:
        return self.current_time() / float(self.__duration)
