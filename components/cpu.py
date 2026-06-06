from ctypes import c_uint16, c_uint8, POINTER

class CPU:
    """
        Defines our CHIP-8 Emulator Registers
    """
    def __init__(self):
        #defines our auxiliary pointers
        self.index : POINTER = 0x0
        self.pc : POINTER = 0x0

        # defines 8 bit registers for our chip
        self.registers : List[c_uint8] = [0x0] * 16
