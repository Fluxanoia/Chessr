from threading import Thread

import pygame as pg

from src.engine.factory import Factory
from src.engine.state_manager import StateManager
from src.engine.state_type import StateType


class Master:

    def __init__(self) -> None:

        factory = Factory.get()
        camera = factory.camera
        file_manager = factory.file_manager
        group_manager = factory.group_manager

        pg.init()
        pg.font.init()

        starting_screen_size = (1280, 720)
        screen = pg.display.set_mode(starting_screen_size, pg.RESIZABLE)
        camera.on_view_change(*starting_screen_size)
        
        pg.display.set_icon(file_manager.load_image('icon.png', True))
        pg.display.set_caption('Chessr')

        state_manager = StateManager()

        def load():
            state_manager.load_states()
            state_manager.set_state(StateType.MAIN_MENU)

        loading_thread = Thread(target=load)
        loading_thread.daemon = True
        loading_thread.start()

        running = True
        clock = pg.time.Clock()
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    continue
                if event.type == pg.WINDOWSIZECHANGED:
                    camera.on_view_change(
                        event.__dict__['x'],
                        event.__dict__['y'])
                state_manager.pass_event(event)
                
            state_manager.update()
            current_state = state_manager.state_type

            screen.fill((40, 40, 40))

            if current_state is not None:
                group_manager.update_groups(current_state)
                group_manager.draw_groups(screen, current_state)

            pg.display.flip()

            clock.tick(60)

        pg.quit()
