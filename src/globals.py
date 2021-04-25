def instance(_type):
    return Singleton.get_instance(_type)

class Singleton:

    __instances = {}

    @staticmethod
    def get_instance(_type):
        if _type in Singleton.__instances:
            return Singleton.__instances[_type]
        raise Exception("No instance of Singleton.")

    def __init__(self):
        if type(self) in Singleton.__instances:
            raise Exception("Invalid initialistion of Singleton.")
        Singleton.__instances[type(self)] = self

class Globals(Singleton):

    def __init__(self):
        super().__init__()
        self.__window_size = (1024, 1024)

    def get_window_size(self):
        return self.__window_size
