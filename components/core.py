"""
Integrates all components to simulate an instruction cycle.
"""

import sdl3

from components.cpu import CPU
from components.memory import Memory
from components.display import Display
from components.rom_reader import RomReader
from components.helpers.timers import Timers
from typing import List
from ctypes import c_uint16

ROM_PATH = "/home/arthurprioli/Documentos/dev/fun/chip8-emulator/roms/IBM Logo.ch8"


class Core:
    def __init__(self):
        """
        Starts the core of the emulator, defines all parameters to its standards.
        """
        self.cpu = CPU()
        self.memory = Memory()
        self.display = Display()
        self.rom_reader = RomReader(ROM_PATH)
        self.instructions: List[c_uint16] = self.rom_reader.get_instructions()
        # load instruction to first avaliable memory address in IO
        self.memory.load_instructions(self.instructions)
        self.cpu.pc = 0xFF  # hard-coded - first address with instructions

    def fetch_instruction(self):
        """
        Fetches the instruction on the memory.
        """
        print(f"Fetching instruction at addr {hex(self.cpu.pc)}")
        instruction = self.memory.curr_memory[self.cpu.pc]
        self.cpu.pc += 1
        return instruction

    def decode_instruction(self, instruction: c_uint16):
        """
        Decodes the fetched instruction.
        """
        print(f"Decoding instruction {hex(instruction)}...")
        first_nibble = instruction >> 12  # 0001
        second_nibble = (instruction >> 8) & 0x0F  # 0010
        third_nibble = (instruction >> 4) & 0x00F  # 0011
        fourth_nibble = instruction & 0x00F  # 0100

        match first_nibble:
            case 0x0:
                match third_nibble:
                    case 0xE:
                        match fourth_nibble:
                            case 0x0:
                                print("Clearing screen...")
                                self.display.clear_screen()
                            case 0xE:
                                returned_addr = self.memory.stack.pop()
                                print(f"Returning address {returned_addr}...")
                                self.cpu.pc = returned_addr
            case 0x1:
                destination_addr = (
                    (second_nibble << 8) + (third_nibble << 4) + fourth_nibble
                )
                self.cpu.pc = destination_addr
            case 0x2:
                curr_pc = self.cpu.pc
                self.memory.stack.append(curr_pc)

                destination_addr = (
                    (second_nibble << 8) + (third_nibble << 4) + fourth_nibble
                )
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
                if (
                    self.cpu.registers[second_nibble]
                    == self.cpu.registers[third_nibble]
                ):
                    self.cpu.pc += 1
            case 0x6:
                new_val = (third_nibble << 4) + fourth_nibble
                print(f"Setting register v{second_nibble} to {hex(new_val)}...")
                self.cpu.registers[second_nibble] = new_val
            case 0x7:
                new_val = (third_nibble << 4) + fourth_nibble
                self.cpu.registers[second_nibble] += new_val
            case 0x9:
                if (
                    self.cpu.registers[second_nibble]
                    != self.cpu.registers[third_nibble]
                ):
                    self.cpu.pc += 1
            case 0xA:
                destination_addr = (
                    (second_nibble << 8) + (third_nibble << 4) + fourth_nibble
                )
                print(f"Setting index pointer to {hex(destination_addr)}...")
                self.cpu.index = destination_addr
            case 0xD:
                x_coord = self.cpu.registers[second_nibble] % 64
                y_coord = self.cpu.registers[third_nibble] % 32
                rows = fourth_nibble
                self.cpu.registers[0xF] = 0
                print(len(self.memory.curr_memory))
                for i in range(rows):
                    sprite_data = self.memory.curr_memory[self.cpu.index + i]
                    for i in range(7, 0, -1):
                        curr_pixel = (sprite_data >> i) & 0x01
                        # If the current pixel in the sprite row is on and the pixel at coordinates X,Y on the screen is also on, turn off the pixel and set VF to 1
                        for pixel in self.display.bits:
                            if pixel.x == x_coord and pixel.y == y_coord:
                                self.display.bits.remove(pixel)
                                self.cpu.registers[0xF] = 1
                                if x_coord == 64.0:
                                    break
                                x_coord += 1
                        # Or if the current pixel in the sprite row is on and the screen pixel is not, draw the pixel at the X and Y coordinates
                        if not self.cpu.registers[0xF]:
                            new_point = sdl3.SDL_FPoint()
                            new_point.x = x_coord
                            new_point.y = y_coord
                            self.display.bits.append(new_point)
                    y_coord += 1
                    if y_coord == 32.0:
                        break


if __name__ == "__main__":
    core = Core()
    print(hex(core.fetch_instruction()))
