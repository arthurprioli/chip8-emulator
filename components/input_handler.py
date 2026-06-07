import sdl3


import sdl3


class InputHandler:
    """
    Class responsible for treating SDL Keyboard inputs.

    This class maintains a 16-key state array (`self.keys`) that reflects whether
    each CHIP-8 key (0x0..0xF) is currently pressed. SDL events are consumed
    to update that state; `check_key_pressed` returns the current state rather
    than relying on a single matching event.
    """

    def __init__(self):
        self.keys = [False] * 16

    def _handle_key(self, scancode):
        if scancode in (
            sdl3.SDL_SCANCODE_1,
            sdl3.SDL_SCANCODE_2,
            sdl3.SDL_SCANCODE_3,
            sdl3.SDL_SCANCODE_4,
            sdl3.SDL_SCANCODE_5,
            sdl3.SDL_SCANCODE_6,
            sdl3.SDL_SCANCODE_7,
            sdl3.SDL_SCANCODE_8,
            sdl3.SDL_SCANCODE_9,
        ):
            return scancode - 29
        elif scancode == sdl3.SDL_SCANCODE_0:
            return 0
        elif scancode == sdl3.SDL_SCANCODE_Q:
            return 0xA
        elif scancode == sdl3.SDL_SCANCODE_W:
            return 0xB
        elif scancode == sdl3.SDL_SCANCODE_E:
            return 0xC
        elif scancode == sdl3.SDL_SCANCODE_R:
            return 0xD
        elif scancode == sdl3.SDL_SCANCODE_T:
            return 0xE
        elif scancode == sdl3.SDL_SCANCODE_Y:
            return 0xF
        return None

    def await_key(self):
        event = sdl3.SDL_Event()
        while True:
            sdl3.SDL_WaitEvent(event)
            if event.type == sdl3.SDL_EVENT_KEY_DOWN:
                mapped = self._handle_key(event.key.scancode)
                if mapped is None:
                    continue
                self.keys[mapped] = True
                return mapped
            elif event.type == sdl3.SDL_EVENT_KEY_UP:
                mapped = self._handle_key(event.key.scancode)
                if mapped is not None:
                    self.keys[mapped] = False

    def check_key_pressed(self, value):
        """
        Update key state from pending SDL events and return True if `value`
        is currently pressed.
        """
        event = sdl3.SDL_Event()
        while sdl3.SDL_PollEvent(event):
            if event.type == sdl3.SDL_EVENT_KEY_DOWN:
                mapped = self._handle_key(event.key.scancode)
                if mapped is not None:
                    self.keys[mapped] = True
            elif event.type == sdl3.SDL_EVENT_KEY_UP:
                mapped = self._handle_key(event.key.scancode)
                if mapped is not None:
                    self.keys[mapped] = False

        if 0 <= value < len(self.keys):
            return self.keys[value]
        return False
