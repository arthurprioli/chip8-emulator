#include <stdlib.h>
#include <stdio.h>
#include "cpu.h"
#include "display.h"
#include "memory.h"
#include "timers.h"

// define a startup function to put font inside of memory
// start both timers at 0 
// start all CPU values at 0 

short* store_font(short* main_mem)
{
    

    return main_mem;
}

Memory* init_memory()
{
    Memory* mem = (Memory*) malloc(sizeof(Memory));
    short* font[] = { (short)0xF0, (short)0x90, (short)0x90, (short)0x90, (short)0xF0,
    (short)0x20, (short)0x60, (short)0x20, (short)0x20, (short)0x70, 
    (short)0xF0, (short)0x10, (short)0xF0, (short)0x80, (short)0xF0, 
    (short)0xF0, (short)0x10, (short)0xF0, (short)0x10, (short)0xF0, 
    (short)0x90, (short)0x90, (short)0xF0, (short)0x10, (short)0x10, 
    (short)0xF0, (short)0x80, (short)0xF0, (short)0x10, (short)0xF0, 
    (short)0xF0, (short)0x80, (short)0xF0, (short)0x90, (short)0xF0, 
    (short)0xF0, (short)0x10, (short)0x20, (short)0x40, (short)0x40, 
    (short)0xF0, (short)0x90, (short)0xF0, (short)0x90, (short)0xF0, 
    (short)0xF0, (short)0x90, (short)0xF0, (short)0x10, (short)0xF0, 
    (short)0xF0, (short)0x90, (short)0xF0, (short)0x90, (short)0x90, 
    (short)0xE0, (short)0x90, (short)0xE0, (short)0x90, (short)0xE0, 
    (short)0xF0, (short)0x80, (short)0x80, (short)0x80, (short)0xF0, 
    (short)0xE0, (short)0x90, (short)0x90, (short)0x90, (short)0xE0, 
    (short)0xF0, (short)0x80, (short)0xF0, (short)0x80, (short)0xF0, 
    (short)0xF0, (short)0x80, (short)0xF0, (short)0x80, (short)0x80 };

    for (int i = 0; i < 80; i++)
    {
        mem->main_memory[i] = font[i];
    }
    return mem;
}

CPU* init_cpu()
{
    CPU* my_cpu = (CPU*) malloc(sizeof(CPU));
    my_cpu->I = 0;
    
}

Timers* init_timers()
{

}

Display* init_display()
{

}



int main()
{
    Memory* mem = init_memory();

    for (int i = 0; i < 4096; i++)
    {
        printf("%d\n", mem->main_memory[i]);
    }
    return 0;
}
