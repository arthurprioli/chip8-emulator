from ctypes import c_bool, POINTER
from typing import List
import sdl3


class Display:
    """
    Our CHIP-8 display class, OOP is my passion :D
    6x2
10 % 6
    1 1 1 0 1 1
    1 0 0 1 1 1
    """

    def __init__(self):
        self.WINDOW_WIDTH = 64
        self.WINDOW_HEIGHT = 32
        self.count = self.WINDOW_HEIGHT * self.WINDOW_WIDTH
        self.frame_buffer = [0x0] * self.count

        self.bits = (sdl3.SDL_FPoint * self.count)()

    def clear_screen(self):
        self.frame_buffer = [0x0] * self.count

    def update_bits(self):
        for i in range(len(self.frame_buffer)):
            x_coord = i % self.WINDOW_WIDTH
            y_coord = i // self.WINDOW_WIDTH

            if self.frame_buffer[i]:
                self.bits[i].x = x_coord
                self.bits[i].y = y_coord
            else:
                self.bits[i].x = -1.0
                self.bits[i].y = -1.0


if __name__ == "__main__":
    test_display = Display()
    for bit in test_display.bits:
        print(f"X: {bit.x} ---- Y: {bit.y}")
