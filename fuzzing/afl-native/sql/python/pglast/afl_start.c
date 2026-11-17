#include <stdint.h>

__attribute__((noinline)) void parsarium_afl_start(void) {
    volatile uint32_t marker = 0;
    marker++;
}
