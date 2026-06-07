import ctypes


class AudioHelper:
    def __init__(self):
        self.beep_enabled = False
        self.phase = 0.0

    def audio_callback(self, userdata, stream, length):
        self.buffer = (ctypes.c_float * (length // 4)).from_address(stream)

        if not self.beep_enabled:
            for i in range(len(buffer)):
                buffer[i] = 0.0
            return

        self.samples_per_cycle = 44100 / 440.0

        for i in range(len(buffer)):
            self.buffer[i] = 0.25 if self.phase < self.samples_per_cycle / 2 else -0.25

            self.phase += 1
            if self.phase >= self.samples_per_cycle:
                self.phase = 0
