import pygame as pg
from src.files import FileManager
from src.board import Board
from src.groups import Groups
from src.globals import Globals
from src.spritesheet import Spritesheet

class Master:

    def __init__(self):
        self.__globals = Globals()
        self.__files = FileManager()

        pg.init()
        pg.display.set_caption("Chessr")
        self.__screen = pg.display.set_mode(self.__globals.get_window_size())
        pg.display.set_icon(self.__files.load_image("icon.png", True))

        self.__groups = Groups()
        self.__spritesheet = Spritesheet()

        self.__board = Board()

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    continue
            self.__board.update()
            self.__groups.update()
            self.__screen.fill((40, 40, 40))
            self.__groups.draw(self.__screen)
            pg.display.flip()

        pg.quit()
