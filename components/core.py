"""
    Integrates all components to simulate an instruction cycle.
"""
from cpu import CPU
from memory import Memory
from display import Display
from helpers.timers import Timers

class Core:
    def __init__(self):
        cpu = CPU()
        memory = Memory()

        # point index pointer to beggining of memory
        
