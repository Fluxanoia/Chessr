import pygame as pg

class Timer():

    def __init__(self, duration, pause = 0):
        self.__duration = duration
        self.__pause = pause
        self.restart()

    def restart(self):
        self.__start_time = pg.time.get_ticks() + self.__pause

    def has_not_started(self):
        return pg.time.get_ticks() <= self.__start_time
    def finished(self):
        return pg.time.get_ticks() >= self.__start_time + self.__duration

    def value(self):
        if self.has_not_started(): return 0
        if self.finished(): return self.__duration
        return pg.time.get_ticks() - self.__start_time

    def value_as_percentage(self):
        return self.value() / float(self.__duration)

    def get_duration(self): return self.__duration
    def get_pause(self): return self.__pause
