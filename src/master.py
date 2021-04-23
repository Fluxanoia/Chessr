import pygame as pg
from src.files import FileManager

WINDOW_SIZE = pg.Rect(0, 0, 1024, 1024)

class Master:

    def __init__(self):
        self.__files = FileManager()

        pg.init()
        pg.display.set_caption("Chessr")
        screen = pg.display.set_mode(WINDOW_SIZE.size)
        pg.display.set_icon(self.__files.load_image("icon.png", True))

        self.__spritesheet = self.__files.load_image("sprites.png", True)

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    continue
            screen.fill((40, 40, 40))
            pg.display.flip()

        pg.quit()
