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
            0x1234,
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

    def decode_instruction(self, instruction):
        """
        Decodes the fetched instruction.

        0001 0010 0011 0100 
        """
        first_nibble = (instruction >> 12) # 0001
        second_nibble = (instruction >> 8) & 0x0F # 0010
        third_nibble = (instruction >> 4) & 0x00F # 0011
        fourth_nibble = instruction & 0x00F # 0100

        match first_nibble:
            case 0x0:
                match thrid_nibble:
                    case 0xE:
                        match fourth_nibble:
                            case 0x0:
                                self.display.clear_screen()
                            case 0xE:
                                returned_addr = self.memory.stack.pop()
                                self.cpu.pc = returned_addr
            case 0x1:
                destination_addr = (second_nibble << 8) + (third_nibble << 4) + fourth_nibble
                self.cpu.pc = destination_addr
            case 0x2:
                curr_pc = self.cpu.pc
                self.memory.stack.append(curr_pc)

                destination_addr = (second_nibble << 8) + (third_nibble << 4) + fourth_nibble
                self.cpu.pc = destination_addr
            case 0x3:
                to_compare = (third_nibble << 4) + fourth_nibble
                if self.cpu.registers[second_nibble] == to_compare:
                    self.cpu.pc += 1
            case 0x4:
                to_compare = (third_nibble << 4) + fourth_nibble
                if self.cpu.registers[second_nibble] != to_compare:
                    self.cpu.pc += 1
            case 0x5:
                if self.cpu.registers[second_nibble] == self.cpu.registers[third_nibble]:
                    self.cpu.pc += 1
            case 0x6:
                new_val = (third_nibble << 4) + fourth_nibble
                self.cpu.registers[second_nibble] = new_val
            case 0x7:
                new_val = (third_nibble << 4) + fourth_nibble
                self.cpu.registers[second_nibble] += new_val
            case 0x9:
                if self.cpu.registers[second_nibble] != self.cpu.registers[third_nibble]:
                    self.cpu.pc += 1
            case 0xA:
                destination_addr = (second_nibble << 8) + (third_nibble << 4) + fourth_nibble
                self.cpu.index = destination_addr
            case 0xD:
                x_coord = self.cpu.registers[second_nibble] % 64
                y_coord = self.cpu.registers[third_nibble] % 32
                rows = fourth_nibble
                self.cpu.registers[0xF] = 0
                for i in range(rows):
                    sprite_data = self.memory.curr_memory[self.cpu.index + i]
                    for i in range(7, 0, -1):
                        curr_pixel = (sprite_data >> i) & 0x01
                        # If the current pixel in the sprite row is on and the pixel at coordinates X,Y on the screen is also on, turn off the pixel and set VF to 1
                        # Or if the current pixel in the sprite row is on and the screen pixel is not, draw the pixel at the X and Y coordinates

 


if __name__ == "__main__":
    core = Core()
    core.decode_instruction(core.fetch_instruction())
