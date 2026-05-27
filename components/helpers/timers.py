from ctypes import c_uint8

class Timers:
    """
        Defines CHIP-8's delay and sound timers.
    """
    def __init__(self):
        self.delay_timer : c_uint8 = 0x0 
        self.sound_timer : c_uint8 = 0x0