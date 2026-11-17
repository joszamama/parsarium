#ifndef PARSARIUM_GTK4_SVG_H
#define PARSARIUM_GTK4_SVG_H
#include <stddef.h>
#include <stdint.h>

struct parsarium_svg_result {
    int width;
    int height;
};

int parsarium_parse_svg(const uint8_t *data, size_t size,
                        struct parsarium_svg_result *result);
#endif
