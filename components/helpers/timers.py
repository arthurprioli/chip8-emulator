from ctypes import c_uint8


class Timers:
    """
    Defines CHIP-8's delay and sound timers.
    """

    def __init__(self):
        self.delay_timer: c_uint8 = 0x0
        self.sound_timer: c_uint8 = 0x0
        self.acc = 0
        self.last = None

    def update_timers(self, now):
        if self.last is None:
            self.last = now
        self.acc += now - self.last
        while self.acc >= 1 / 60:
            if self.delay_timer > 0:
                self.delay_timer -= 1
            if self.sound_timer > 0:
                self.sound_timer -= 1
            self.acc -= 1 / 60
