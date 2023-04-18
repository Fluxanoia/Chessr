import pygame as pg

from src.engine.factory import Factory
from src.engine.state_manager import StateManager


class Master:

    def __init__(self) -> None:
        factory = Factory.get()

        pg.init()
        pg.font.init()

        starting_screen_size = (1280, 720)
        screen = pg.display.set_mode(starting_screen_size, pg.RESIZABLE)
        factory.camera.on_view_change(*starting_screen_size)
        
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
                if event.type == pg.WINDOWSIZECHANGED:
                    factory.camera.on_view_change(event.__dict__['x'], event.__dict__['y'])
                state_manager.pass_event(event)
                
            state_manager.update()
            factory.group_manager.update_groups(state_manager.state_type)

            screen.fill((40, 40, 40))
            factory.group_manager.draw_groups(screen, state_manager.state_type)

            pg.display.flip()

            clock.tick(60)

        pg.quit()
