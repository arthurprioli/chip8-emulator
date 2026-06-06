from ctypes import c_uint16, c_uint8
from typing import List
from components.helpers.font import font


class Memory:
    """
    Defines our memory class.
    """

    def __init__(self):
        self.curr_memory: List[c_uint16] = [0x0] * 4096
        self.stack: List[c_uint16] = [0x0, 0x0]
        # Place font at the start without changing overall memory size.
        # Use a slice whose length matches `font` so list length is preserved.
        self.curr_memory[0:len(font)] = font

    def load_instructions(self, instructions: List[c_uint16]):
        """
        Loads instructions in the first avaliable memory address.

        Args:
            instructions: The list of instructions to place in memory.
        """
        start = 0xFF
        end = start + len(instructions)
        self.curr_memory[start:end] = instructions
