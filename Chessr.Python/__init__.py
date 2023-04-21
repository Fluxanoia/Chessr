import os

import backend

from src.master import Master

backend.SomeClass(1)

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

if __name__ == '__main__':
    Master()
