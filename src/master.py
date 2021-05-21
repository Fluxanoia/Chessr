import pygame as pg
from src.game.board import Board
from src.game.logic import Logic
from src.utils.files import FileManager
from src.utils.groups import Groups
from src.utils.globals import Globals
from src.utils.spritesheet import Spritesheet

class Master:

    def __init__(self):
        self.__globals = Globals()
        self.__files = FileManager()
        self.__logic = Logic()

        pg.init()
        pg.display.set_caption("Chessr")
        self.__screen = pg.display.set_mode(self.__globals.get_window_size())
        pg.display.set_icon(self.__files.load_image("icon.png", True))

        self.__groups = Groups()
        self.__spritesheet = Spritesheet()
        self.__clock = pg.time.Clock()
        self.__board = Board()

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    continue
                if event.type == pg.MOUSEBUTTONDOWN: self.__board.pressed(event)
                if event.type == pg.MOUSEBUTTONUP: self.__board.released(event)
            self.__board.update()
            self.__groups.update()
            self.__screen.fill((40, 40, 40))
            self.__groups.draw(self.__screen)
            pg.display.flip()
            self.__clock.tick(self.__globals.get_fps())

        pg.quit()
