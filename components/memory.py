from ctypes import c_uint16, c_uint8
from typing import List
from helpers.font import font


class Memory:
    """
    Defines our memory class.
    """

    def __init__(self):
        self.curr_memory: List[c_uint16] = [0x0] * 4096
        self.stack: List[c_uint16] = [0x0, 0x0]

        self.curr_memory[0x00:0xFF] = font

    def load_instructions(self, instructions: List[c_uint16]):
        """
        Loads instructions in the first avaliable memory address.

        Args:
            instructions: The list of instructions to place in memory.
        """
        self.curr_memory[0xFF:] = instructions
