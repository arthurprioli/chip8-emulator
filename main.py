from ctypes import c_bool, c_char_p, POINTER
from typing import List
import os
import time
import sys

from components.core import Core

os.environ["SDL_USE_MAIN_CALLBACKS"] = "1"
os.environ["SDL_RENDER_DRIVER"] = "opengl"

import sdl3

renderer = POINTER(sdl3.SDL_Renderer)()
window = POINTER(sdl3.SDL_Window)()
core = Core()


@sdl3.SDL_AppInit_func
def SDL_AppInit(appstate, argc, argv):
    if not sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO):
        sdl3.SDL_Log("Couldn't initialize SDL: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    if not sdl3.SDL_CreateWindowAndRenderer(
        "CHIP-8 EMULATOR".encode(),
        core.display.WINDOW_WIDTH * 10,
        core.display.WINDOW_HEIGHT * 10,
        0,
        window,
        renderer,
    ):
        sdl3.SDL_Log("Couldn't initialize SDL: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    spec = sdl3.SDL_AudioSpec()
    spec.freq = 44100
    spec.format = sdl3.SDL_AUDIO_F32
    spec.channels = 1
    spec.callback = core.audio_helper.audio_callback

    device = sdl3.SDL_OpenAudioDevice(sdl3.SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, spec)

    sdl3.SDL_ResumeAudioDevice(device)

    return sdl3.SDL_APP_CONTINUE


@sdl3.SDL_AppEvent_func
def SDL_AppEvent(appstate, event):
    e = sdl3.SDL_DEREFERENCE(event)
    if e.type == sdl3.SDL_EVENT_QUIT:
        return sdl3.SDL_APP_SUCCESS

    core.input_handler.handle_event(e)
    return sdl3.SDL_APP_CONTINUE


@sdl3.SDL_AppIterate_func
def SDL_AppIterate(appstate):
    sdl3.SDL_SetRenderDrawColor(renderer, 0, 0, 0, sdl3.SDL_ALPHA_OPAQUE)
    sdl3.SDL_RenderClear(renderer)
    sdl3.SDL_SetRenderDrawColor(renderer, 255, 255, 255, sdl3.SDL_ALPHA_OPAQUE)
    sdl3.SDL_SetRenderScale(renderer, 10, 10)

    core.audio_helper.been_enabled = True if core.timers.sound_timer else False

    to_execute = core.fetch_instruction()
    core.decode_instruction(to_execute)
    core.display.update_bits()
    time.sleep(1 / 3600)
    sdl3.SDL_RenderPoints(
        renderer, core.display.bits, sdl3.SDL_arraysize(core.display.bits)
    )
    sdl3.SDL_RenderPresent(renderer)
    return sdl3.SDL_APP_CONTINUE


@sdl3.SDL_AppQuit_func
def SDL_AppQuit(appstate, result): ...


if __name__ == "__main__":
    argv_bytes = [a.encode() for a in sys.argv]
    argc = len(argv_bytes)
    argv = (c_char_p * (argc + 1))(*argv_bytes, None)
    sdl3.SDL_EnterAppMainCallbacks(
        argc, argv, SDL_AppInit, SDL_AppIterate, SDL_AppEvent, SDL_AppQuit
    )
