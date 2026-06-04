"""
Integrates all components to simulate an instruction cycle.
"""

from cpu import CPU
from memory import Memory
from display import Display
from helpers.timers import Timers
from typing import List
from ctypes import c_uint16


class Core:
    def __init__(self):
        """
        Starts the core of the emulator, defines all parameters to its standards.
        """
        self.cpu = CPU()
        self.memory = Memory()
        instructions: List[c_uint16] = [
            0x00E0,
            0x1000,
            0x6000,
            0x7000,
            0xA000,
            0xD000,
        ]

        # load instruction to first avaliable memory address in IO
        self.memory.load_instructions(instructions)
        self.cpu.pc = 0xFF + 1  # hard-coded - first address with instructions

    def fetch_instruction(self):
        """
        Fetches the instruction on the memory.
        """
        instruction = self.memory.curr_memory[self.cpu.pc]
        self.cpu.pc += 1
        return instruction


if __name__ == "__main__":
    core = Core()
    print(core.fetch_instruction())
