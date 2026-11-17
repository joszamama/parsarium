#ifndef PARSARIUM_LIBRSVG_SVG_HARNESS_H
#define PARSARIUM_LIBRSVG_SVG_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_svg_result {
    unsigned width, height;
    unsigned char first[3], second[3];
    int second_present;
};
int parsarium_parse_svg(const uint8_t *data, size_t size, struct parsarium_svg_result *result);
#endif
