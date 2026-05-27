# Emulating CHIP-8

## What should be done?

- [ ] Define the components (Memory, timers, registers, I/O, Font, Display)
    - [ ] Define auxiliary registers: Index, Program Counter, 16 register variables
        - Program counter points at current memory instruction - 16bit pointer
        - Index points at locations at memory (like fonts btw)
        - 16 8-bit variable register (V0-VF)
    - [ ] Define delay and sound timers
        - Decrease both timers 60 times a second
        - Sound timer beeps the computer if it is above 0
        - Delay independent of refresh rate 
    - [ ] Define memory array and reading and writing 
        - Memory should be 4kB large - 4096 memory adresses
    - [ ] Define the stack and it's location (within/outside the memory)
        - stores 16-bit numbers, used to store subroutines returns
    - [ ] Store font data in memory 
        - Font should be 4x5 pixels
        - Store font in memory between `000-1FF`
    - [ ] Define display and it's drawing and refreshing
        - Define pixel array map 64x32 boolean
        - Update pixels at 60Hz
        - Draw draws sprite on screen, each bit is a horizontal pixel, 0 is transparent, 1 flips the pixel in the location drawn (XOR)
    - [ ] Define I/O keypads
        - Use left side of QWERTY

- [ ] Generate execution loop (Fetch, Decode, Execute)
    - [ ] Implement the fetch process
    - [ ] Implement the decode process
    - [ ] Implement the execute process

- [] Test in real applications
    - Draw IBM logo first


## Helpers


```
0xF0, 0x90, 0x90, 0x90, 0xF0, // 0
0x20, 0x60, 0x20, 0x20, 0x70, // 1
0xF0, 0x10, 0xF0, 0x80, 0xF0, // 2
0xF0, 0x10, 0xF0, 0x10, 0xF0, // 3
0x90, 0x90, 0xF0, 0x10, 0x10, // 4
0xF0, 0x80, 0xF0, 0x10, 0xF0, // 5
0xF0, 0x80, 0xF0, 0x90, 0xF0, // 6
0xF0, 0x10, 0x20, 0x40, 0x40, // 7
0xF0, 0x90, 0xF0, 0x90, 0xF0, // 8
0xF0, 0x90, 0xF0, 0x10, 0xF0, // 9
0xF0, 0x90, 0xF0, 0x90, 0x90, // A
0xE0, 0x90, 0xE0, 0x90, 0xE0, // B
0xF0, 0x80, 0x80, 0x80, 0xF0, // C
0xE0, 0x90, 0x90, 0x90, 0xE0, // D
0xF0, 0x80, 0xF0, 0x80, 0xF0, // E
0xF0, 0x80, 0xF0, 0x80, 0x80  // F
```