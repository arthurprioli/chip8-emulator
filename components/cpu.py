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
        self.v0 : c_uint8 = 0x0
        self.v1 : c_uint8 = 0x0
        self.v2 : c_uint8 = 0x0
        self.v3 : c_uint8 = 0x0
        self.v4 : c_uint8 = 0x0
        self.v5 : c_uint8 = 0x0
        self.v6 : c_uint8 = 0x0
        self.v7 : c_uint8 = 0x0
        self.v8 : c_uint8 = 0x0
        self.v9 : c_uint8 = 0x0
        self.va : c_uint8 = 0x0
        self.vb : c_uint8 = 0x0
        self.vc : c_uint8 = 0x0
        self.vd : c_uint8 = 0x0
        self.ve : c_uint8 = 0x0
        self.vf : c_uint8 = 0x0

