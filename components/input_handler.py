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
        self.released_keys = None

    def handle_event(self, event):
        mapped = self._handle_key(event.key.scancode)
        if mapped:
            if event.type == sdl3.SDL_EVENT_KEY_DOWN:
                    self.keys[mapped] = True
            elif event.type == sdl3.SDL_EVENT_KEY_UP:
                    self.keys[mapped] = False
                    self.released_key = mapped

    def _handle_key(self, scancode):
        match scancode:
            case sdl3.SDL_SCANCODE_1:
                return 0x1
            case sdl3.SDL_SCANCODE_2:
                return 0x2
            case sdl3.SDL_SCANCODE_3:
                return 0x3
            case sdl3.SDL_SCANCODE_4:
                return 0xC
            case sdl3.SDL_SCANCODE_Q:
                return 0x4
            case sdl3.SDL_SCANCODE_W:
                return 0x5
            case sdl3.SDL_SCANCODE_E:
                return 0x6
            case sdl3.SDL_SCANCODE_R:
                return 0xD
            case sdl3.SDL_SCANCODE_A:
                return 0x7
            case sdl3.SDL_SCANCODE_S:
                return 0x8
            case sdl3.SDL_SCANCODE_D:
                return 0x9
            case sdl3.SDL_SCANCODE_F:
                return 0xE
            case sdl3.SDL_SCANCODE_Z:
                return 0xA
            case sdl3.SDL_SCANCODE_X:
                return 0x0
            case sdl3.SDL_SCANCODE_C:
                return 0xB
            case sdl3.SDL_SCANCODE_V:
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
        if 0 <= value < len(self.keys):
            return self.keys[value]
        return False
