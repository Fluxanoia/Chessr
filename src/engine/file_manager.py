import os
from typing import Optional

import pygame as pg

from src.utils.path import Path, PathLike


class FileManager():

    DELIM = ':'
    DEFAULT_FONT = 'Roboto-Black.ttf'

    def __init__(self) -> None:
        self.__fonts : dict[str, dict[int, pg.font.Font]]= {}
        if not pg.image.get_extended():
            raise SystemExit('The extended image types are required.')

    def load_default_font(self, pt : int = 16) -> pg.font.Font:
        return self.load_font(FileManager.DEFAULT_FONT, pt)

    def load_font(self, name : str, pt : int) -> pg.font.Font:
        if not name in self.__fonts:
            self.__fonts[name] = {}

        if not pt in self.__fonts[name]:
            path = Path(('files', 'fonts')).get_relative_path(name).get_literal_path()
            self.__fonts[name][pt] = pg.font.Font(path, pt)
            
        return self.__fonts[name][pt]

    def load_image(
        self,
        pathlike : PathLike,
        use_alpha : bool = False
    ) -> pg.surface.Surface:
        path = Path('images').get_relative_path(pathlike).get_literal_path()
        try:
            surface = pg.image.load(path)
        except pg.error as e:
            raise SystemExit(f'The image \'{path}\' could not be loaded.') from e

        return surface.convert_alpha() if use_alpha else surface.convert()

    def load_board(
        self,
        pathlike : PathLike
    ) -> Optional[dict[str, str]]:
        path_object = self.__get_path_object(pathlike)
        return self.load_file(Path(('files', 'boards')).get_relative_path(path_object))

    def load_file(
        self,
        pathlike : PathLike,
        default : Optional[dict[str, str]] = None
    ) -> Optional[dict[str, str]]:
        path_object = self.__get_path_object(pathlike)

        path = path_object.get_literal_path()
        if not self.__exists(path):
            if not default is None:
                self.overwrite_file(path_object, default)
            return default
        
        data : dict[str, str] = {}
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
            self.overwrite_file(path_object, data)
        return data

    def overwrite_file(
        self,
        pathlike : PathLike,
        content : dict[str, str]
    ) -> None:
        path = self.__get_path_object(pathlike).get_literal_path()
        if not self.__exists(path):
            self.__mkdirs(path)
        
        with open(path, 'w+') as file:
            for (x, y) in content.items():
                file.write(str(x) + FileManager.DELIM + str(y) + '\n')

    def __get_path_object(self, obj : PathLike) -> Path:
        if isinstance(obj, Path):
            return obj
        return Path(obj)

    def __mkdirs(self, path : str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok = True)

    def __exists(self, path : str) -> bool:
        return os.path.exists(path)
