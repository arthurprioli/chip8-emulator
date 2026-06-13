import ctypes


class AudioHelper:
    SAMPLE_RATE = 44100
    FREQUENCY = 440.0  # A4 tone

    def __init__(self):
        self.beep_enabled = False
        self.phase = 0.0

    def generate(self, num_samples):
        num_samples = int(num_samples)
        buffer = (ctypes.c_float * num_samples)()

        # How many samples make up one full 440 Hz cycle (~100.2 at 44.1 kHz).
        # This is the wave period — independent of the chunk size.
        samples_per_cycle = self.SAMPLE_RATE / self.FREQUENCY

        for i in range(num_samples):
            # First half of each cycle = high, second half = low: a square wave.
            buffer[i] = 0.25 if self.phase < samples_per_cycle / 2 else -0.25

            self.phase += 1
            if self.phase >= samples_per_cycle:
                # Subtract (don't reset to 0) so the fractional remainder carries
                # over — keeps the pitch accurate and the wave continuous across chunks.
                self.phase -= samples_per_cycle

        return buffer
