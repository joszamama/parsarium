#ifndef PARSARIUM_CPP_LODEPNG_HARNESS_HPP
#define PARSARIUM_CPP_LODEPNG_HARNESS_HPP

#include <array>
#include <cstddef>
#include <cstdint>

struct ParsariumPngResult {
    unsigned width;
    unsigned height;
    std::array<unsigned char, 4> first;
    std::array<unsigned char, 4> second;
};

bool parsarium_parse_png(const std::uint8_t *data, std::size_t size,
                         ParsariumPngResult &result);

#endif
