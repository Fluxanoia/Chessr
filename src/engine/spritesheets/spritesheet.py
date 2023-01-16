import pygame as pg
from src.utils.path import PathLike
from src.engine.file_manager import FileManager

class Spritesheet():

    def __init__(self, file_manager : FileManager, pathlike : PathLike) -> None:
        super().__init__()
        self.__sheets : dict[float, pg.surface.Surface] = {
            1 : file_manager.load_image(pathlike, True)
        }
    
    def get_sheet(self, scale : float = 1) -> pg.surface.Surface:
        if scale in self.__sheets:
            return self.__sheets[scale]
        
        src = self.__sheets[1]
        scaled_size = tuple(map(lambda x: int(x * scale), src.get_size()))
        self.__sheets[scale] = pg.transform.scale(src, scaled_size)
        return self.__sheets[scale]

    def get_image(self, src_rect : pg.Rect, scale : float) -> pg.surface.Surface:
        image = pg.Surface(src_rect.size, pg.SRCALPHA, 32).convert_alpha()
        image.blit(self.get_sheet(scale), (0, 0), src_rect)
        return image
