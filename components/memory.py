from ctypes import c_uint16, c_uint8
from typing import List
from .helpers.font import font

class Memory:
    """
        Defines our memory class.
    """
    def __init__(self):
        self.curr_memory : List[c_uint16] = [0x0] * 4096
        self.stack : List[c_uint16] = [0x0, 0x0]

        self.curr_memory[0x00:0xFF] = font
    
