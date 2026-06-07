"""
Integrates all components to simulate an instruction cycle.
"""

import random

from components.cpu import CPU
from components.memory import Memory
from components.display import Display
from components.rom_reader import RomReader
from components.helpers.timers import Timers
from components.input_handler import InputHandler
from typing import List
from ctypes import c_uint16

ROM_PATH = "/home/arthurprioli/Documentos/dev/fun/chip8-emulator/roms/slipperyslope.ch8"


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
        self.cpu.pc = 0x200  # hard-coded - first address with instructions
        self.input_handler = InputHandler()
        self.timers = Timers()

    def fetch_instruction(self):
        """
        Fetches the instruction on the memory.
        """
        print(f"Fetching instruction at addr {hex(self.cpu.pc)}")
        high_byte = self.memory.curr_memory[self.cpu.pc]
        low_byte = self.memory.curr_memory[self.cpu.pc + 1]
        instruction = (high_byte << 8) | low_byte

        if not instruction:
            return

        self.cpu.pc += 2
        return instruction

    def decode_instruction(self, instruction: c_uint16):
        """
        Decodes the fetched instruction.
        """
        if not instruction:
            print("END OF PROGRAM")
            return

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
                                if not self.memory.stack:
                                    print(
                                        "Stack underflow on 00EE: stack is empty — stopping simulation"
                                    )
                                    raise RuntimeError("Stack underflow on return (00EE)")

                                returned_addr = self.memory.stack.pop()
                                print(f"Returning address {returned_addr}...")
                                self.cpu.pc = returned_addr
            case 0x1:
                destination_addr = (
                    (second_nibble << 8) | (third_nibble << 4) | fourth_nibble
                )
                print(f"Setting pc to {hex(destination_addr)}")
                self.cpu.pc = destination_addr
            case 0x2:
                curr_pc = self.cpu.pc
                # Protect against stack overflow
                if len(self.memory.stack) >= 16:
                    print(
                        "Stack overflow on 2NNN: maximum stack depth reached — stopping simulation"
                    )
                    raise RuntimeError("Stack overflow on call (2NNN)")

                self.memory.stack.append(curr_pc)
                destination_addr = (
                    (second_nibble << 8) | (third_nibble << 4) | fourth_nibble
                )
                self.cpu.pc = destination_addr
            case 0x3:
                to_compare = (third_nibble << 4) | fourth_nibble
                if self.cpu.registers[second_nibble] == to_compare:
                    self.cpu.pc += 2
            case 0x4:
                to_compare = (third_nibble << 4) | fourth_nibble
                print(
                    f"Comparing {hex(to_compare)} with {hex(self.cpu.registers[second_nibble])}"
                )
                if self.cpu.registers[second_nibble] != to_compare:
                    self.cpu.pc += 2
            case 0x5:
                if (
                    self.cpu.registers[second_nibble]
                    == self.cpu.registers[third_nibble]
                ):
                    self.cpu.pc += 2
            case 0x6:
                new_val = (third_nibble << 4) | fourth_nibble
                print(f"Setting register v{second_nibble} to {hex(new_val)}...")
                self.cpu.registers[second_nibble] = new_val & 0xFF
            case 0x7:
                new_val = (third_nibble << 4) | fourth_nibble
                self.cpu.registers[second_nibble] = (
                    self.cpu.registers[second_nibble] + new_val
                ) & 0xFF
                print(
                    f"Adding {hex(new_val)} to {hex(self.cpu.registers[second_nibble])} in v{second_nibble}"
                )
            case 0x8:
                match fourth_nibble:
                    case 0x0:
                        self.cpu.registers[second_nibble] = self.cpu.registers[
                            third_nibble
                        ]
                    case 0x1:
                        self.cpu.registers[second_nibble] |= self.cpu.registers[
                            third_nibble
                        ]
                    case 0x2:
                        self.cpu.registers[second_nibble] &= self.cpu.registers[
                            third_nibble
                        ]
                    case 0x3:
                        self.cpu.registers[second_nibble] ^= self.cpu.registers[
                            third_nibble
                        ]
                    case 0x4:
                        total = (
                            self.cpu.registers[second_nibble]
                            + self.cpu.registers[third_nibble]
                        )
                        self.cpu.registers[0xF] = 1 if total > 0xFF else 0
                        self.cpu.registers[second_nibble] = total & 0xFF
                    case 0x5:
                        self.cpu.registers[0xF] = (
                            1
                            if (
                                self.cpu.registers[second_nibble]
                                > self.cpu.registers[third_nibble]
                            )
                            else 0
                        )
                        diff = (
                            self.cpu.registers[second_nibble]
                            - self.cpu.registers[third_nibble]
                        )
                        self.cpu.registers[second_nibble] = diff & 0xFF
                    case 0x6:
                        # self.cpu.registers[second_nibble] = self.cpu.registers[
                        #    third_nibble
                        # ]
                        self.cpu.registers[0xF] = (
                            1 if (self.cpu.registers[second_nibble] & 0x01) else 0
                        )
                        self.cpu.registers[second_nibble] = (
                            self.cpu.registers[second_nibble] >> 1
                        ) & 0xFF
                    case 0x7:
                        if (
                            self.cpu.registers[third_nibble]
                            > self.cpu.registers[second_nibble]
                        ):
                            self.cpu.registers[0xF] = 1
                        else:
                            self.cpu.registers[0xF] = 0

                        diff = (
                            self.cpu.registers[third_nibble]
                            - self.cpu.registers[second_nibble]
                        )
                        self.cpu.registers[third_nibble] = diff & 0xFF
                    case 0xE:
                        #                        self.cpu.registers[second_nibble] = self.cpu.registers[
                        #                           third_nibble
                        #                        ]
                        self.cpu.registers[0xF] = (
                            1 if (self.cpu.registers[second_nibble] & 0x80) else 0
                        )
                        self.cpu.registers[second_nibble] = (
                            self.cpu.registers[second_nibble] << 1
                        ) & 0xFF
            case 0x9:
                if (
                    self.cpu.registers[second_nibble]
                    != self.cpu.registers[third_nibble]
                ):
                    self.cpu.pc += 2
            case 0xA:
                destination_addr = (
                    (second_nibble << 8) | (third_nibble << 4) | fourth_nibble
                )
                print(f"Setting index pointer to {hex(destination_addr)}...")
                self.cpu.index = destination_addr
            case 0xB:
                destination_addr = (
                    (second_nibble << 8) | (third_nibble << 4) | fourth_nibble
                )
                final_addr = destination_addr + self.cpu.registers[0]
                self.cpu.pc = print(
                    f"Jumping to instruction in address {hex(final_addr)}"
                )
            case 0xC:
                random_num = random.randbytes(1)
                final_val = random_num & ((third_nibble << 4) | fourth_nibble)
                self.cpu.registers[second_nibble] = final_val
                print(
                    f"Generating random number {random_num}, ANDing it to {final_val}  and putting into v{second_nibble}"
                )
            case 0xD:
                x_coord = self.cpu.registers[second_nibble] % 64
                y_coord = self.cpu.registers[third_nibble] % 32
                rows = fourth_nibble
                self.cpu.registers[0xF] = 0
                mem_size = len(self.memory.curr_memory)
                for i in range(rows):
                    addr = self.cpu.index + i
                    if 0 <= addr < mem_size:
                        sprite_data = self.memory.curr_memory[addr]
                        print(f"Current sprite data: f{sprite_data}")
                    else:
                        print(f"DXYN: skipped out-of-bounds sprite byte read at {hex(addr)}")
                        continue
                    for j in range(8):
                        target_y = y_coord + i
                        target_x = x_coord + j

                        if target_x >= 64 or target_y >= 32:
                            continue

                        curr_sprite_bit = (sprite_data >> (7 - j)) & 0x01
                        if curr_sprite_bit:
                            index_in_display = target_x + 64 * target_y

                            if self.display.frame_buffer[index_in_display]:
                                self.cpu.registers[0xF] = 1

                            self.display.frame_buffer[index_in_display] ^= 1
            case 0xE:
                match third_nibble:
                    case 0x9:
                        vx_key = self.cpu.registers[second_nibble] & 0xF
                        if self.input_handler.check_key_pressed(vx_key):
                            self.cpu.pc += 2
                    case 0xA:
                        vx_key = self.cpu.registers[second_nibble] & 0xF
                        if not self.input_handler.check_key_pressed(vx_key):
                            self.cpu.pc += 2
            case 0xF:
                match third_nibble:
                    case 0x0:
                        match fourth_nibble:
                            case 0x7:
                                self.cpu.registers[second_nibble] = (
                                    self.timers.delay_timer
                                )
                            case 0xA:
                                self.cpu.registers[second_nibble] = (
                                    self.input_handler.await_key()
                                )
                    case 0x1:
                        match fourth_nibble:
                            case 0x5:
                                self.timers.delay_timer = self.cpu.registers[
                                    second_nibble
                                ]
                            case 0x8:
                                self.timers.sound_timer = self.cpu.registers[
                                    second_nibble
                                ]
                            case 0xE:
                                self.cpu.index += self.cpu.registers[second_nibble]
                                if (self.cpu.index > 0x1000) or (
                                    self.cpu.index < 0x0FFF
                                ):
                                    self.cpu.registers[0xF] = 1
                    case 0x2:
                        vx = self.cpu.registers[second_nibble] & 0xF
                        self.cpu.index = vx * 5
                    case 0x3:
                        first_num, second_num, third_num = (
                            self.cpu.registers[second_nibble] // 100,
                            (self.cpu.registers[second_nibble] // 10) % 10,
                            (self.cpu.registers[second_nibble] % 10),
                        )
                        print(
                            f"Decomposed value {self.cpu.registers[second_nibble]} in {first_num}, {second_num} and {third_num}..."
                        )
                        mem_size = len(self.memory.curr_memory)
                        for offset, byte in enumerate(
                            (first_num, second_num, third_num)
                        ):
                            addr = self.cpu.index + offset
                            if 0 <= addr < mem_size:
                                self.memory.curr_memory[addr] = byte
                            else:
                                print(
                                    f"FX33: skipped out-of-bounds write at {hex(addr)}"
                                )
                    case 0x5:
                        curr_addr = self.cpu.index
                        mem_size = len(self.memory.curr_memory)
                        for i in range(second_nibble + 1):
                            addr = curr_addr + i
                            print(
                                f"Setting {hex(addr)} to the value of v{i}: {self.cpu.registers[i]}..."
                            )
                            if 0 <= addr < mem_size:
                                self.memory.curr_memory[addr] = self.cpu.registers[i]
                            else:
                                print(f"FX55: skipped out-of-bounds write at {hex(addr)}")
                    case 0x6:
                        curr_addr = self.cpu.index
                        mem_size = len(self.memory.curr_memory)
                        for i in range(second_nibble + 1):
                            addr = curr_addr + i
                            if 0 <= addr < mem_size:
                                self.cpu.registers[i] = self.memory.curr_memory[addr]
                            else:
                                print(f"FX65: skipped out-of-bounds read at {hex(addr)}")


if __name__ == "__main__":
    core = Core()
    print(hex(core.fetch_instruction()))
