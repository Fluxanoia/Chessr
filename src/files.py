import os

import pygame as pg

class FileManager:

    __instance = None

    @staticmethod
    def get_instance():
        if FileManager.__instance is None:
            raise Exception("No instance of FileManager.")
        return FileManager.__instance

    def __init__(self):
        if FileManager.__instance is not None:
            raise Exception("Invalid initialistion of FileManager.")
        else:
            if not pg.image.get_extended():
                raise SystemExit("Extended image types required.")
            FileManager.__instance = self

    def load_image(self, name, with_alpha = False):
        name = FileManager.get_images_path(name)
        try:
            surface = pg.image.load(name)
        except pg.error as e:
            raise SystemExit('Could not load image "%s" %s' % (name, pg.get_error())) from e
        return surface.convert_alpha() if with_alpha else surface.convert()

    @staticmethod
    def get_images_path(*args):
        return FileManager.get_path("images", *args)

    @staticmethod
    def get_path(*args):
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), *args)
    