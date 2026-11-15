#ifndef PARSARIUM_PLUTOSVG_HARNESS_H
#define PARSARIUM_PLUTOSVG_HARNESS_H
#include <stddef.h>
#include <stdint.h>

struct parsarium_svg_result {
    int width;
    int height;
    uint8_t first[3];
    uint8_t second[3];
};
int parsarium_parse_svg(const uint8_t *data, size_t size,
                        struct parsarium_svg_result *result);
#endif
