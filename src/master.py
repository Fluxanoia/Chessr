import pygame as pg

from src.engine.config import Config
from src.engine.factory import Factory
from src.engine.game_manager import GameManager


class Master:

    def __init__(self):
        factory = Factory.get()

        pg.init()
        pg.font.init()
        pg.display.set_caption('Chessr')
        screen = pg.display.set_mode(Config.get_window_dimensions())
        pg.display.set_icon(factory.file_manager.load_image('icon.png', True))

        game_manager = GameManager()
        game_manager.start()

        running = True
        clock = pg.time.Clock()
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    continue
                game_manager.pass_event(event)
                
            game_manager.update()
            factory.group_manager.update_groups()

            screen.fill((40, 40, 40))
            factory.group_manager.draw_groups(screen)
            pg.display.flip()

            clock.tick(Config.get_fps())

        pg.quit()
