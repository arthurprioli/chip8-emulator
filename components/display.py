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
        self.count = self.WINDOW_HEIGHT * self.WINDOW_WIDTH

        self.bits = (sdl3.SDL_FPoint * self.count)()

    def clear_screen(self):
        self.bits = (sdl3.SDL_FPoint * self.count)()

 
if __name__ == "__main__":
    test_display = Display()
    for bit in test_display.bits:
        print(f"X: {bit.x} ---- Y: {bit.y}")
