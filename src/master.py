import pygame as pg

from src.engine.config import Config
from src.engine.factory import Factory
from src.engine.state_manager import StateManager


class Master:

    def __init__(self) -> None:
        factory = Factory.get()

        pg.init()
        pg.font.init()

        screen = pg.display.set_mode(Config.get_window_dimensions())
        
        pg.display.set_icon(factory.file_manager.load_image('icon.png', True))
        pg.display.set_caption('Chessr')

        state_manager = StateManager()

        running = True
        clock = pg.time.Clock()
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    continue
                state_manager.pass_event(event)
                
            state_manager.update()
            factory.group_manager.update_groups(state_manager.state_type)

            screen.fill((40, 40, 40))
            factory.group_manager.draw_groups(screen, state_manager.state_type)
            pg.display.flip()

            clock.tick(Config.get_fps())

        pg.quit()
