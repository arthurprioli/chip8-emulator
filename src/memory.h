#ifndef MEMORY_H
#define MEMORY_H

typedef struct {
    short* main_memory[4096];
    short* stack[2];
} Memory;

#endif