#ifndef PARSARIUM_LIBRSVG_CPP_SVG_HARNESS_H
#define PARSARIUM_LIBRSVG_CPP_SVG_HARNESS_H

#include <cstddef>
#include <cstdint>

struct parsarium_svg_result {
    unsigned width;
    unsigned height;
    unsigned char first[3];
    unsigned char second[3];
    bool second_present;
};

bool parsarium_parse_svg(const std::uint8_t *data, std::size_t size,
                         parsarium_svg_result *result);

#endif
