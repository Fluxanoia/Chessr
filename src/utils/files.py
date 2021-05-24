import os
import pygame as pg
from src.utils.globals import Singleton

class FileManager(Singleton):

    DELIM = ':'
    DEFAULT_FONT = "Kenney Blocks.ttf"

    def __init__(self):
        super().__init__()
        self.__fonts = {}
        if not pg.image.get_extended():
            raise SystemExit("Extended image types required.")

    def load_default_font(self, pt = 16):
        return self.load_font(FileManager.DEFAULT_FONT, pt)
    def load_font(self, name, pt):
        if not name in self.__fonts:
            self.__fonts[name] = {}
        if not pt in self.__fonts[name]:
            font = pg.font.Font(self.__get_path(name, False, ("files", "fonts")), int(pt))
            self.__fonts[name][pt] = font
        return self.__fonts[name][pt]
        

    def load_image(self, names, with_alpha = False, raw = False):
        path = self.__get_path(names, raw, "images")
        try:
            surface = pg.image.load(path)
        except pg.error as e:
            raise SystemExit('Could not load image "%s" %s' % (path, pg.get_error())) from e
        return surface.convert_alpha() if with_alpha else surface.convert()

    def load_board(self, names, raw = False):
        return self.load_file(self.__get_path(names, raw, ("files", "boards")), raw = True)

    def load_file(self, names, default = None, raw = False):
        path = self.__get_path(names, raw)
        if not self.__exists(path):
            if not default is None:
                self.overwrite_file(path, default, raw = True)
            return default
        data = {}
        with open(path, 'r') as file:
            for line in file:
                args = line.split(FileManager.DELIM, 1)
                if len(args) == 2:
                    data[args[0]] = args[1].strip('\n')
        rewrite = False
        if not default is None:
            for k in default.keys():
                if not k in data:
                    rewrite = True
                    data[k] = default[k]
        if rewrite:
            self.overwrite_file(path, data, raw = True)
        return data

    def overwrite_file(self, names, content, raw = False):
        path = self.__get_path(names, raw)
        if not self.__exists(path):
            self.__mkdirs(path)
        with open(path, "w+") as file:
            for (x, y) in content.items():
                file.write(str(x) + FileManager.DELIM + str(y) + '\n')

    def __mkdirs(self, path):
        os.makedirs(os.path.dirname(path), exist_ok = True)
    def __exists(self, path):
        return os.path.exists(path)
    def __get_path(self, names, raw, prepend = None):
        if raw:
            return names
        if prepend is None:
            prepend = tuple()
        if not isinstance(prepend, tuple):
            prepend = (prepend,)
        if not isinstance(names, tuple):
            names = (names,)
        return self.get_path(*(*prepend, *names))
    @staticmethod
    def get_path(*args):
        path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(path, *args)
