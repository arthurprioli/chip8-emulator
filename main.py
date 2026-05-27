from ctypes import c_bool, c_char_p, POINTER
from typing import List
import os
import time
import sys 

from components.display import Display

os.environ["SDL_USE_MAIN_CALLBACKS"] = "1"
os.environ["SDL_RENDER_DRIVER"] = "opengl"

import sdl3

renderer = POINTER(sdl3.SDL_Renderer)()
window = POINTER(sdl3.SDL_Window)()
display = Display()

@sdl3.SDL_AppInit_func
def SDL_AppInit(appstate, argc, argv):
    if not sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO):
        sdl3.SDL_Log("Couldn't initialize SDL: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    if not sdl3.SDL_CreateWindowAndRenderer("CHIP-8 EMULATOR".encode(), display.WINDOW_WIDTH * 10, display.WINDOW_HEIGHT * 10, 0, window, renderer):
        sdl3.SDL_Log("Couldn't initialize SDL: %s".encode() % sdl3.SDL_GetError())
        return sdl3.SDL_APP_FAILURE

    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppEvent_func
def SDL_AppEvent(appstate, event):
    if sdl3.SDL_DEREFERENCE(event).type == sdl3.SDL_EVENT_QUIT:
        return sdl3.SDL_APP_SUCCESS

    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppIterate_func
def SDL_AppIterate(appstate):
    sdl3.SDL_SetRenderDrawColor(renderer, 0, 0, 0, sdl3.SDL_ALPHA_OPAQUE)
    sdl3.SDL_RenderClear(renderer)
    sdl3.SDL_SetRenderDrawColor(renderer, 255, 255, 255, sdl3.SDL_ALPHA_OPAQUE)
    sdl3.SDL_SetRenderScale(renderer, 10, 10)
    sdl3.SDL_RenderPoints(renderer, display.bits, sdl3.SDL_arraysize(display.bits))
    sdl3.SDL_RenderPresent(renderer)
    return sdl3.SDL_APP_CONTINUE

@sdl3.SDL_AppQuit_func
def SDL_AppQuit(appstate, result):
    ...

if __name__ == "__main__":
    argv_bytes = [a.encode() for a in sys.argv]
    argc = len(argv_bytes)
    argv = (c_char_p * (argc + 1))(*argv_bytes, None) 
    sdl3.SDL_EnterAppMainCallbacks(argc, argv, SDL_AppInit, SDL_AppIterate, SDL_AppEvent, SDL_AppQuit)