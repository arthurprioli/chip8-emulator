import os
from ctypes import c_uint16
from typing import List

class RomReader:
    """
    Defines the reading of binary instructions in a ROM.
    """

    def __init__(self, rom_path: str = ""):
        self.rom_path = rom_path
        self.chunk_size = 2

    def get_instructions(self):
        instructions : List[c_uint16] = []
        with open(self.rom_path, "rb") as f:
            for instruction in iter(lambda: f.read(self.chunk_size), b""):
                value = int.from_bytes(instruction)
                instructions.append(value)
        f.close()
        return instructions


if __name__ == "__main__":
    reader = RomReader(
        rom_path="/home/arthurprioli/Documentos/dev/fun/chip8-emulator/roms/IBM Logo.ch8"
    )
    print(reader.get_instructions())

