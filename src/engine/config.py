from src.utils.helpers import IntVector

class Config:

    @staticmethod
    def get_window_dimensions() -> IntVector:
        return (1024, 1024)

    @staticmethod
    def get_fps() -> int:
        return 60
