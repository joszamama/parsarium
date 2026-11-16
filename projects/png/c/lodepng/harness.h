#ifndef PARSARIUM_LODEPNG_PNG_HARNESS_H
#define PARSARIUM_LODEPNG_PNG_HARNESS_H

#include <stddef.h>
#include <stdint.h>

struct parsarium_png_result {
    unsigned width;
    unsigned height;
    unsigned char first[4];
    unsigned char second[4];
    int has_second;
};

int parsarium_parse_png(const uint8_t *data, size_t size,
                        struct parsarium_png_result *result);

#endif
