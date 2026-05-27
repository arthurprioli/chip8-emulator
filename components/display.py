from ctypes import c_bool, POINTER
from typing import List
import sdl3

class Display:
    """
        Our CHIP-8 display class, OOP is my passion :D
    """
    def __init__(self):
        self.WINDOW_WIDTH = 64
        self.WINDOW_HEIGHT = 32
        count = self.WINDOW_HEIGHT * self.WINDOW_WIDTH

        self.bits = (sdl3.SDL_FPoint * count)()

        for i in range(count):
            self.bits[i].x = float(i % self.WINDOW_WIDTH) # TODO: read and translate sprites
            self.bits[i].y = float(i // self.WINDOW_HEIGHT) 
