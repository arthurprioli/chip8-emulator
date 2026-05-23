#ifndef CPU_H
#define CPU_H

typedef struct {
    unsigned short *PC;
    unsigned short *I;
    unsigned char V0, V1, V2, V3, V4, V5, V6, V7, V8, V9, VA, VB, VC, VD, VE, VF;
} CPU;

#endif