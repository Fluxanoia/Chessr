from typing import Optional

from src.engine.camera import Camera
from src.engine.file_manager import FileManager
from src.engine.group_manager import GroupManager
from src.engine.spritesheets.board_spritesheet import BoardSpritesheet


class Factory:

    __instance : Optional['Factory'] = None

    @staticmethod
    def get() -> 'Factory':
        if Factory.__instance is None:
            Factory.__instance = Factory()
        return Factory.__instance

    def __init__(self) -> None:
        if not Factory.__instance is None:
            raise SystemExit('Invalid initialisation of Factory.')

        self.__camera : Optional[Camera] = None
        self.__file_manager : Optional[FileManager] = None
        self.__group_manager : Optional[GroupManager] = None
        self.__board_spritesheet : Optional[BoardSpritesheet] = None

    @property
    def camera(self) -> Camera:
        if self.__camera is None:
            self.__camera = Camera()
        return self.__camera

    @property
    def file_manager(self) -> FileManager:
        if self.__file_manager is None:
            self.__file_manager = FileManager()
        return self.__file_manager

    @property
    def group_manager(self) -> GroupManager:
        if self.__group_manager is None:
            self.__group_manager = GroupManager()
        return self.__group_manager

    @property
    def board_spritesheet(self) -> BoardSpritesheet:
        if self.__board_spritesheet is None:
            self.__board_spritesheet = BoardSpritesheet(self.file_manager)
        return self.__board_spritesheet
