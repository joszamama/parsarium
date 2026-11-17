#ifndef PARSARIUM_THORVG_CPP_SVG_HARNESS_H
#define PARSARIUM_THORVG_CPP_SVG_HARNESS_H

#include <stddef.h>
#include <stdint.h>

struct parsarium_svg_result {
    unsigned width;
    unsigned height;
};

int parsarium_parse_svg(const uint8_t *data, size_t size,
                        struct parsarium_svg_result *result);

#endif
